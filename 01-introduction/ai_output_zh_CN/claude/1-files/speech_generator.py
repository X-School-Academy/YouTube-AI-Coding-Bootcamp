import openai
import os
import config
from utils.helpers import ensure_directories_exist

def generate_speech(scenes):
    """
    使用OpenAI的TTS模型为每个场景生成语音音频文件。
    
    参数:
        scenes (list): 包含叙述文本的场景字典列表
        
    返回:
        list: 生成的音频文件路径列表
    """
    # 确保临时目录存在
    audio_dir = os.path.join(config.TEMP_DIR, 'audio')
    ensure_directories_exist([audio_dir])
    
    # 初始化OpenAI客户端
    openai.api_key = config.OPENAI_API_KEY
    
    audio_files = []
    
    for i, scene in enumerate(scenes):
        narration = scene['narration']
        voice = config.STYLE_TEMPLATES.get(scene.get('style', 'children_story'), {}).get('voice', 'alloy')
        
        # 生成文件名
        filename = f"scene_{i+1}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        # 调用OpenAI TTS API
        response = openai.Audio.create(
            model=config.SPEECH_MODEL,
            voice=voice,
            input=narration
        )
        
        # 保存音频文件
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        audio_files.append(filepath)
    
    return audio_files
