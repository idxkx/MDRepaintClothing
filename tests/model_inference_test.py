import torch
from PIL import Image

# BLIP2 测试
try:
    from transformers import Blip2Processor, Blip2ForConditionalGeneration
    print("\n[BLIP2] 开始加载模型...")
    blip2_processor = Blip2Processor.from_pretrained("models/blip2/processor")
    blip2_model = Blip2ForConditionalGeneration.from_pretrained("models/blip2/weights")
    blip2_model.eval()
    print("[BLIP2] 模型加载成功！")
    image = Image.open("tests/img/05.jpg")
    inputs = blip2_processor(image, return_tensors="pt")
    with torch.no_grad():
        output = blip2_model.generate(**inputs, max_length=50)
    description = blip2_processor.decode(output[0], skip_special_tokens=True)
    print(f"[BLIP2] 图片描述结果：{description}")
except Exception as e:
    print(f"[BLIP2] 测试失败：{e}")

# Janus 测试
try:
    from transformers import AutoModelForCausalLM
    from janus.models import VLChatProcessor
    print("\n[Janus] 开始加载模型...")
    janus_processor = VLChatProcessor.from_pretrained("models/janus/processor")
    janus_tokenizer = janus_processor.tokenizer
    janus_model = AutoModelForCausalLM.from_pretrained(
        "models/janus/weights",
        trust_remote_code=True
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    janus_model = janus_model.to(torch.bfloat16).to(device).eval()
    print("[Janus] 模型加载成功！")
    # 构造对话
    conversation = [
        {
            "role": "<|User|>",
            "content": "描述这件衣服的细节",
            "images": [Image.open("tests/img/05.jpg")],
        },
        {"role": "<|Assistant|>", "content": ""},
    ]
    pil_images = [conv["images"][0] for conv in conversation if "images" in conv]
    prepare_inputs = janus_processor(
        conversations=conversation,
        images=pil_images,
        force_batchify=True
    ).to(device)
    inputs_embeds = janus_model.prepare_inputs_embeds(**prepare_inputs)
    outputs = janus_model.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepare_inputs.attention_mask,
        pad_token_id=janus_tokenizer.eos_token_id,
        bos_token_id=janus_tokenizer.bos_token_id,
        eos_token_id=janus_tokenizer.eos_token_id,
        max_new_tokens=128,
        do_sample=False,
        use_cache=True,
    )
    answer = janus_tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    print(f"[Janus] 图片描述结果：{answer}")
except Exception as e:
    print(f"[Janus] 测试失败：{e}") 