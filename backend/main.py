from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import engine, Base
from app.routers import food, movie, calendar, files
from app.config import settings

# 加载环境变量
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 小雨微寒后端服务启动中...")
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建上传目录
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    print("✅ 后端服务启动完成！")
    yield
    # 关闭时执行
    print("📴 后端服务关闭")

# 创建FastAPI应用
app = FastAPI(
    title="小雨微寒 - Memory Backend",
    description="个人网站后端API服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(food.router, prefix="/api/food", tags=["美食记录"])
app.include_router(movie.router, prefix="/api/movie", tags=["电影记录"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["日历备注"])
app.include_router(files.router, prefix="/api/files", tags=["文件管理"])

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用小雨微寒 Memory 后端服务",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )