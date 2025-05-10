from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from . import upload
from . import logging_config
from .segmentation_api import router as segmentation_router
from .describe_api import router as describe_router

app = FastAPI(title="MDRepaintClothing 后端API")

# 允许跨域（便于前端本地开发调试）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册图片上传路由
app.include_router(upload.router)

# 注册分割API路由
app.include_router(segmentation_router, prefix="/api")

# 注册服装描述API路由
app.include_router(describe_router, prefix="/api")

# 静态文件服务（图片访问）
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app.mount("/api/image", StaticFiles(directory=UPLOAD_DIR), name="image")


@app.get("/")
def root():
    return {"msg": "MDRepaintClothing 后端服务运行中"}
