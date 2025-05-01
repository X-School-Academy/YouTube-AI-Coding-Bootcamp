# OpenAI最新图片生成API使用指南

[English Version](README.md)

### ▶️ 油管直播视频

[![Watch on YouTube](https://img.youtube.com/vi/3F5D09KyjFE/mqdefault.jpg)](https://youtu.be/3F5D09KyjFE)

[播放](https://youtu.be/3F5D09KyjFE)

### 1. 氛围学习关键词

- JSON
- RESTful API
- CURL
- Base64 编码
- Mermaid 流程图
- 吉卜力风格漫画风格

### 2. 复习上节课创建的视频脚本

提示词：

1. 请检查这个脚本，列出我需要掌握哪些知识点，以便能够大致理解这个脚本的内容。
2. 请检查提供的 Shell 脚本，说明如何使用它来创建有声视频。 请给出文字版步骤说明，并用 Mermaid 流程图展示。

Shell 脚本：[create_ebook_video.sh](../02-linux-ffmpeg/ai_output_zh_CN/create_ebook_video.sh)

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

AI 输出: [story.json](./ai_output_zh_CN/story.json)

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

关于如何调用 ffmpeg 命令，可以参考前面提供的 Shell 脚本。

> 原始 Linux 脚本文件：[文本链接](../02-linux-ffmpeg/ai_output_zh_CN/create_ebook_video.sh)

AI 输出: 1. [Google](ai_output_zh_CN/gemini/4.2.md) | 2. [Claude](ai_output_zh_CN/claude/4.2.md) | 3. [OpenAI](ai_output_zh_CN/chatgpt/4.2.md)

### 5. 要求AI评价三个不同AI生成的脚本

> 我有三个由不同 AI 生成的代码文件，应如何评估才能选出最优秀的那个？

请评价下面三个脚本从以下几个方面:

1. 正确性：功能需求是否全部满足？
2. 性能：运行时的速度和内存占用是否达标？
3. 可读性与可维护性：代码是否清晰易懂，便于后续扩展和调试？
4. 代码质量与风格：是否符合团队的编码规范，有无明显的坏味道？
5. 健壮性与错误处理：对无效输入或异常场景的处理是否完善？
6. 测试覆盖率：单元测试和集成测试是否齐全、充分？
7. 安全性：有无引入安全漏洞或不安全的编码模式？
8. 文档：是否有清晰的注释、docstring 或 README 来说明使用方法？

AI 输出: [Google](ai_output_zh_CN/gemini/5.md)

最终我们采用脚本: [文件](ai_output_zh_CN/generate_story_video.py)

### 6. 要求AI编写用户手册

> 如果要求AI对一个软件脚本编写用户手册， 我需要要求AI考虑哪些方面？

请对**下面的代码**， 编写一个用户手册， 考虑以下几个因素:

1. 目标和范围： 功能定位与业务背景， 目标用户， 使用场景及适用环境
2. 前置条件： 环境需求， 权限要求，配置项及默认值
3. 安装与部署
4. 使用说明
5. 错误处理与故障恢复
6. 安全与权限
7. 附录： 术语表， FAQ 常见问题

[文件](ai_output_zh_CN/generate_story_video.py)

AI 输出: [Google](ai_output_zh_CN/gemini/6.md)

### 7. 要求AI编写测试与验收流程

> 如果要求AI对一个软件脚本编写测试与验收流程， 我需要要求AI考虑哪些方面？

请对**下面的代码***， 编写一个测试与验收流程， 考虑以下几个因素:

1. 测试概述: 测试目标
2. 测试环境: 环境搭建, 数据准备
3. 测试类型与用例: 功能测试, 集成测试, 性能测试, 安全测试
4. 测试执行流程: 计划, 测试脚本或自动化框架, 结果与报告
5. 验收标准

[文件](ai_output_zh_CN/generate_story_video.py)

AI 输出: [Google](ai_output_zh_CN/gemini/7.md)

### 8. 要求AI对项目进行技术性总结

请对**下面的代码**使用的技术进行一个总结， 需要考虑以下几个因素:

1. 项目需求： 我们所要构建内容的高层概述：目标、用户故事、功能性和非功能性需求，以及验收标准。
2. 应用流程及流程图： 分步骤映射应用的用户旅程和系统交互，并配以清晰的流程图。
3. 技术栈概览： 说明技术选择的“为什么”和“什么”：语言、框架、库、云服务与工具，以及版本说明。
4. 前端与后端指南： 编码规范、架构模式、文件夹结构、API 协议约定、测试策略和风格规则——分别针对客户端和服务器端。
5. API、SDK 与技术参考 整合所有外部依赖：第三方 API、SDK、库和平台的目录，包含端点、版本号、配置示例和快速使用说明。

[文件](ai_output_zh_CN/generate_story_video.py)

AI 输出: [Google](ai_output_zh_CN/gemini/8.md)

### 9. 让AI给出氛围学习法需要学习的要点

我目前正在通过氛围学习法学习如何使用AI进行氛围编程，下面是关于氛围编程和氛围学习法的介绍：

- 氛围编程（Vibe Coding）：一种全新的编程方式，用户无需任何编程基础，仅需借助 AI 的能力，即可完成一个完整的编程项目。
- 氛围学习法（Vibe Learning）：聚焦掌握基础专业知识点，避开复杂细节，通过清晰的提示引导 AI 执行开发任务，让“不会写代码”的人也能开发项目。

目前我的的专业知识背景

- 仅具备基本的 Windows 使用能力  
- 对AI只有一点概念 
- 刚开始使用 GitHub  
- 刚开始使用 Linux 系统  
- 没有编程概念

请按照氛围学习法和氛围编程的要求，对**下面的代码**列出我需要学习哪些基本的知识点，我才能具备以下技能：

- 我可以用专业的语言给AI下达开发命令  
- 在AI开发过程中，我可以使用专业语言和AI进行沟通
- 我可以协助AI完成编码以外的手工任务
- 检查和测试AI完成的任务，并发现或提出问题

然后我可以轻松的使用AI完成这个项目。

[文件](ai_output_zh_CN/generate_story_video.py)

AI 输出: [Google](ai_output_zh_CN/gemini/9.md)