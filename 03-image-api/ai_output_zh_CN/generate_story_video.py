#!/usr/bin/env python3
import json
import base64
import subprocess
from openai import OpenAI

def main():
    # 初始化 OpenAI 客户端
    client = OpenAI()

    # 读取场景列表
    with open("story.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    # 准备临时目录和片段列表文件
    temp_dir = "temp_video_files"
    subprocess.run(["mkdir", "-p", temp_dir], check=True)
    segments_file = f"{temp_dir}/segments.txt"
    open(segments_file, "w").close()

    # 遍历每个场景：生成图像 + 合成视频片段
    for idx, scene in enumerate(scenes, start=1):
        print(f"处理第 {idx} 场景：{scene['scene_title']}")

        # 调整提示，添加风格和中文对话框
        prompt = (
            f"{scene['image_prompt']}，吉卜力风格漫画风格，" 
            "并且在漫画面中添加中文对话框"
        )
        # 调用 GPT-Image 生成图像
        img = client.images.generate(
            model="gpt-image-1",
            output_format="png",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        # 解码并保存图像
        image_bytes = base64.b64decode(img.data[0].b64_json)
        image_path = f"{temp_dir}/image{idx}.png"
        with open(image_path, "wb") as img_f:
            img_f.write(image_bytes)

        # 声音文件路径
        audio_path = scene["audio_file"]
        segment_path = f"{temp_dir}/segment{idx}.mp4"

        # 调用 ffmpeg 生成视频片段
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning",
            "-loop", "1", "-i", image_path, "-i", audio_path,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-vf",
            "scale=1280:720:force_original_aspect_ratio=decrease,"
            "pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-shortest", segment_path
        ], check=True)

        # 写入片段列表
        with open(segments_file, "a", encoding="utf-8") as seg_f:
            seg_f.write(f"file '{segment_path}'\n")

    # 合并所有视频片段
    final_video = "ebook_video.mp4"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "warning",
        "-f", "concat", "-safe", "0", "-i", segments_file,
        "-c", "copy", final_video
    ], check=True)

    # 清理临时文件夹
    subprocess.run(["rm", "-rf", temp_dir], check=True)

    # 输出最终文件名
    print(f"视频已创建: {final_video}")

if __name__ == "__main__":
    main()
