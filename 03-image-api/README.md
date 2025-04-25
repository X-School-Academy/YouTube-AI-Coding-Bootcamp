# OpenAI Image Generation API Usage Guide

[中文版](README_zh_CN.md)

### 1. Key Concepts for Immersive Learning (via Google, YouTube or AI Search)

- What is the JSON text format  
- What is a RESTful API  
- What is the `curl` command  
- OpenAI Images API documentation  
- Base64 encoding  
- Mermaid flowcharts  
- Studio Ghibli–style illustrations  
- What is Python  

### 2. Review the Video Script from Last Lesson

**Prompts:**

1. Please review this script and list the key concepts I need to understand in order to grasp its overall content.  
2. Please examine the provided shell script and explain how to use it to create a narrated video. Provide a written, step-by-step guide and illustrate it with a Mermaid flowchart.

Shell script: [create_ebook_video.sh](ai_output_zh_CN/create_ebook_video.sh)

### 3. Learning to Navigate the API Documentation: OpenAI’s Latest Image Generation Model — `gpt-image-1`

[API Reference](https://platform.openai.com/docs/api-reference/images/create)

> (Using Chrome: right-click on the page → Translate)

**Introduction to the GPT Image model**  
This is a first-party multimodal language model that can generate high-quality images with realistic details based on its visual understanding of the world. For example, if you ask GPT Image to render a glass display case showcasing the most popular semi-precious stones, it will automatically select amethyst, rose quartz, jade, etc., and draw them in a lifelike style.

**API Test Example (Shell command):**
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

**How to Call the API (Python code):**
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

### 4. Create a Python Script to Auto-Generate Images with the OpenAI `gpt-image-1` Model

#### 1. Preparing the JSON Data

**Prompt:**  
Please convert the following Markdown-formatted text into JSON. Replace each scene’s text content with the corresponding audio file name (`audio1.mp3` through `audio5.mp3`), while preserving the original image-generation prompts.

**Markdown Text:**
```markdown
<<Original Markdown Text>>
```

**Expected Output Format:**
```json
[
    {
        "scene_title": "string",
        "audio_file": "audio1.mp3",
        "image_prompt": "string"
    }
]
```

> Original Markdown story text: [Text Link](../02-linux-ffmpeg/ai_output_zh_CN/claude/3.md)

#### 2. Writing the Python Script Using the OpenAI `gpt-image-1` API

**Prompt:**  
Please refer to the following Linux shell script:

```bash
<<FFmpeg Shell Script>>
```

Then create a Python script that:

1. Reads a file named `story.json` in this format:
   ```json
   [
       {
           "scene_title": "string",
           "audio_file": "audio1.mp3",
           "image_prompt": "string"
       }
   ]
   ```

2. Automatically calls the OpenAI `gpt-image-1` API for each scene’s `image_prompt` in the JSON file. You can use this example as a reference:
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

3. Ensures that the generated images have a “Ghibli-style comic” aesthetic and include Chinese dialogue bubbles within the comic panels.

4. Outputs the filename of the generated video at the end of the Python script.

> **Note:** You can refer to the previously provided shell script for guidance on how to invoke `ffmpeg`.