import os

import yaml
from dotenv import load_dotenv

# 加载.env文件（如果存在）
load_dotenv()

with open("./config/config_prod.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

PORT = int(os.getenv("PORT", config.get("port", 8000)))
MODEL_PATH = os.getenv("MODEL_PATH", config.get("model_path"))

# 其他配置可按需扩展
