#!/bin/bash

# 电子书视频生成器
# 将5张图片和对应的5个MP3音频文件合成为一个视频

# 检查ffmpeg是否已安装
if ! command -v ffmpeg &> /dev/null; then
    echo "错误: 未安装ffmpeg。请先安装ffmpeg。"
    exit 1
fi

# 创建临时目录
TEMP_DIR="temp_video_files"
mkdir -p "$TEMP_DIR"

# 创建片段列表文件
SEGMENTS_FILE="$TEMP_DIR/segments.txt"
> "$SEGMENTS_FILE"

echo "开始创建电子书视频..."

# 处理每个图片和音频对
for i in {1..5}; do
    echo "处理第 $i 页..."
    
    # 输入文件
    IMAGE_FILE="image$i.png"  # 图片文件名格式
    AUDIO_FILE="audio$i.mp3"  # 音频文件名格式
    
    # 检查文件是否存在
    if [ ! -f "$IMAGE_FILE" ]; then
        echo "错误: 图片文件 $IMAGE_FILE 不存在。"
        exit 1
    fi
    
    if [ ! -f "$AUDIO_FILE" ]; then
        echo "错误: 音频文件 $AUDIO_FILE 不存在。"
        exit 1
    fi
    
    # 从图片和音频创建视频片段
    ffmpeg -hide_banner -loglevel warning \
           -loop 1 -i "$IMAGE_FILE" -i "$AUDIO_FILE" \
           -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
           -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
           -shortest \
           "$TEMP_DIR/segment$i.mp4"
    
    # 添加到片段列表
    echo "file 'segment$i.mp4'" >> "$SEGMENTS_FILE"
done

# 将所有片段合并为一个视频
echo "合并片段为最终视频..."
ffmpeg -hide_banner -loglevel warning \
       -f concat -safe 0 -i "$SEGMENTS_FILE" \
       -c copy "ebook_video.mp4"

# 清理临时文件
echo "清理临时文件..."
rm -rf "$TEMP_DIR"

echo "电子书视频已创建: ebook_video.mp4"