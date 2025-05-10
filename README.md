# MDRepaintClothing

## 项目简介
MDRepaintClothing 是一个本地可用的服装图片重绘与生成平台，支持服装图片上传、自动抠图、服装细节描述、多模型文生图生成、图片对比与历史追溯，便于服装设计、分析与创新。

## 功能概述
- 上传服装图片（支持 jpg、png、webp）
- 自动扣除背景（可选，支持多种分割模型）
- 自动生成服装细节描述（支持中英文，多模型）
- 根据描述生成新服装图片（多模型，参数可调）
- 图片对比（原图、分割图、描述生成图）
- 历史记录与追溯
- 日志记录与报错追踪
- 前端参数动态调整，参数含义说明

## 技术架构
- 前端：React + TailwindCSS
- 后端：Python + FastAPI
- 支持本地 GPU 推理（Nvidia 5070ti/4090）和外部 API 调用
- 日志分级，存储于 logs/ 目录

## 使用方法
1. 启动后端服务（FastAPI）
2. 启动前端服务（React）
3. 上传服装图片，选择模型，调整参数，生成并对比图片
4. 查看历史记录与日志

## 目录结构
- /frontend 前端代码
- /backend 后端代码
- /logs 日志文件
- /config 配置文件
- /history 历史记录
- /docs 文档
- /models 模型文件
  - /blip2 BLIP2模型文件
    - /weights 模型权重文件
    - /processor 处理器配置文件
  - /janus Janus模型文件
    - /weights 模型权重文件
    - /processor 处理器配置文件

## 参数说明
- 不同模型支持不同参数，前端会动态展示并有详细说明
- 所有参数调整均会影响生成效果，建议多尝试对比

## 常见问题
- 报错信息会自动记录在 logs/ 目录下
- 如需添加新模型，请参考 /backend/models/ 目录结构，独立实现接口和代码文件

## 联系方式
如有问题或建议，请通过 issues 反馈

## 技术选型

| 领域         | 选型                | 说明/理由                         |
|--------------|---------------------|-----------------------------------|
| Python依赖   | pip + requirements.txt | 传统、简单、兼容性好              |
| 前端包管理   | npm                 | 官方、最常用                      |
| 代码风格     | 可选 flake8/eslint  | 初期可不集成                      |
| 自动化测试   | pytest              | 主流、易用                        |
| CI/CD        | GitHub Actions      | 免费、易用                        |
| 安全扫描     | 暂不需要            | 记为技术债务                      |
| 环境变量     | .env 文件           | 简单易用                          |
| 数据库       | sqlite              | 轻量级、零配置                    |
| 缓存         | 暂不需要            |                                   |
| API文档      | FastAPI自带Swagger/ReDoc | 自动生成、易用                   |
| UI组件库     | TailwindCSS         | 原子化CSS，灵活高效               |

## 技术债务与后续优化建议

- 依赖安全扫描与锁定（如 pip-audit、npm audit）暂未集成，后续可根据需要补充。
- 代码风格与质量工具（如 flake8、eslint）暂未强制，后续如需团队协作可补充。
- 缓存方案（如 redis）暂未集成，后续如有性能瓶颈可考虑。
- 前端已去除图片大小限制，后端和服务器资源仍有限制，建议后续根据实际需求完善大文件处理策略（如分片上传、后端限流、压缩等）。

## 基础环境与工程脚手架说明

本项目已集成标准Python工程基础环境，适合个人和团队协作开发。

