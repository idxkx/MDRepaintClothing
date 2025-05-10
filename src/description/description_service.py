"""
服装描述生成服务
- 自动拼接结构化Prompt
- 支持BLIP2和Janus模型
- 支持中英文
"""
import torch
from PIL import Image
from .prompt_templates import get_prompt_template

# BLIP2推理
from transformers import Blip2Processor, Blip2ForConditionalGeneration
# Janus推理
from transformers import AutoModelForCausalLM
try:
    from janus.models import VLChatProcessor
    JANUS_AVAILABLE = True
except ImportError:
    JANUS_AVAILABLE = False

def generate_description(image_path, model_name='blip2', lang='en'):
    """
    生成结构化服装描述
    :param image_path: 图片路径
    :param model_name: 'blip2' 或 'janus'
    :param lang: 'en' 或 'zh'
    :return: 结构化描述字符串
    """
    prompt = get_prompt_template(lang)
    image = Image.open(image_path)
    if model_name == 'blip2':
        processor = Blip2Processor.from_pretrained("models/blip2/processor")
        model = Blip2ForConditionalGeneration.from_pretrained("models/blip2/weights")
        model.eval()
        # 拼接prompt与图片
        inputs = processor(image, prompt, return_tensors="pt")
        with torch.no_grad():
            output = model.generate(**inputs, max_length=80)
        description = processor.decode(output[0], skip_special_tokens=True)
        return description
    elif model_name == 'janus' and JANUS_AVAILABLE:
        processor = VLChatProcessor.from_pretrained("models/janus/processor")
        tokenizer = processor.tokenizer
        model = AutoModelForCausalLM.from_pretrained(
            "models/janus/weights",
            trust_remote_code=True
        )
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(torch.bfloat16).to(device).eval()
        # 构造对话
        conversation = [
            {
                "role": "<|User|>",
                "content": prompt,
                "images": [image],
            },
            {"role": "<|Assistant|>", "content": ""},
        ]
        pil_images = [conv["images"][0] for conv in conversation if "images" in conv]
        prepare_inputs = processor(
            conversations=conversation,
            images=pil_images,
            force_batchify=True
        ).to(device)
        inputs_embeds = model.prepare_inputs_embeds(**prepare_inputs)
        outputs = model.language_model.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=prepare_inputs.attention_mask,
            pad_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            max_new_tokens=128,
            do_sample=False,
            use_cache=True,
        )
        answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
        return answer
    else:
        raise ValueError(f"不支持的模型名: {model_name} 或 Janus依赖未安装") 