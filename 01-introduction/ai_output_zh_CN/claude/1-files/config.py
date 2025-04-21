import os

# OpenAI API 配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# 目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# 视频配置
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 30
SCENE_DURATION = 5  # 每个场景的秒数

# OpenAI 模型
TEXT_MODEL = "gpt-4"
SPEECH_MODEL = "tts-1"
IMAGE_MODEL = "dall-e-3"

# 样式模板（不同内容类型的提示）
STYLE_TEMPLATES = {
    'children_story': {
        'text_prompt': "创建一个包含5个场景的儿童故事。对于每个场景，提供标题、用于图像生成的描述和叙述文本。",
        'voice': 'alloy',
    },
    'poetry': {
        'text_prompt': "基于古典诗词创建一个包含5个场景的诗歌旅程。对于每个场景，提供标题、用于图像生成的描述和诗歌文本。",
        'voice': 'echo',
    },
    'english_learning': {
        'text_prompt': "创建一个包含5个场景的英语学习课程。对于每个场景，提供标题、用于图像生成的描述和教育内容。",
        'voice': 'nova',
    },
    'educational': {
        'text_prompt': "创建一个关于有趣主题的包含5个场景的教育演示。对于每个场景，提供标题、用于图像生成的描述和教育内容。",
        'voice': 'onyx',
    }
}
