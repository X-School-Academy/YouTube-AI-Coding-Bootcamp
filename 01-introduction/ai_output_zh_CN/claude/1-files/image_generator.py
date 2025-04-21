import openai
import os
import requests
import config
from utils.helpers import ensure_directories_exist

def generate_images(scenes):
    """
    使用OpenAI的DALL-E模型为每个场景生成图像。
    
    参数:
        scenes (list): 包含图像提示的场景字典列表
        
    返回:
        list: 生成的图像文件路径列表
    """
    # 确保临时目录存在
    image_dir = os.path.join(config.TEMP_DIR, 'images')
    ensure_directories_exist([image_dir])
    
    # 初始化OpenAI客户端
    openai.api_key = config.OPENAI_API_KEY
    
    image_files = []
    
    for i, scene in enumerate(scenes):
        # 提取图像提示并增强它以获得更好的质量
        image_prompt = (
            f"创建一个高质量、详细的视频场景插图: "
            f"{scene['image_prompt']} 图像应该清晰、教育性强，"
            f"适合所有年龄段。场景标题: {scene['title']}"
        )
        
        # 生成文件名
        filename = f"scene_{i+1}.png"
        filepath = os.path.join(image_dir, filename)
        
        # 调用OpenAI DALL-E API
        response = openai.Image.create(
            model=config.IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024",
            n=1,
            response_format="url"
        )
        
        # 下载图像
        image_url = response.data[0].url
        r = requests.get(image_url, stream=True)
        
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            
            image_files.append(filepath)
        else:
            raise Exception(f"下载图像失败: {r.status_code}")
    
    return image_files
