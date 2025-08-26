#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小雨微寒个人网站后端服务
FastAPI + MySQL + Gunicorn
Author: XYWH
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from contextlib import asynccontextmanager

from app.database import engine, create_tables
from app.routers import food, movie, calendar, files


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建数据库表
    print("🚀 正在启动小雨微寒后端服务...")
    create_tables()
    print("✅ 数据库表初始化完成")
    yield
    # 关闭时清理资源
    print("🛑 正在关闭后端服务...")


# 创建FastAPI应用
app = FastAPI(
    title="小雨微寒个人网站API",
    description="记录美好时光的个人网站后端服务",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080", 
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://47.105.52.49",
        "https://47.105.52.49",
        "*"  # 开发阶段允许所有来源
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(food.router, prefix="/api", tags=["美食记录"])
app.include_router(movie.router, prefix="/api", tags=["电影记录"]) 
app.include_router(calendar.router, prefix="/api", tags=["日历备注"])
app.include_router(files.router, prefix="/api", tags=["文件管理"])


@app.get("/")
async def root():
    """根路径"""
    return {"message": "小雨微寒个人网站后端服务", "version": "2.0.0", "status": "running"}


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "message": "API服务运行正常",
        "version": "2.0.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"服务器内部错误: {str(exc)}",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    # 本地开发运行
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )