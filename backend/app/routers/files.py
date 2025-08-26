# -*- coding: utf-8 -*-
"""
文件管理API路由
"""

import os
import uuid
import shutil
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database import get_db
from app.models import FileRecord as FileRecordModel
from app.schemas import (
    FileRecord, FileRecordUpdate,
    BaseResponse, PaginatedResponse, StatsResponse
)
from app.config import settings

router = APIRouter()


def get_file_type(filename: str) -> str:
    """根据文件扩展名获取文件类型"""
    ext = os.path.splitext(filename)[1].lower()
    
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
    video_exts = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']
    audio_exts = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']
    document_exts = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']
    archive_exts = ['.zip', '.rar', '.7z', '.tar', '.gz']
    
    if ext in image_exts:
        return "图片"
    elif ext in video_exts:
        return "视频"
    elif ext in audio_exts:
        return "音频"
    elif ext in document_exts:
        return "文档"
    elif ext in archive_exts:
        return "压缩包"
    else:
        return "其他"


def generate_unique_filename(original_filename: str) -> str:
    """生成唯一的文件名"""
    name, ext = os.path.splitext(original_filename)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name


@router.get("/files", response_model=PaginatedResponse)
async def get_file_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    file_type: Optional[str] = Query(None, description="文件类型筛选"),
    category: Optional[str] = Query(None, description="分类筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取文件记录列表"""
    try:
        # 构建查询
        query = db.query(FileRecordModel)
        
        # 文件类型筛选
        if file_type:
            query = query.filter(FileRecordModel.file_type == file_type)
        
        # 分类筛选
        if category:
            query = query.filter(FileRecordModel.category == category)
        
        # 关键词搜索
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (FileRecordModel.original_filename.like(search_term)) |
                (FileRecordModel.description.like(search_term))
            )
        
        # 总数统计
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        files = query.order_by(desc(FileRecordModel.created_at)).offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            message="获取文件列表成功",
            data=[FileRecord.from_orm(file) for file in files],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


@router.post("/files/upload", response_model=BaseResponse)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    custom_category: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """上传文件"""
    try:
        # 检查文件大小
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413, 
                detail=f"文件大小超过限制({settings.max_file_size / 1024 / 1024:.1f}MB)"
            )
        
        # 生成唯一文件名
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(settings.upload_dir, unique_filename)
        
        # 确保上传目录存在
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        file_type = get_file_type(file.filename)
        
        # 创建文件记录
        file_record = FileRecordModel(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            mime_type=file.content_type,
            description=description,
            category=custom_category,
            is_public=False  # 默认私有
        )
        
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        return BaseResponse(
            success=True,
            message="文件上传成功",
            data=FileRecord.from_orm(file_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        # 如果数据库操作失败，删除已上传的文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.get("/files/{file_id}", response_model=BaseResponse)
async def get_file_record(
    file_id: int,
    db: Session = Depends(get_db)
):
    """获取文件记录详情"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件记录不存在")
        
        return BaseResponse(
            success=True,
            message="获取文件记录成功",
            data=FileRecord.from_orm(file_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件记录失败: {str(e)}")


@router.put("/files/{file_id}", response_model=BaseResponse)
async def update_file_info(
    file_id: int,
    file_data: FileRecordUpdate,
    db: Session = Depends(get_db)
):
    """更新文件信息"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件记录不存在")
        
        # 更新字段
        update_data = file_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(file_record, field, value)
        
        db.commit()
        db.refresh(file_record)
        
        return BaseResponse(
            success=True,
            message="文件信息更新成功",
            data=FileRecord.from_orm(file_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新文件信息失败: {str(e)}")


@router.delete("/files/{file_id}", response_model=BaseResponse)
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """删除文件"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件记录不存在")
        
        # 删除物理文件
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 删除数据库记录
        db.delete(file_record)
        db.commit()
        
        return BaseResponse(
            success=True,
            message="文件删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")


@router.get("/files/download/{file_id}")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """下载文件"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        if not os.path.exists(file_record.file_path):
            raise HTTPException(status_code=404, detail="文件已被删除")
        
        # 更新下载次数
        file_record.download_count += 1
        db.commit()
        
        return FileResponse(
            path=file_record.file_path,
            filename=file_record.original_filename,
            media_type=file_record.mime_type
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}")


@router.get("/files/stats/summary", response_model=BaseResponse)
async def get_file_stats(db: Session = Depends(get_db)):
    """获取文件统计"""
    try:
        # 总数统计
        total_count = db.query(FileRecordModel).count()
        
        # 最近30天统计
        from datetime import timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = db.query(FileRecordModel).filter(
            FileRecordModel.created_at >= thirty_days_ago
        ).count()
        
        # 文件类型统计
        type_stats = db.query(
            FileRecordModel.file_type,
            func.count(FileRecordModel.id).label('count'),
            func.sum(FileRecordModel.file_size).label('total_size')
        ).filter(
            FileRecordModel.file_type.isnot(None)
        ).group_by(FileRecordModel.file_type).all()
        
        categories = [
            {
                "name": stat[0] or "未知类型", 
                "count": stat[1],
                "size": stat[2] or 0
            } 
            for stat in type_stats
        ]
        
        # 总存储大小
        total_size = db.query(func.sum(FileRecordModel.file_size)).scalar() or 0
        
        # 月度统计
        monthly_stats = db.query(
            func.date_format(FileRecordModel.created_at, '%Y-%m').label('month'),
            func.count(FileRecordModel.id).label('count')
        ).group_by('month').order_by('month').limit(12).all()
        
        monthly_data = [
            {"month": month[0], "count": month[1]} 
            for month in monthly_stats
        ]
        
        stats = StatsResponse(
            total_count=total_count,
            recent_count=recent_count,
            categories=categories,
            monthly_data=monthly_data
        )
        
        return BaseResponse(
            success=True,
            message="获取文件统计成功",
            data={
                **stats.dict(),
                "total_size": total_size,
                "total_size_mb": round(total_size / 1024 / 1024, 2)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件统计失败: {str(e)}")