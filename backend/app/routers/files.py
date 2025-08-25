from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
import mimetypes
from ..database import get_db
from ..models import FileRecord as FileRecordModel
from ..schemas import FileRecord, FileRecordCreate, FileRecordUpdate, ResponseBase, ListResponse
from ..config import settings

router = APIRouter()

def get_file_category(filename: str) -> str:
    """根据文件扩展名判断分类"""
    ext = Path(filename).suffix.lower()
    
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'}
    document_exts = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.rtf'}
    audio_exts = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'}
    video_exts = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'}
    archive_exts = {'.zip', '.rar', '.7z', '.tar', '.gz'}
    
    if ext in image_exts:
        return 'image'
    elif ext in document_exts:
        return 'document'
    elif ext in audio_exts:
        return 'audio'
    elif ext in video_exts:
        return 'video'
    elif ext in archive_exts:
        return 'archive'
    else:
        return 'other'

def validate_file(file: UploadFile) -> tuple[bool, str]:
    """验证文件"""
    # 检查文件大小
    if hasattr(file, 'size') and file.size > settings.MAX_FILE_SIZE:
        return False, f"文件大小超过限制({settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB)"
    
    # 检查文件扩展名
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions_list:
        return False, f"不支持的文件类型: {file_ext}"
    
    return True, "文件验证通过"

async def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """保存上传的文件"""
    # 生成唯一文件名
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    
    # 创建目录结构 (按类型分类)
    category = get_file_category(file.filename)
    upload_dir = Path(settings.UPLOAD_DIR) / category
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / unique_filename
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path), unique_filename

@router.get("/", response_model=ListResponse)
async def get_file_records(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    category: Optional[str] = Query(None, description="文件分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方式"),
    db: Session = Depends(get_db)
):
    """获取文件记录列表"""
    try:
        query = db.query(FileRecordModel)
        
        # 按分类过滤
        if category:
            query = query.filter(FileRecordModel.category == category)
        
        # 搜索功能
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                FileRecordModel.filename.like(search_pattern) |
                FileRecordModel.original_filename.like(search_pattern) |
                FileRecordModel.description.like(search_pattern)
            )
        
        # 排序
        if hasattr(FileRecordModel, sort_by):
            order_column = getattr(FileRecordModel, sort_by)
            if sort_order == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        # 分页
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        
        return ListResponse(
            success=True,
            message="获取文件列表成功",
            data=[{
                "id": record.id,
                "filename": record.filename,
                "original_filename": record.original_filename,
                "file_path": record.file_path,
                "file_size": record.file_size,
                "file_type": record.file_type,
                "category": record.category,
                "description": record.description,
                "download_url": f"/api/files/download/{record.id}",
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            } for record in records],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")

@router.post("/upload", response_model=ResponseBase)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    custom_category: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """上传文件"""
    try:
        # 验证文件
        is_valid, message = validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # 保存文件
        file_path, unique_filename = await save_uploaded_file(file)
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        file_type = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        category = custom_category or get_file_category(file.filename)
        
        # 创建数据库记录
        db_file = FileRecordModel(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            category=category,
            description=description
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return ResponseBase(
            success=True,
            message="文件上传成功",
            data={
                "id": db_file.id,
                "filename": db_file.filename,
                "original_filename": db_file.original_filename,
                "file_size": db_file.file_size,
                "file_type": db_file.file_type,
                "category": db_file.category,
                "description": db_file.description,
                "download_url": f"/api/files/download/{db_file.id}",
                "created_at": db_file.created_at.isoformat()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        # 删除已上传的文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    """下载文件"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件未找到")
        
        if not os.path.exists(file_record.file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=file_record.file_path,
            filename=file_record.original_filename,
            media_type=file_record.file_type
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}")

@router.get("/{file_id}", response_model=ResponseBase)
async def get_file_info(file_id: int, db: Session = Depends(get_db)):
    """获取文件信息"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件未找到")
        
        return ResponseBase(
            success=True,
            message="获取文件信息成功",
            data={
                "id": file_record.id,
                "filename": file_record.filename,
                "original_filename": file_record.original_filename,
                "file_path": file_record.file_path,
                "file_size": file_record.file_size,
                "file_type": file_record.file_type,
                "category": file_record.category,
                "description": file_record.description,
                "download_url": f"/api/files/download/{file_record.id}",
                "exists": os.path.exists(file_record.file_path),
                "created_at": file_record.created_at.isoformat(),
                "updated_at": file_record.updated_at.isoformat() if file_record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")

@router.put("/{file_id}", response_model=ResponseBase)
async def update_file_info(
    file_id: int,
    file_update: FileRecordUpdate,
    db: Session = Depends(get_db)
):
    """更新文件信息"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件未找到")
        
        # 更新字段
        update_data = file_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(file_record, field, value)
        
        db.commit()
        db.refresh(file_record)
        
        return ResponseBase(
            success=True,
            message="文件信息更新成功",
            data={
                "id": file_record.id,
                "filename": file_record.filename,
                "original_filename": file_record.original_filename,
                "file_size": file_record.file_size,
                "file_type": file_record.file_type,
                "category": file_record.category,
                "description": file_record.description,
                "download_url": f"/api/files/download/{file_record.id}",
                "created_at": file_record.created_at.isoformat(),
                "updated_at": file_record.updated_at.isoformat() if file_record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新文件信息失败: {str(e)}")

@router.delete("/{file_id}", response_model=ResponseBase)
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    """删除文件"""
    try:
        file_record = db.query(FileRecordModel).filter(FileRecordModel.id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="文件未找到")
        
        # 删除物理文件
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 删除数据库记录
        db.delete(file_record)
        db.commit()
        
        return ResponseBase(
            success=True,
            message="文件删除成功",
            data={"id": file_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")

@router.get("/stats/summary")
async def get_file_stats(db: Session = Depends(get_db)):
    """获取文件统计信息"""
    try:
        total_files = db.query(FileRecordModel).count()
        
        # 计算总文件大小
        total_size_result = db.query(
            db.func.sum(FileRecordModel.file_size)
        ).scalar()
        total_size = int(total_size_result) if total_size_result else 0
        
        # 统计各分类文件数量
        category_stats = {}
        categories = db.query(FileRecordModel.category).distinct().all()
        for (category,) in categories:
            count = db.query(FileRecordModel).filter(FileRecordModel.category == category).count()
            category_stats[category] = count
        
        # 统计文件类型分布
        type_stats = {}
        files = db.query(FileRecordModel).all()
        for file_record in files:
            ext = Path(file_record.original_filename).suffix.lower()
            type_stats[ext] = type_stats.get(ext, 0) + 1
        
        return ResponseBase(
            success=True,
            message="获取统计信息成功",
            data={
                "total_files": total_files,
                "total_size": total_size,
                "total_size_mb": round(total_size / 1024 / 1024, 2),
                "category_distribution": category_stats,
                "type_distribution": type_stats
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """获取所有文件分类"""
    try:
        categories = db.query(FileRecordModel.category).distinct().all()
        category_list = [category[0] for category in categories if category[0]]
        
        return ResponseBase(
            success=True,
            message="获取分类列表成功",
            data={
                "categories": sorted(category_list),
                "count": len(category_list)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分类列表失败: {str(e)}")