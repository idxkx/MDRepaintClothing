import os
import torch
from transformers import (
    Blip2Processor,
    Blip2ForConditionalGeneration,
    AutoModelForCausalLM,
)
from janus.models import MultiModalityCausalLM, VLChatProcessor

def download_blip2_model(save_dir="models"):
    """下载并保存BLIP2模型
    
    Args:
        save_dir: 保存模型的目录
    """
    print("正在下载BLIP2模型...")
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
    
    os.makedirs(save_dir, exist_ok=True)
    blip2_path = os.path.join(save_dir, "blip2")
    processor.save_pretrained(os.path.join(blip2_path, "processor"))
    model.save_pretrained(os.path.join(blip2_path, "weights"))
    print("BLIP2模型下载完成!")

def download_janus_model(save_dir="models"):
    """下载并保存Janus-Pro-7B模型
    
    Args:
        save_dir: 保存模型的目录
    """
    print("正在下载Janus-Pro-7B模型...")
    model_path = "deepseek-ai/Janus-Pro-7B"
    
    # 初始化处理器和分词器
    vl_chat_processor = VLChatProcessor.from_pretrained(model_path)
    
    # 初始化模型
    vl_gpt = AutoModelForCausalLM.from_pretrained(
        model_path,
        trust_remote_code=True
    )
    
    # 如果有GPU则使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    vl_gpt = vl_gpt.to(torch.bfloat16).to(device).eval()
    
    # 保存模型和处理器
    os.makedirs(save_dir, exist_ok=True)
    janus_path = os.path.join(save_dir, "janus")
    vl_chat_processor.save_pretrained(os.path.join(janus_path, "processor"))
    vl_gpt.save_pretrained(os.path.join(janus_path, "weights"))
    print("Janus-Pro-7B模型下载完成!")

def verify_blip2_files():
    """验证BLIP2模型文件的完整性"""
    import os
    
    # 验证模型文件
    model_files = [
        "models/blip2/weights/config.json",
        "models/blip2/weights/generation_config.json",
        "models/blip2/weights/model.safetensors.index.json",
        "models/blip2/weights/model-00001-of-00004.safetensors",
        "models/blip2/weights/model-00002-of-00004.safetensors", 
        "models/blip2/weights/model-00003-of-00004.safetensors",
        "models/blip2/weights/model-00004-of-00004.safetensors"
    ]
    
    # 验证处理器文件
    processor_files = [
        "models/blip2/processor/processor_config.json",
        "models/blip2/processor/tokenizer.json",
        "models/blip2/processor/merges.txt",
        "models/blip2/processor/vocab.json",
        "models/blip2/processor/special_tokens_map.json",
        "models/blip2/processor/preprocessor_config.json",
        "models/blip2/processor/tokenizer_config.json"
    ]
    
    missing_files = []
    for file_path in model_files + processor_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("警告：以下BLIP2模型文件缺失：")
        for file in missing_files:
            print(f"- {file}")
        return False
    
    print("BLIP2模型文件完整性验证通过！")
    return True

def main():
    """下载所有需要的模型"""
    save_dir = "models"
    download_blip2_model(save_dir)
    download_janus_model(save_dir)
    print("所有模型下载完成!")
    
    # 验证BLIP2模型文件
    print("\n正在验证BLIP2模型文件...")
    verify_blip2_files()

if __name__ == "__main__":
    main()



# import torch
# print(torch.cuda.is_available()) 