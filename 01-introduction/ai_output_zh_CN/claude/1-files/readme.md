# AI自动生成短视频项目

这是一个使用Python和Web技术构建的自动视频生成系统，它利用OpenAI的API来创建"有声图文电子书"式的短视频。

## 功能特点

- 基于用户提示词自动生成短视频内容
- 每个视频包含多个场景，每个场景都有文字、图像和配音
- 支持多种内容风格：儿童故事、古诗词、英语学习和教育知识
- 实时显示生成进度
- 视频生成完成后可直接在浏览器中播放
- 支持下载生成的视频

## 技术栈

### 后端
- Python
- Flask (Web框架)
- OpenAI API (用于文本、语音和图像生成)
- MoviePy (用于视频处理)
- Pillow (用于图像处理)

### 前端
- HTML5
- CSS3
- JavaScript (原生)

## 安装说明

1. 克隆此仓库：
```
git clone https://github.com/yourusername/auto-video-generator.git
cd auto-video-generator
```

2. 安装Python依赖：
```
pip install -r backend/requirements.txt
```

3. 设置OpenAI API密钥：
```
export OPENAI_API_KEY="your_api_key_here"
```

## 运行项目

1. 启动后端服务器：
```
cd backend
python app.py
```

2. 打开浏览器访问：
```
http://localhost:5000
```

## 使用方法

1. 在主页中输入你想要的视频内容提示词
2. 从下拉菜单中选择内容风格
3. 点击"生成视频"按钮
4. 等待视频生成完成（可以在进度条查看进度）
5. 生成完成后，视频将自动加载并可以播放
6. 可以使用"下载视频"按钮保存视频到本地

## 项目结构

```
auto-video-generator/
├── backend/
│   ├── app.py                 # Flask主应用
│   ├── config.py              # 配置设置
│   ├── requirements.txt       # Python依赖
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── text_generator.py  # OpenAI文本生成
│   │   ├── speech_generator.py # OpenAI语音合成
│   │   ├── image_generator.py # OpenAI图像生成
│   │   └── video_generator.py # 视频合成
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # 工具函数
├── frontend/
│   ├── index.html             # 主页面
│   ├── css/
│   │   └── styles.css         # 样式
│   └── js/
│       ├── main.js            # 主JavaScript逻辑
│       ├── api.js             # API交互
│       └── video-player.js    # 视频播放器功能
└── README.md                  # 项目文档
```

## 自定义与扩展

- 在`config.py`中可以自定义视频分辨率、帧率和其他设置
- 添加新的内容风格可以在`config.py`的`STYLE_TEMPLATES`字典中添加

## 许可证

MIT

## 贡献

欢迎提交问题报告和拉取请求！
