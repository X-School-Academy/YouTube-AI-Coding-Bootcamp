from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import threading
from generators.text_generator import generate_text
from generators.speech_generator import generate_speech
from generators.image_generator import generate_images
from generators.video_generator import create_video
from utils.helpers import ensure_directories_exist
import config

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # 启用所有域名所有路由的CORS

# 确保必要的目录存在
ensure_directories_exist([config.TEMP_DIR, config.OUTPUT_DIR])

# 存储任务状态
jobs = {}

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('../frontend', path)

@app.route('/api/generate', methods=['POST'])
def generate_video():
    data = request.json
    prompt = data.get('prompt', '')
    style = data.get('style', 'children_story')
    
    if not prompt:
        return jsonify({'error': '需要提供提示词'}), 400
    
    # 生成唯一任务ID
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        'status': 'queued',
        'progress': 0,
        'message': '任务已加入队列',
        'video_url': None
    }
    
    # 在后台线程中启动生成过程
    thread = threading.Thread(target=process_job, args=(job_id, prompt, style))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id})

def process_job(job_id, prompt, style):
    try:
        update_job_status(job_id, 'processing', 10, '正在生成文本内容...')
        
        # 生成文本内容
        text_content = generate_text(prompt, style)
        
        update_job_status(job_id, 'processing', 30, '正在生成语音...')
        
        # 为每个场景生成语音
        audio_files = generate_speech(text_content)
        
        update_job_status(job_id, 'processing', 50, '正在生成图像...')
        
        # 为每个场景生成图像
        image_files = generate_images(text_content)
        
        update_job_status(job_id, 'processing', 80, '正在创建视频...')
        
        # 创建最终视频
        video_path = create_video(text_content, image_files, audio_files)
        
        # 创建视频的相对URL
        video_url = f'/api/videos/{os.path.basename(video_path)}'
        
        update_job_status(job_id, 'completed', 100, '视频生成完成！', video_url)
        
    except Exception as e:
        update_job_status(job_id, 'failed', 0, f'错误: {str(e)}')

def update_job_status(job_id, status, progress, message, video_url=None):
    if job_id in jobs:
        jobs[job_id]['status'] = status
        jobs[job_id]['progress'] = progress
        jobs[job_id]['message'] = message
        if video_url:
            jobs[job_id]['video_url'] = video_url

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': '找不到任务'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/api/videos/<filename>')
def serve_video(filename):
    return send_from_directory(config.OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
