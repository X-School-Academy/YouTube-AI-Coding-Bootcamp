#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import base64
import subprocess
import shutil
from openai import OpenAI

def read_story_json(file_path="story.json"):
    """读取并解析故事JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"错误: {file_path} 不是有效的JSON文件")
        exit(1)

def generate_image(prompt, output_file, api_key=None):
    """使用OpenAI的API生成图片"""
    # 如果未提供API密钥，则从环境变量中获取
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("错误: 未设置OPENAI_API_KEY环境变量")
            exit(1)
    
    # 初始化OpenAI客户端
    client = OpenAI(api_key=api_key)
    
    # 增强提示词，指定吉卜力风格和中文对话框
    enhanced_prompt = f"吉卜力风格漫画风格: {prompt}, 包含中文对话框"
    
    try:
        # 生成图片
        img = client.images.generate(
            model="gpt-image-1",
            output_format="png",
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024"
        )
        
        # 解码并保存图片
        image_bytes = base64.b64decode(img.data[0].b64_json)
        with open(output_file, "wb") as f:
            f.write(image_bytes)
        
        print(f"已生成图片: {output_file}")
        return True
    
    except Exception as e:
        print(f"生成图片时出错: {str(e)}")
        return False

def create_video(story_data, output_video="ebook_video.mp4"):
    """从图片和音频文件创建视频"""
    # 创建临时目录
    temp_dir = "temp_video_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 创建片段列表文件
    segments_file = os.path.join(temp_dir, "segments.txt")
    with open(segments_file, 'w') as f:
        pass  # 创建空文件
    
    print("开始创建电子书视频...")
    
    # 处理每个场景
    for i, scene in enumerate(story_data, 1):
        print(f"处理第 {i} 页...")
        
        # 输入文件
        image_file = f"image{i}.png"
        audio_file = scene["audio_file"]
        
        # 检查音频文件是否存在
        if not os.path.isfile(audio_file):
            print(f"错误: 音频文件 {audio_file} 不存在。")
            exit(1)
        
        # 创建视频片段
        segment_file = f"segment{i}.mp4"
        segment_path = os.path.join(temp_dir, segment_file)
        
        ffmpeg_cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "warning",
            "-loop", "1", "-i", image_file, "-i", audio_file,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-shortest", segment_path
        ]
        
        subprocess.run(ffmpeg_cmd, check=True)
        
        # 添加到片段列表
        with open(segments_file, 'a') as f:
            f.write(f"file '{segment_file}'\n")
    
    # 将所有片段合并为一个视频
    print("合并片段为最终视频...")
    
    # 切换到临时目录以执行ffmpeg命令
    current_dir = os.getcwd()
    os.chdir(temp_dir)
    
    ffmpeg_merge_cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning",
        "-f", "concat", "-safe", "0", "-i", "segments.txt",
        "-c", "copy", f"../{output_video}"
    ]
    
    subprocess.run(ffmpeg_merge_cmd, check=True)
    
    # 返回原始目录
    os.chdir(current_dir)
    
    # 清理临时文件
    print("清理临时文件...")
    shutil.rmtree(temp_dir)
    
    print(f"电子书视频已创建: {output_video}")
    return output_video

def main():
    # 读取故事数据
    story_data = read_story_json()
    
    # 为每个场景生成图片
    for i, scene in enumerate(story_data, 1):
        image_file = f"image{i}.png"
        print(f"为场景 '{scene['scene_title']}' 生成图片...")
        if not generate_image(scene["image_prompt"], image_file):
            print(f"错误: 为场景 {i} 生成图片失败")
            exit(1)
    
    # 创建视频
    output_video = create_video(story_data)
    
    # 输出生成的视频文件名
    print(f"成功生成视频: {output_video}")

if __name__ == "__main__":
    main()