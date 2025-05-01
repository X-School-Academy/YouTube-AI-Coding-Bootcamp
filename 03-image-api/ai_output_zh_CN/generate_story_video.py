import json
import os
import subprocess
import base64
import shutil
import sys
from openai import OpenAI, APIError  # Import APIError for better error handling

# --- 配置 ---
STORY_JSON_FILE = "story.json"
TEMP_DIR = "temp_video_files"
SEGMENTS_FILE_NAME = "segments.txt"
FINAL_VIDEO_NAME = "ebook_video.mp4"
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
IMAGE_SIZE = "1024x1024" # DALL-E 3 支持的尺寸之一
# 注意：根据 OpenAI 文档，推荐使用 'dall-e-3' 模型。
# 如果 'gpt-image-1' 不可用或报错，请尝试更换为 'dall-e-3'。
IMAGE_MODEL = "gpt-image-1"
IMAGE_STYLE_PROMPT = ", 吉卜力漫画风格, 包含中文对话框" # Style appended to user prompt

# --- OpenAI 客户端初始化 ---
# 确保您的 OpenAI API 密钥已设置为环境变量 OPENAI_API_KEY
try:
    client = OpenAI()
except Exception as e:
    print(f"错误：无法初始化 OpenAI 客户端。请确保 OPENAI_API_KEY 环境变量已设置。")
    print(f"详细错误: {e}")
    sys.exit(1)

# --- 函数定义 ---

def check_ffmpeg():
    """检查 ffmpeg 是否安装并可用"""
    if shutil.which("ffmpeg") is None:
        print("错误: 未找到 ffmpeg。请先安装 ffmpeg 并确保它在系统的 PATH 中。")
        sys.exit(1)
    print("ffmpeg 已找到。")

def generate_image(prompt, output_path, scene_index):
    """使用 OpenAI API 生成图片并保存"""
    full_prompt = prompt + IMAGE_STYLE_PROMPT
    print(f"  为场景 {scene_index + 1} 生成图片，提示: \"{prompt}\" (风格: 吉卜力漫画, 中文对话框)")
    try:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=full_prompt,
            n=1,
            size=IMAGE_SIZE # 使用 OpenAI 支持的标准尺寸
            #response_format="b64_json" # This parameter isn't supported for gpt-image-1 which will always return base64-encoded images.
        )
        # 从响应中获取 base64 数据
        if response.data and response.data[0].b64_json:
            image_b64 = response.data[0].b64_json
            # 解码并保存图片
            image_bytes = base64.b64decode(image_b64)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            print(f"  图片已保存到: {output_path}")
            return True
        else:
            print(f"错误：OpenAI API 返回了空的图片数据。")
            return False

    except APIError as e:
        print(f"错误：调用 OpenAI API 时出错 (场景 {scene_index + 1})。")
        print(f"  状态码: {e.status_code}")
        print(f"  响应: {e.response}")
        print(f"  提示: {full_prompt}")
        # 检查是否是无效模型错误
        if "invalid_model" in str(e).lower() or (hasattr(e, 'code') and e.code == 'invalid_request_error'):
             print(f"\n  提示: 检测到无效模型错误。您可能需要将脚本中的 IMAGE_MODEL 从 '{IMAGE_MODEL}' 更改为 'dall-e-3'。\n")
        return False
    except Exception as e:
        print(f"错误：生成图片时发生未知错误 (场景 {scene_index + 1}): {e}")
        return False


