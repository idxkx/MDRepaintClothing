import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

router = APIRouter()

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    print("=== upload_image called ===")
    # 不再限制扩展名和大小
    contents = await file.read()
    # 防止重名覆盖
    save_name = file.filename
    save_path = os.path.join(UPLOAD_DIR, save_name)
    i = 1
    while os.path.exists(save_path):
        name, ext = os.path.splitext(file.filename)
        save_name = f"{name}_{i}{ext}"
        save_path = os.path.join(UPLOAD_DIR, save_name)
        i += 1
    with open(save_path, "wb") as f:
        f.write(contents)
    # 返回图片访问URL（假设后续有静态文件服务）
    return JSONResponse({"success": True, "url": f"/api/image/{save_name}"})
