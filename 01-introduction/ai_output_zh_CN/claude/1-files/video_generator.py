import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
import config
from utils.helpers import ensure_directories_exist

def create_video(scenes, image_files, audio_files):
    """
    通过组合图像、文本叠加层和音频文件创建视频。
    
    参数:
        scenes (list): 场景字典列表
        image_files (list): 图像文件路径列表
        audio_files (list): 音频文件路径列表
        
    返回:
        str: 生成的视频文件路径
    """
    # 确保输出目录存在
    ensure_directories_exist([config.OUTPUT_DIR])
    
    # 为输出视频生成唯一文件名
    output_filename = f"video_{os.urandom(4).hex()}.mp4"
    output_path = os.path.join(config.OUTPUT_DIR, output_filename)
    
    clips = []
    
    for i, (scene, image_file, audio_file) in enumerate(zip(scenes, image_files, audio_files)):
        # 加载音频以获取其持续时间
        audio = mp.AudioFileClip(audio_file)
        audio_duration = audio.duration
        
        # 创建场景剪辑
        image_clip = mp.ImageClip(image_file).set_duration(audio_duration)
        
        # 添加文本叠加
        title_text = scene['title']
        
        # 创建带有文本的临时图像
        temp_img = Image.open(image_file)
        draw = ImageDraw.Draw(temp_img)
        
        # 尝试加载字体，如果不可用则使用默认字体
        try:
            font = ImageFont.truetype("Arial", 40)
        except IOError:
            font = ImageFont.load_default()
        
        # 在顶部添加标题
        draw.text((50, 50), title_text, fill="white", font=font, stroke_width=2, stroke_fill="black")
        
        # 保存带有文本叠加的图像
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            text_image_path = tmp.name
            temp_img.save(text_image_path, format='PNG')
        
        # 创建带有文本叠加的剪辑
        text_image_clip = mp.ImageClip(text_image_path).set_duration(audio_duration)
        
        # 与音频组合
        final_clip = text_image_clip.set_audio(audio)
        
        # 添加到剪辑列表
        clips.append(final_clip)
        
        # 清理临时文件
        os.unlink(text_image_path)
    
    # 连接所有剪辑
    final_video = mp.concatenate_videoclips(clips, method="compose")
    
    # 将最终视频写入文件
    final_video.write_videofile(
        output_path,
        fps=config.FPS,
        codec='libx264',
        audio_codec='aac'
    )
    
    return output_path