def create_video_segment(image_path, audio_path, output_segment_path, scene_index):
    """使用 ffmpeg 将图片和音频合并为视频片段"""
    print(f"  为场景 {scene_index + 1} 创建视频片段...")

    if not os.path.exists(image_path):
        print(f"错误：图片文件 {image_path} 不存在。")
        return False
    if not os.path.exists(audio_path):
        print(f"错误：音频文件 {audio_path} 不存在。")
        return False

    try:
        # 构建 ffmpeg 命令列表
        # 使用 scale 和 pad 滤镜来调整图像大小并适应 1280x720 的视频尺寸
        vf_filter = (
            f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
            f"format=yuv420p"
        )

        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "warning",  # 或使用 "error" 获取更少的日志
            "-loop", "1",           # 循环输入图像
            "-i", image_path,       # 输入图像文件
            "-i", audio_path,       # 输入音频文件
            "-vf", vf_filter,       # 视频滤镜（缩放、填充、像素格式）
            "-c:v", "libx264",      # 视频编解码器
            "-tune", "stillimage",  # 针对静态图像优化
            "-c:a", "aac",          # 音频编解码器
            "-b:a", "192k",         # 音频比特率
            "-shortest",            # 使输出时长与最短的输入（音频）匹配
            output_segment_path     # 输出视频片段文件
        ]

        # 执行命令
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        # print(f"  ffmpeg 输出:\n{result.stdout}") # 可选：打印 ffmpeg 输出
        if result.stderr:
             print(f"  ffmpeg 警告/错误:\n{result.stderr}") # 打印警告或错误
        print(f"  视频片段已创建: {output_segment_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"错误：执行 ffmpeg 命令失败 (场景 {scene_index + 1})。")
        print(f"  命令: {' '.join(e.cmd)}")
        print(f"  返回码: {e.returncode}")
        print(f"  错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"错误：创建视频片段时发生未知错误 (场景 {scene_index + 1}): {e}")
        return False

def concatenate_videos(segment_list_path, output_video_path):
    """将所有视频片段合并为一个最终视频"""
    print("合并片段为最终视频...")
    if not os.path.exists(segment_list_path) or os.path.getsize(segment_list_path) == 0:
        print(f"错误: 片段列表文件 {segment_list_path} 为空或不存在。")
        return False

    try:
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "warning",
            "-f", "concat",         # 使用 concat demuxer
            "-safe", "0",           # 允许不安全的（例如，相对）文件名
            "-i", segment_list_path,# 输入片段列表文件
            "-c", "copy",           # 直接复制代码流，不重新编码
            output_video_path       # 输出最终视频文件
        ]
        # 执行命令
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stderr:
             print(f"  ffmpeg 警告/错误:\n{result.stderr}") # 打印警告或错误
        print(f"最终视频合并完成: {output_video_path}")
        return True

    except subprocess.CalledProcessError as e:
        print("错误：合并视频片段时 ffmpeg 执行失败。")
        print(f"  命令: {' '.join(e.cmd)}")
        print(f"  返回码: {e.returncode}")
        print(f"  错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"错误：合并视频时发生未知错误: {e}")
        return False

def main():
    """主执行函数"""
    check_ffmpeg()

    # 1. 读取 story.json
    try:
        with open(STORY_JSON_FILE, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
        if not isinstance(story_data, list) or not story_data:
             print(f"错误: {STORY_JSON_FILE} 不是有效的 JSON 列表或为空。")
             sys.exit(1)
        print(f"成功读取 {STORY_JSON_FILE}，包含 {len(story_data)} 个场景。")
    except FileNotFoundError:
        print(f"错误: 故事文件 {STORY_JSON_FILE} 未找到。")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: 解析 {STORY_JSON_FILE} 时出错，请检查 JSON 格式。")
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取故事文件时发生未知错误: {e}")
        sys.exit(1)

    # 2. 创建临时目录
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"临时目录 '{TEMP_DIR}' 已创建或已存在。")

    # 3. 准备片段列表文件
    segments_file_path = os.path.join(TEMP_DIR, SEGMENTS_FILE_NAME)
    generated_segments = []

    print("\n开始处理场景...")
    all_steps_successful = True

    # 4. 循环处理每个场景
    for i, scene in enumerate(story_data):
        print(f"\n--- 处理场景 {i + 1}/{len(story_data)} ---")
        scene_title = scene.get("scene_title", f"场景 {i+1}")
        audio_file = scene.get("audio_file")
        image_prompt = scene.get("image_prompt")

        if not audio_file or not image_prompt:
            print(f"警告：场景 {i + 1} 缺少 'audio_file' 或 'image_prompt'，跳过此场景。")
            continue

        # 定义此场景的文件名
        image_filename = f"image_scene_{i + 1}.png"
        segment_filename = f"segment_{i + 1}.mp4"
        image_path = os.path.join(TEMP_DIR, image_filename)
        segment_path = os.path.join(TEMP_DIR, segment_filename)

        # 检查音频文件是否存在 (相对或绝对路径)
        if not os.path.exists(audio_file):
            print(f"错误：场景 {i+1} 的音频文件 '{audio_file}' 未找到。请确保路径正确。")
            all_steps_successful = False
            break # 或者可以选择 continue 跳过

        # A. 生成图片
        if not generate_image(image_prompt, image_path, i):
            print(f"错误：无法为场景 {i + 1} 生成图片。")
            all_steps_successful = False
            break # 停止处理

        # B. 创建视频片段
        if not create_video_segment(image_path, audio_file, segment_path, i):
            print(f"错误：无法为场景 {i + 1} 创建视频片段。")
            all_steps_successful = False
            break # 停止处理

        # C. 记录片段以供合并
        generated_segments.append(f"file '{segment_filename}'") # 使用相对于临时目录的路径

    # 5. 如果所有片段都成功生成，则写入片段列表文件并合并
    if all_steps_successful and generated_segments:
        try:
            with open(segments_file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(generated_segments))
            print(f"\n片段列表文件已写入: {segments_file_path}")

            # D. 合并所有片段
            if not concatenate_videos(segments_file_path, FINAL_VIDEO_NAME):
                all_steps_successful = False
        except IOError as e:
             print(f"错误: 无法写入片段列表文件 {segments_file_path}: {e}")
             all_steps_successful = False

    # 6. 清理或提示
    if all_steps_successful and os.path.exists(FINAL_VIDEO_NAME):
        print("\n清理临时文件...")
        try:
            shutil.rmtree(TEMP_DIR)
            print(f"临时目录 '{TEMP_DIR}' 已删除。")
        except OSError as e:
            print(f"警告：无法完全删除临时目录 '{TEMP_DIR}': {e}")
        print(f"\n🎉 电子书视频已成功创建！")
        print(f"输出文件名: {FINAL_VIDEO_NAME}") # 输出最终文件名
    else:
        print("\n❌ 处理过程中发生错误，视频未生成或未完成。")
        print(f"临时文件保留在 '{TEMP_DIR}' 目录中以供检查。")
        # 如果最终文件存在但过程有错，也提示一下
        if os.path.exists(FINAL_VIDEO_NAME):
             print(f"注意：最终视频文件 '{FINAL_VIDEO_NAME}' 可能已生成，但可能不完整或存在问题。")


if __name__ == "__main__":
    main()