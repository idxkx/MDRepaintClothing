from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional, Dict
import logging
import os
from fastapi.responses import JSONResponse
from src.prompt_engineering import generate_structured_prompt

# 你需要在config_loader.py或环境变量中配置API Key
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '请在环境变量中配置')
BLIP2_API_KEY = os.getenv('BLIP2_API_KEY', '请在环境变量中配置')

router = APIRouter()
logger = logging.getLogger('describe')

class DescribeRequest(BaseModel):
    image_path: str  # 原图路径
    segmented_path: str  # 去背景图路径
    model: str = 'janus'  # 'janus' or 'blip2'
    lang: str = 'zh'  # 'zh' or 'en'

# DeepSeek R1 Prompt模板
PROMPT_TEMPLATE = {
    'zh': "请只根据图片内容，详细描述图片中服装的款式、颜色、材质、细节和风格，不要描述背景、模特或其它无关内容。",
    'en': "Please describe only the clothing in the image, focusing on style, color, material, details, and fashion. Ignore the background, model, or any irrelevant elements."
}

# TODO: 实现图片转base64或url上传到API，视API支持情况而定

# Janus多版本模型全局缓存
janus_models = {}

def call_janus(image_path: str, lang: str, prompt: str, version: str = "Janus-1.3B") -> str:
    global janus_models
    import torch
    from PIL import Image
    from transformers import AutoModelForCausalLM
    from janus.models import MultiModalityCausalLM, VLChatProcessor
    from janus.utils.io import load_pil_images
    import os
    import time

    print(f"[调试] Janus推理 | 图片路径: {image_path}, 是否存在: {os.path.exists(image_path)}")
    model_path_map = {
        "Janus-Pro-7B": "deepseek-ai/Janus-Pro-7B",
        "Janus-1.3B": "deepseek-ai/Janus-1.3B"
    }
    model_path = model_path_map.get(version, "deepseek-ai/Janus-1.3B")

    if version not in janus_models:
        processor = VLChatProcessor.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model = model.to(torch.bfloat16).cuda().eval()
        print(f"[调试] Janus模型当前设备: {model.device}")
        janus_models[version] = (processor, model)
    else:
        processor, model = janus_models[version]
        print(f"[调试] Janus模型当前设备: {model.device}")

    # 缩放图片到512x512，保存为临时文件
    pil_img = Image.open(image_path).convert('RGB')
    pil_img = pil_img.resize((512, 512))
    tmp_path = image_path + ".janus_tmp.jpg"
    pil_img.save(tmp_path)

    # 构造对话
    conversation = [
        {
            "role": "<|User|>",
            "content": f"<image_placeholder>\n{prompt}",
            "images": [tmp_path],
        },
        {"role": "<|Assistant|>", "content": ""},
    ]
    pil_images = load_pil_images(conversation)
    prepare_inputs = processor(
        conversations=conversation, images=pil_images, force_batchify=True
    ).to(model.device)
    inputs_embeds = model.prepare_inputs_embeds(**prepare_inputs)
    start = time.time()
    outputs = model.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepare_inputs.attention_mask,
        pad_token_id=processor.tokenizer.eos_token_id,
        bos_token_id=processor.tokenizer.bos_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        max_new_tokens=512,
        do_sample=False,
        use_cache=True,
    )
    answer = processor.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    print(f"[调试] Janus推理耗时: {time.time() - start:.2f}秒")
    print(f"[调试] Janus原始输出: {answer}")
    # 清理临时文件
    try:
        os.remove(tmp_path)
    except Exception:
        pass
    return answer

# BLIP2模型全局缓存
blip2_model = None
blip2_processor = None
blip2_device = None

def call_blip2(image_path: str, lang: str, prompt: str) -> str:
    global blip2_model, blip2_processor, blip2_device
    import torch
    from PIL import Image
    from transformers import Blip2Processor, Blip2ForConditionalGeneration
    import time
    import os
    if blip2_model is None or blip2_processor is None or blip2_device is None:
        blip2_device = "cuda" if torch.cuda.is_available() else "cpu"
        blip2_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        blip2_model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16 if blip2_device=="cuda" else torch.float32
        )
        blip2_model.to(blip2_device)
        print(f"[调试] BLIP2当前设备: {blip2_device}")
    print(f"[调试] BLIP2推理 | 图片路径: {image_path}, 是否存在: {os.path.exists(image_path)}")
    image = Image.open(image_path).convert('RGB')
    blip2_prompt = "Describe this clothing in detail."
    start = time.time()
    # 官方推荐方式：只用text和images
    inputs = blip2_processor(images=image, text=blip2_prompt, return_tensors="pt").to(blip2_device)
    generated_ids = blip2_model.generate(**inputs, max_new_tokens=128)
    description = blip2_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    print(f"[调试] BLIP2推理耗时: {time.time() - start:.2f}秒")
    print(f"[调试] BLIP2原始输出: {description}")
    return description

