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