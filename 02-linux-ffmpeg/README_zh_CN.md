# Linux云容器与FFmpeg视频编辑软件

[English Version](README.md)

### 1. 氛围学习网络搜素关键词 （Google, YouTube or AI）

- 如何创建GitHub账号
- 如何使用GitHub Codespaces
- 什么是markdown格式文本
- 什么是TTS
- 如何使用视频编辑软件 FFmpeg


### 2. 免费海螺文字，声音，视频生成网站

- 文字 https://chat.minimax.io/
- 声音 https://www.minimax.io/audio/text-to-speech
- 视频 https://hailuoai.video/create

### 3. AI提示词 - 手工生成电子书视频的文本和图片AI提示词

我需要创建一个儿童电子书， 主题为： 小猫学习飞行
请按照以下“”“”和“”“”之间的 Markdown 格式输出内容

```markdown
""""
# 封面： 电子书名称

## 场景-1: 场景名称

### 场景-1 文字

场景-1 文字， 用于通过TTS生成电子书场景1的声音, 大约30个字左右

### 场景-1 图片

场景-1 图片AI提示词， 用于通过AI生成场景1的图片

## 场景-n: 场景名称

场景-n 文字， 用于通过TTS生成电子书场景n的声音, 大约30个字左右

### 场景-n 图片

场景-n 图片AI提示词， 用于通过AI生成场景n的图片
""""
```
请按照以上格式输出5个场景的电子书文字和图片AI提示词

AI 输出: [Google](ai_output_zh_CN/gemini/3.md) | [Claude](ai_output_zh_CN/claude/3.md) | [OpenAI](ai_output_zh_CN/chatgpt/3.md)

### 4. AI提示词 - 生成一个shell脚本， 使用FFmpeg生成电子书视频

我有五个图片，每一个图片对应一个mp3声音文件，请生成一个Linux Shell脚本， 使用ffmpeg生成一个电子书视频

AI 输出: [Google](ai_output_zh_CN/gemini/4.md) | [Claude](ai_output_zh_CN/claude/4.md) | [OpenAI](ai_output_zh_CN/chatgpt/4.md)

成功生成电子书视频的脚本：[create_ebook_video.sh](ai_output_zh_CN/create_ebook_video.sh)

### 5. AI提示词 - 用户手册及测试验收流程

对于这个Shell脚本， 请写一个用户手册及测试验收流程，以保证这个脚本在各种情况下都可以正常工作：

1. 在不同的 Linux 发行版本和环境下
2. 在不同的 Shell 环境下
3. 考虑不同的FFmpeg版本
4. 错误处理

AI 输出: [Google](ai_output_zh_CN/gemini/5.md) | [Claude](ai_output_zh_CN/claude/5.md) | [OpenAI](ai_output_zh_CN/chatgpt/5.md)

### 6. 要求AI对完成的工作进行总结

请简单总结一下这个Linux Shell脚本， 按下面的要点（仅总结适用部分）：

1. 项目需求 我们所要构建内容的高层概述：目标、用户故事、功能性和非功能性需求，以及验收标准。
2. 应用流程及流程图 分步骤映射应用的用户旅程和系统交互，并配以清晰的流程图。
3. 技术栈概览 说明技术选择的“为什么”和“什么”：语言、框架、库、云服务与工具，以及版本说明。
4. 前端与后端指南 编码规范、架构模式、文件夹结构、API 协议约定、测试策略和风格规则——分别针对客户端和服务器端。
5. API、SDK 与技术参考 整合所有外部依赖：第三方 API、SDK、库和平台的目录，包含端点、版本号、配置示例和快速使用说明。

AI 输出: [Google](ai_output_zh_CN/gemini/6.md) | [Claude](ai_output_zh_CN/claude/6.md) | [OpenAI](ai_output_zh_CN/chatgpt/6.md)

### 7. 让AI给出氛围学习法需要学习的要点

我目前正在通过氛围学习法学习如何使用AI进行氛围编程，下面是关于氛围编程和氛围学习法的介绍：

- 氛围编程（Vibe Coding）：一种全新的编程方式，用户无需任何编程基础，仅需借助 AI 的能力，即可完成一个完整的编程项目。
- 氛围学习法（Vibe Learning）：聚焦掌握基础专业知识点，避开复杂细节，通过清晰的提示引导 AI 执行开发任务，让“不会写代码”的人也能开发项目。

目前我的的专业知识背景

- 仅具备基本的 Windows 使用能力  
- 对AI只有一点概念 
- 刚开始使用 GitHub  
- 刚开始使用 Linux 系统  
- 完全没有编程概念
- 不清楚什么是编程语言  

对于在Linux下让AI撰写Shell脚本， 请按照氛围学习法和氛围编程的要求，列出我需要学习哪些基本的知识点，我才能具备一下技能：

- 我可以用专业的语言给AI下达开发命令  
- 在AI开发过程中，我可以使用专业语言和AI进行沟通
- 我可以协助AI完成编码以外的手工任务
- 检查和测试AI完成的任务，并发现或提出问题

然后我可以轻松的使用AI完成这个项目。

AI 输出: [Google](ai_output_zh_CN/gemini/7.md) | [Claude](ai_output_zh_CN/claude/7.md) | [OpenAI](ai_output_zh_CN/chatgpt/7.md)