# OpenAI最新图片生成API使用指南

[English Version](README.md)

### 1. 氛围学习关键词（Google、YouTube 或 AI 搜索）

- 什么是 JSON 文本格式
- 什么是 RESTful API
- 什么是 curl 命令
- OpenAI 图片API文档
- Base64 编码
- Mermaid 流程图
- 吉卜力风格漫画风格
- 什么是 Python

### 2. 复习上节课创建的视频脚本

提示词：

1. 请检查这个脚本，列出我需要掌握哪些知识点，以便能够大致理解这个脚本的内容。
2. 请检查提供的 Shell 脚本，说明如何使用它来创建有声视频。 请给出文字版步骤说明，并用 Mermaid 流程图展示。

Shell 脚本：[create_ebook_video.sh](ai_output_zh_CN/create_ebook_video.sh)

### 3. 学习如何查看API文档： OpenAI 最新图片生成模型 —— `gpt-image-1`

[API 网址](https://platform.openai.com/docs/api-reference/images/create)

> （使用 Chrome 浏览器：右键点击页面 -> 翻译）

GPT Image 模型简介：  

这是一款原生多模态语言模型，能够基于对世界的视觉理解，生成包含真实细节的高质量图像。  
例如，当提示 GPT Image 生成一个展示最受欢迎半宝石的玻璃柜时，它会自动选择紫水晶、玫瑰石英、玉石等，并以逼真的风格绘制出来。

API测试示例（Shell 命令）：

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-image-1",
    "output_format": "png",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024"
  }'
```

如何调用API（Python 代码）：

```python
import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="gpt-image-1",
    output_format="png",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

### 4. 创建Python脚本，并使用 OpenAI `gpt-image-1` 模型自动生成图像

#### 1. 准备 JSON 数据

提示词：

请将以下 Markdown 格式文本转换成 JSON 格式，  
并将每个场景的文字内容替换为对应的音频文件（audio1.mp3 到 audio5.mp3），  
保留原有的图片生成提示语。

Markdown 文本：

\<markdown\>

  \<\<原始Markdown文本\>\>

\</markdown\>

输出格式示例：

\<output\>
```json
[
    {
        "scene_title": "string",
        "audio_file": "audio1.mp3",
        "image_prompt": "string"
    }
]
```
\</output\>

> 原始 Markdown 格式故事文本：[文本链接](../02-linux-ffmpeg/ai_output_zh_CN/claude/3.md)

#### 2. 编写 Python 脚本，使用 OpenAI `gpt-image-1` API

提示词：

请参考下面提供的 Linux Shell 脚本

\<shell_script\>
    \<\<FFmpeg Shell 脚本\>\>
\</shell_script\>

然后请创建一个 Python 脚本，要求如下：

1. 读取名为 `story.json` 的文件，格式如下：

```json
[
    {
        "scene_title": "string",
        "audio_file": "audio1.mp3",
        "image_prompt": "string"
    }
]
```

2. 自动根据 JSON 文件中每个场景的 `image_prompt`，调用 OpenAI 最新的 `gpt-image-1` API 生成图片。  
参考代码如下：

```python
import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="gpt-image-1",
    output_format="png",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

3. 要求生成的图片风格为“吉卜力风格漫画风格”，并且在漫画面中添加中文对话框。

4. 在 Python 脚本最后输出生成的视频文件名。  

**关于如何调用 ffmpeg 命令，可以参考前面提供的 Shell 脚本。**
