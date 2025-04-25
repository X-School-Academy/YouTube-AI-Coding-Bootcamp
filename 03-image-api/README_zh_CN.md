# OpenAI最新图片生成API的使用

[English Version](README.md)

### 1. 氛围学习网络搜素关键词 （Google, YouTube or AI）

- What is Json text format
- What is Restful API
- What is curl command
- Openai's Image APIs
- Base64 encode
- mermaid Diagram

### 2. Review the video script created in the last session 

Prompts:

1. Please check the script for which knowleges I need to know, so I can have a basic understand tp it
2. Please check the shell script for how to use it to create an audio video.
Give me the steps in text and Mermaid Diagram as well

Shell script: [create_ebook_video.sh](ai_output_zh_CN/create_ebook_video.sh)

### 3. Review the latest openAI image generation model api - `gpt-image-1`

> Right click (Google Chrome): Translate to English, then to Chinese 

GPT Image模型： 原生多模态语言模型可以利用其对世界的视觉理解，即可生成包含真实细节的逼真图像。
例如，如果您提示 GPT Image 生成一个带有最受欢迎的半宝石的玻璃柜图像，该模型就会知道选择紫水晶、玫瑰石英、玉石等宝石，并以逼真的方式描绘它们。

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-image-1",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024"
  }'
```

```python
import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="gpt-image-1",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

### 4. Update the script to python and use OpenAI `gpt-image-1` model 

1. Prepare json data as input

Prompt: 

Convert the markdown text to json, provide mp3 file but keep the image creation prompts 

2. Ask to write Python script to use  OpenAI `gpt-image-1` model api

Prompt: 