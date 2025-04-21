import openai
import json
import config

def generate_text(prompt, style="children_story"):
    """
    使用OpenAI的GPT模型生成视频场景的文本内容。
    
    参数:
        prompt (str): 用户的输入提示
        style (str): 内容风格 (children_story, poetry, english_learning, educational)
        
    返回:
        list: 场景字典列表，包含title, image_prompt, 和 narration
    """
    
    # 获取适当的样式模板
    style_template = config.STYLE_TEMPLATES.get(style, config.STYLE_TEMPLATES['children_story'])
    
    # 创建系统提示
    system_prompt = (
        "你是一个教育视频的创意内容生成器。"
        "你将创建分为多个场景的内容。"
        "将你的响应作为JSON数组返回，其中每个对象代表一个具有以下属性的场景：\n"
        "- title: 场景的简短标题\n"
        "- image_prompt: 用于生成图像的详细描述\n"
        "- narration: 在此场景中要叙述的文本"
    )
    
    # 创建用户提示
    user_prompt = (
        f"{style_template['text_prompt']} 基于这个主题: {prompt}\n\n"
        "将你的响应格式化为场景对象的JSON数组。"
    )
    
    # 调用OpenAI API
    openai.api_key = config.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=config.TEXT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    # 提取并解析内容
    content = response.choices[0].message.content
    try:
        parsed_content = json.loads(content)
        # 确保我们有预期的结构
        if 'scenes' in parsed_content:
            return parsed_content['scenes']
        else:
            return parsed_content
    except json.JSONDecodeError:
        # 如果JSON解析失败，回退到简单结构
        return [
            {
                "title": "错误场景",
                "image_prompt": "生成内容时出错",
                "narration": "生成内容时出错。请重试。"
            }
        ]
