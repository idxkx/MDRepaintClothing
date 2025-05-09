@echo off
REM 启动后端FastAPI服务
start cmd /k "poetry run uvicorn src.main:app --reload --port 8000"
REM 启动前端React开发服务器
cd frontend
start cmd /k "npm start"
cd ..

echo ==============================
echo 前后端启动中，请稍候...
echo 后端: http://localhost:8000/docs 