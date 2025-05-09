import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

router = APIRouter()

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)


def allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@router.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="仅支持jpg/png/webp格式图片")
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过5MB")
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
