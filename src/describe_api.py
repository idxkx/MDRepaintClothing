from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional, Dict
import logging
import os

# 你需要在config_loader.py或环境变量中配置API Key
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '请在环境变量中配置')
BLIP2_API_KEY = os.getenv('BLIP2_API_KEY', '请在环境变量中配置')

router = APIRouter()
logger = logging.getLogger('describe')

class DescribeRequest(BaseModel):
    image_path: str  # 原图路径
    segmented_path: str  # 去背景图路径
    model: str = 'deepseek'  # 'deepseek' or 'blip2'
    lang: str = 'zh'  # 'zh' or 'en'

# DeepSeek R1 Prompt模板
PROMPT_TEMPLATE = {
    'zh': "请只根据图片内容，详细描述图片中服装的款式、颜色、材质、细节和风格，不要描述背景、模特或其它无关内容。",
    'en': "Please describe only the clothing in the image, focusing on style, color, material, details, and fashion. Ignore the background, model, or any irrelevant elements."
}

# TODO: 实现图片转base64或url上传到API，视API支持情况而定

# BLIP2本地模型全局缓存
blip2_model = None
blip2_processor = None
blip2_device = None

def call_deepseek(image_path: str, lang: str) -> str:
    """
    调用DeepSeek R1 API，返回描述
    """
    import requests
    import base64
    with open(image_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    prompt = PROMPT_TEMPLATE[lang]
    # DeepSeek API兼容OpenAI格式
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"请描述这张服装图片：data:image/jpeg;base64,{img_b64}" if lang=='zh' else f"Describe this clothing image: data:image/jpeg;base64,{img_b64}"}
        ],
        "stream": False
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def call_blip2(image_path: str, lang: str) -> str:
    """
    本地推理BLIP2，返回服装描述
    """
    global blip2_model, blip2_processor, blip2_device
    import torch
    from PIL import Image
    from transformers import Blip2Processor, Blip2ForConditionalGeneration
    if blip2_model is None or blip2_processor is None or blip2_device is None:
        blip2_device = "cuda" if torch.cuda.is_available() else "cpu"
        blip2_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        blip2_model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16 if blip2_device=="cuda" else torch.float32
        )
        blip2_model.to(blip2_device)
    image = Image.open(image_path).convert('RGB')
    prompt = "请详细描述这件衣服。" if lang == 'zh' else "Describe this clothing in detail."
    inputs = blip2_processor(images=image, text=prompt, return_tensors="pt").to(blip2_device)
    generated_ids = blip2_model.generate(**inputs, max_new_tokens=128)
    description = blip2_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    return description

@router.post('/describe')
def describe(req: DescribeRequest):
    try:
        logger.info(f'收到描述请求: {req}')
        if req.model == 'deepseek':
            desc_origin = call_deepseek(req.image_path, req.lang)
            desc_segmented = call_deepseek(req.segmented_path, req.lang)
        elif req.model == 'blip2':
            desc_origin = call_blip2(req.image_path, req.lang)
            desc_segmented = call_blip2(req.segmented_path, req.lang)
        else:
            return {"success": False, "msg": "不支持的模型类型"}
        return {
            "success": True,
            "model": req.model,
            "lang": req.lang,
            "origin_desc": desc_origin,
            "segmented_desc": desc_segmented,
            "prompt": PROMPT_TEMPLATE[req.lang]
        }
    except Exception as e:
        logger.error(f'描述接口异常: {e}')
        return {"success": False, "msg": str(e)} 