### 1. 依赖管理
- 推荐使用 [poetry](https://python-poetry.org/) 统一管理依赖，配置见 pyproject.toml
- 兼容 pip 用户，提供 requirements.txt

### 2. 目录结构
- src/         主代码目录
- tests/       自动化测试用例
- logs/        日志文件目录
- config/      配置文件（开发/生产）
- .github/workflows/  CI配置

### 3. 代码规范与提交钩子
- 集成 flake8、isort 代码规范工具
- 预置 pre-commit 钩子，提交前自动检查代码风格
- 配置见 .pre-commit-config.yaml

### 4. 自动化测试
- 使用 pytest 作为测试框架
- 示例测试见 tests/test_sample.py
- 集成 coverage 追踪测试覆盖率

### 5. 持续集成（CI）
- 使用 GitHub Actions 自动化测试
- 配置见 .github/workflows/ci.yml

### 6. 日志与配置
- 日志统一输出至 logs/ 目录
- config/ 目录下区分开发与生产环境配置

### 7. 快速开始
```bash
# 安装poetry
pip install poetry
# 安装依赖
poetry install
# 运行测试
poetry run pytest
# 代码风格检查
poetry run flake8 src/
# 预提交钩子安装
poetry run pre-commit install
```

如需自定义配置，请参考 config/ 目录下的模板文件。

## 配置与环境变量（仅生产环境）

- 所有配置均以生产环境为准，配置文件为 config/config_prod.yaml
- 可选用 .env 文件灵活调整端口、模型路径等参数
- 代码优先读取环境变量（.env），无则用配置文件默认值

示例 .env：
```
PORT=8000
MODEL_PATH=./models/prod/
```

示例 config/config_prod.yaml：
```
app_name: MDRepaintClothing
log_level: INFO
model_path: ./models/prod/
port: 8000
```

## 图片上传接口说明

### 1. 上传图片
- 路径：POST /api/upload-image
- 参数：form-data，字段名 file，类型为图片（jpg/png/webp，最大5MB）
- 返回：
  - success: 是否成功
  - url: 图片访问路径（如 /api/image/xxx.jpg）
  - error: 错误信息（如有）

### 2. 访问图片
- 通过返回的url字段直接访问图片，如 http://localhost:8000/api/image/xxx.jpg

### 3. 示例
- curl命令上传：
  curl -F "file=@你的图片路径.jpg" http://localhost:8000/api/upload-image 

## 前端目录与初始化说明

- 前端代码建议放在 /frontend 目录下
- 推荐使用 create-react-app 或 Vite 快速初始化
- 进入 frontend 目录后，运行 npm install 安装依赖
- 启动开发服务器：npm start

目录结构示例：
/frontend
  └── src
      └── components
          └── ImageUploader.jsx
      └── App.jsx
  └── package.json
  └── ...

如无 frontend 目录，请先在项目根目录执行：
npx create-react-app frontend
或
npm create vite@latest frontend -- --template react 

## 1. 图片上传与预览模块（已完成 ✅）
- 用户可上传 jpg/png/webp 格式图片，支持本地预览与后端存储。
- 上传成功后可直接预览后端返回的正式图片。
- 错误处理完善，体验流畅。

### 反思与后续建议
- 代码结构清晰，便于维护和扩展。
- 可平滑扩展多图上传、进度条、图片压缩等功能。
- 建议后续开发时保持接口风格和用户体验一致。 

## 图像分割（抠图）模块

### 功能简介
- 支持服装图片自动抠图，去除背景，仅保留衣物区域
- 支持U^2-Net分割模型（可扩展）
- 分割参数可调（前景阈值、细节保留），参数含义有中文说明
- 分割结果可与原图对比，支持前端滑块对比
- 日志分级，分割日志单独存储于logs/segmentation.log
- 完善的异常处理与测试用例

### 后端接口
- 路径：`POST /api/segment`
- 参数：
  - image_path: 图片路径（字符串）
  - threshold: 前景阈值（0-1，默认0.5）
  - detail: 细节保留程度（0-1，默认0.7）
  - model: 分割模型（默认u2net）
- 返回：
  - success: 是否成功
  - segmented_path: 分割后图片路径（成功时）
  - msg: 错误信息（失败时）

### 参数说明
| 参数名     | 说明           | 默认值 | 备注           |
|------------|----------------|--------|----------------|
| model      | 分割模型       | u2net  | 可扩展         |
| threshold  | 前景阈值       | 0.5    | 0-1 浮点数     |
| detail     | 细节保留程度   | 0.7    | 0-1 浮点数     |

### 日志
- 分割相关日志存储于 logs/segmentation.log

### 测试方法
- 进入项目根目录，运行：
  ```bash
  pytest tests/test_segmentation.py --maxfail=1 --disable-warnings -v
  ```
- 测试覆盖模型加载、推理、异常分支 

## 服装细节描述模块

### 接口说明
- 路径：`POST /api/describe`
- 功能：对上传的服装原图和去背景图分别生成AI描述，支持BLIP2和DeepSeek R1模型，支持中英文。

#### 请求参数
| 参数名         | 类型   | 说明                       |
| --------------| ------ | -------------------------- |
| image_path    | str    | 服装原图路径               |
| segmented_path| str    | 去背景图路径               |
| model         | str    | 'deepseek' 或 'blip2'      |
| lang          | str    | 'zh'（中文）或 'en'（英文）|

#### 返回参数
| 参数名         | 类型   | 说明                       |
| --------------| ------ | -------------------------- |
| success       | bool   | 是否成功                   |
| model         | str    | 使用的模型                 |
| lang          | str    | 语言                       |
| origin_desc   | str    | 原图AI描述                 |
| segmented_desc| str    | 去背景图AI描述             |
| prompt        | str    | 使用的提示词（Prompt）     |
| msg           | str    | 错误信息（失败时）         |

#### 使用方法
1. 上传服装图片，获取图片路径
2. 进行抠图，获取去背景图片路径
3. 选择模型和语言，调用`/api/describe`接口
4. 前端展示原图和去背景图的两组描述

#### DeepSeek R1提示词工程
- 中文：请只根据图片内容，详细描述图片中服装的款式、颜色、材质、细节和风格，不要描述背景、模特或其它无关内容。
- 英文：Please describe only the clothing in the image, focusing on style, color, material, details, and fashion. Ignore the background, model, or any irrelevant elements. 

## 模型下载与使用

### 模型下载
项目使用了两个主要模型：BLIP2和Janus-Pro-7B。可以通过以下步骤下载模型：

1. 安装依赖：
```bash
# 克隆Janus代码库（必需）
git clone https://github.com/deepseek-ai/Janus.git
cd Janus
pip install -e .
cd ..

# 安装其他依赖
pip install torch transformers accelerate
```

2. 运行下载脚本：
```bash
python download_models.py
```

下载的模型将保存在项目根目录的 `models/` 目录下：
- `models/blip2/`: BLIP2模型文件
  - `processor/`: BLIP2处理器
  - `model/`: BLIP2模型
- `models/janus/`: Janus-Pro-7B模型文件
  - `processor/`: Janus处理器
  - `model/`: Janus模型

### Windows系统下查找模型位置
在Windows系统中，如果您在E盘的projects目录下克隆了项目，模型文件的完整路径应该是：
```
E:\projects\MDRepaintClothing\models\blip2\processor  # BLIP2处理器
E:\projects\MDRepaintClothing\models\blip2\model     # BLIP2模型
E:\projects\MDRepaintClothing\models\janus\processor # Janus处理器
E:\projects\MDRepaintClothing\models\janus\model    # Janus模型
```

您可以通过以下步骤确认模型是否下载成功：
1. 打开文件资源管理器
2. 导航到项目所在目录（例如：E:\projects\MDRepaintClothing）
3. 查看 models 文件夹是否存在
4. 检查 models 文件夹下是否有 blip2 和 janus 两个子文件夹
5. 每个子文件夹中应该都有 processor 和 model 两个目录

如果看不到这些文件夹，请检查：
1. 下载脚本是否执行成功（没有报错）
2. 是否在正确的目录下运行了下载脚本
3. 磁盘空间是否充足（需要约25GB空间）

### 模型使用示例

#### 1. BLIP2模型（图片描述生成）
```python
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image

# 加载模型
processor = Blip2Processor.from_pretrained("models/blip2/processor")
model = Blip2ForConditionalGeneration.from_pretrained("models/blip2/model")

# 处理图片
image = Image.open("path_to_your_image.jpg")
inputs = processor(image, return_tensors="pt")

# 生成描述
outputs = model.generate(**inputs, max_length=50)
description = processor.decode(outputs[0], skip_special_tokens=True)
print(description)
```

#### 2. Janus-Pro-7B模型（多模态理解与生成）
```python
import torch
from transformers import AutoModelForCausalLM
from janus.models import MultiModalityCausalLM, VLChatProcessor
from PIL import Image

# 加载模型
vl_chat_processor = VLChatProcessor.from_pretrained("models/janus/processor")
tokenizer = vl_chat_processor.tokenizer

vl_gpt = AutoModelForCausalLM.from_pretrained(
    "models/janus/model",
    trust_remote_code=True
)

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vl_gpt = vl_gpt.to(torch.bfloat16).to(device).eval()

# 准备对话
conversation = [
    {
        "role": "<|User|>",
        "content": "描述这件衣服的细节",
        "images": [Image.open("path_to_your_image.jpg")],
    },
    {"role": "<|Assistant|>", "content": ""},
]

# 处理输入
pil_images = [conv["images"][0] for conv in conversation if "images" in conv]
prepare_inputs = vl_chat_processor(
    conversations=conversation,
    images=pil_images,
    force_batchify=True
).to(device)

# 生成回复
inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)
outputs = vl_gpt.language_model.generate(
    inputs_embeds=inputs_embeds,
    attention_mask=prepare_inputs.attention_mask,
    pad_token_id=tokenizer.eos_token_id,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
    max_new_tokens=512,
    do_sample=False,
    use_cache=True,
)

# 解码输出
answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
print(answer)
```

### 注意事项
1. 确保有足够的磁盘空间（约25GB）用于存储模型
2. 推荐使用GPU进行推理，最小显存要求：
   - BLIP2: 8GB
   - Janus-Pro-7B: 16GB
3. 首次运行时会自动下载模型，请确保网络连接稳定
4. 如遇到CUDA相关错误，请检查CUDA版本与PyTorch版本是否匹配 