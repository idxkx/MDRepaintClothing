"""
结构化服装描述Prompt模板模块
支持中英文，便于后续扩展和自定义。
"""

PROMPT_TEMPLATES = {
    'en': (
        "Please describe only the clothing in the image in a detailed and structured way, focusing on: "
        "1. Garment type (e.g., T-shirt, dress, coat, etc.)\n"
        "2. Cut and fit (e.g., long/short sleeves, long/short pants, slim/loose fit, special structure, etc.)\n"
        "3. Colors of each part (e.g., main body, sleeves, collar, hem, pockets—specify the color of each part)\n"
        "4. Material/fabric (e.g., cotton, linen, silk, denim, leather, etc.)\n"
        "5. Key details (e.g., patterns, prints, embroidery, stripes, buttons, zippers, pockets, collar type, etc.)\n"
        "6. Style and occasion (e.g., casual, business, sports, vintage, formal, etc.)\n"
        "7. Any unique features\n"
        "Format your answer as a single, detailed sentence suitable for use as a text-to-image generation prompt. "
        "Do not mention background, model, or irrelevant elements."
    ),
    'zh': (
        "请只根据图片内容，详细、结构化地描述服装的以下方面：\n"
        "1. 款式类型（如T恤、连衣裙、大衣等）\n"
        "2. 剪裁与版型（如长/短袖、长/短裤、修身/宽松、特殊结构等）\n"
        "3. 各部位颜色（如主体、袖子、领口、下摆、口袋等分别是什么颜色）\n"
        "4. 材质/面料（如棉、麻、丝绸、牛仔、皮革等）\n"
        "5. 关键细节（如图案、印花、刺绣、条纹、纽扣、拉链、口袋、领型等）\n"
        "6. 风格与适用场景（如休闲、商务、运动、复古、正式等）\n"
        "7. 任何独特特征\n"
        "请将答案整理为一条完整、详细的句子，适合作为AI文生图的提示词。不要描述背景、模特或无关内容。"
    )
}

def get_prompt_template(lang='en'):
    """
    获取指定语言的结构化服装描述Prompt模板。
    :param lang: 'en' 或 'zh'
    :return: prompt字符串
    """
    return PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES['en']) 