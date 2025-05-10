# prompt_engineering.py
"""
结构化服装描述提示词工程模块
"""

def generate_structured_prompt(lang='zh'):
    """
    根据语言生成结构化服装描述的专业提示词。
    :param lang: 'zh' 或 'en'
    :return: prompt字符串
    """
    if lang == 'zh':
        prompt = (
            "请只根据图片内容，详细、结构化地描述图片中服装的所有细节。请分条输出以下信息：\n"
            "1. 款式类型\n"
            "2. 剪裁与版型\n"
            "3. 部位结构（如领型、袖型、下摆、口袋等）\n"
            "4. 颜色（主色、辅色、拼色等）\n"
            "5. 材质/面料\n"
            "6. 图案与装饰\n"
            "7. 风格\n"
            "8. 适用场景\n"
            "9. 独特特征\n"
            "10. 其它你认为重要的细节\n"
            "最后请输出一句简明的整体描述。"
        )
    else:
        prompt = (
            "Please describe in detail and in a structured way all the details of the clothing in the image, based only on the image content. Please output the following information in order:\n"
            "1. Type\n"
            "2. Cutting and Fit\n"
            "3. Part Structure (e.g., collar, sleeve, hem, pocket, etc.)\n"
            "4. Color (main, secondary, color block, etc.)\n"
            "5. Material/Fabric\n"
            "6. Pattern and Decoration\n"
            "7. Style\n"
            "8. Occasion\n"
            "9. Unique Features\n"
            "10. Other important details you find\n"
            "Finally, provide a concise overall summary."
        )
    return prompt 