def call_model(image_path: str, lang: str, model: str, prompt: str, janus_version: str = "Janus-Pro-7B") -> str:
    if model == 'janus':
        return call_janus(image_path, lang, prompt, version=janus_version)
    elif model == 'blip2':
        return call_blip2(image_path, lang, prompt)
    else:
        raise ValueError('不支持的模型类型')

def parse_structured_description(desc_text: str, lang: str) -> dict:
    import re
    sections = []
    raw = ''
    if lang == 'zh':
        # Janus结构化分段解析
        label_map = [
            ('款式类型', '款式类型'),
            ('剪裁与版型', '剪裁与版型'),
            ('部位结构', '部位结构'),
            ('颜色', '颜色'),
            ('材质/面料', '材质/面料'),
            ('图案与装饰', '图案与装饰'),
            ('风格', '风格'),
            ('适用场景', '适用场景'),
            ('独特特征', '独特特征'),
            ('其它', '其它'),
        ]
        for label, key in label_map:
            m = re.search(rf'{label}[:：]\s*(.*)', desc_text)
            if m:
                sections.append({'label': label, 'value': m.group(1).strip()})
        m = re.search(r'整体描述[:：]\s*(.*)', desc_text)
        if m:
            raw = m.group(1).strip()
        # BLIP2输出为自然语言描述，无法结构化分段，仅填充raw
        if not sections and not raw and desc_text.strip():
            return {'sections': [], 'raw': desc_text.strip()}
    else:
        # 英文模式可扩展
        if desc_text.strip():
            return {'sections': [], 'raw': desc_text.strip()}
    return {'sections': sections, 'raw': raw}

@router.post('/describe')
def describe(req: DescribeRequest):
    try:
        logger.info(f'收到描述请求: {req}')
        print('image_path:', req.image_path)
        print('segmented_path:', req.segmented_path)
        print('model:', req.model)
        print('lang:', req.lang)
        # 生成结构化提示词
        prompt = generate_structured_prompt(req.lang)
        # 支持前端传递janus_version参数（如无则默认Pro-7B）
        janus_version = getattr(req, 'janus_version', 'Janus-Pro-7B')
        # 根据模型分发
        desc_origin = call_model(req.image_path, req.lang, req.model, prompt, janus_version=janus_version)
        desc_segmented = call_model(req.segmented_path, req.lang, req.model, prompt, janus_version=janus_version)
        # 结构化解析
        origin_struct = parse_structured_description(desc_origin, req.lang)
        segmented_struct = parse_structured_description(desc_segmented, req.lang)
        return JSONResponse(content={
            "success": True,
            "model": req.model,
            "lang": req.lang,
            "origin_desc": origin_struct,
            "segmented_desc": segmented_struct,
            "prompt": prompt,
            "janus_version": janus_version
        })
    except Exception as e:
        logger.error(f'描述接口异常: {e}')
        print('Exception:', repr(e))
        return JSONResponse(content={"success": False, "msg": str(e)})

if __name__ == "__main__":
    """
    本地调试入口，直接运行本文件即可测试Janus-Pro-7B和BLIP2推理效果。
    默认用tests/img/05.jpg作为原图和去背景图。
    """
    import os
    import sys
    import json
    # 假设图片已放在tests/img/05.jpg
    image_path = os.path.abspath("tests/img/05.jpg")
    segmented_path = image_path  # 如无分割图，直接用原图
    lang = "zh"
    prompt = generate_structured_prompt(lang)

    # Janus-1.3B
    # print("[调试] 开始Janus-1.3B推理...")
    # desc_origin_janus = call_model(image_path, lang, "janus", prompt, janus_version="Janus-1.3B")
    # desc_segmented_janus = call_model(segmented_path, lang, "janus", prompt, janus_version="Janus-1.3B")
    # origin_struct_janus = parse_structured_description(desc_origin_janus, lang)
    # segmented_struct_janus = parse_structured_description(desc_segmented_janus, lang)
    # print("[调试] Janus-1.3B 原图结构化描述:")
    # print(json.dumps(origin_struct_janus, ensure_ascii=False, indent=2))
    # print("[调试] Janus-1.3B 去背景图结构化描述:")
    # print(json.dumps(segmented_struct_janus, ensure_ascii=False, indent=2))

    # BLIP2
    print("\n[调试] 开始BLIP2推理...")

    desc_origin_blip2 = call_model(image_path, lang, "blip2", prompt)
    desc_segmented_blip2 = call_model(segmented_path, lang, "blip2", prompt)
    origin_struct_blip2 = parse_structured_description(desc_origin_blip2, lang)
    segmented_struct_blip2 = parse_structured_description(desc_segmented_blip2, lang)
    print("[调试] BLIP2 原图结构化描述:")
    print(json.dumps(origin_struct_blip2, ensure_ascii=False, indent=2))
    print("[调试] BLIP2 去背景图结构化描述:")
    print(json.dumps(segmented_struct_blip2, ensure_ascii=False, indent=2)) 