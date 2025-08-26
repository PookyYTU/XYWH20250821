# -*- coding: utf-8 -*-
"""
电影记录API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional

from app.database import get_db
from app.models import MovieRecord as MovieRecordModel
from app.schemas import (
    MovieRecord, MovieRecordCreate, MovieRecordUpdate,
    BaseResponse, PaginatedResponse, StatsResponse
)

router = APIRouter()


@router.get("/movie", response_model=PaginatedResponse)
async def get_movie_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    genre: Optional[str] = Query(None, description="类型筛选"),
    is_favorite: Optional[bool] = Query(None, description="收藏筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取电影记录列表"""
    try:
        # 构建查询
        query = db.query(MovieRecordModel)
        
        # 类型筛选
        if genre:
            query = query.filter(MovieRecordModel.genre == genre)
        
        # 收藏筛选
        if is_favorite is not None:
            query = query.filter(MovieRecordModel.is_favorite == is_favorite)
        
        # 关键词搜索
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (MovieRecordModel.title.like(search_term)) |
                (MovieRecordModel.director.like(search_term)) |
                (MovieRecordModel.review.like(search_term))
            )
        
        # 总数统计
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        records = query.order_by(desc(MovieRecordModel.created_at)).offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            message="获取电影记录成功",
            data=[MovieRecord.from_orm(record) for record in records],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影记录失败: {str(e)}")


@router.post("/movie/", response_model=BaseResponse)
async def create_movie_record(
    movie_data: MovieRecordCreate,
    db: Session = Depends(get_db)
):
    """创建电影记录"""
    try:
        movie_record = MovieRecordModel(**movie_data.dict())
        db.add(movie_record)
        db.commit()
        db.refresh(movie_record)
        
        return BaseResponse(
            success=True,
            message="电影记录创建成功",
            data=MovieRecord.from_orm(movie_record)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建电影记录失败: {str(e)}")


@router.get("/movie/{movie_id}", response_model=BaseResponse)
async def get_movie_record(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """获取单个电影记录"""
    try:
        movie_record = db.query(MovieRecordModel).filter(MovieRecordModel.id == movie_id).first()
        if not movie_record:
            raise HTTPException(status_code=404, detail="电影记录不存在")
        
        return BaseResponse(
            success=True,
            message="获取电影记录成功",
            data=MovieRecord.from_orm(movie_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影记录失败: {str(e)}")


@router.put("/movie/{movie_id}", response_model=BaseResponse)
async def update_movie_record(
    movie_id: int,
    movie_data: MovieRecordUpdate,
    db: Session = Depends(get_db)
):
    """更新电影记录"""
    try:
        movie_record = db.query(MovieRecordModel).filter(MovieRecordModel.id == movie_id).first()
        if not movie_record:
            raise HTTPException(status_code=404, detail="电影记录不存在")
        
        # 更新字段
        update_data = movie_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(movie_record, field, value)
        
        db.commit()
        db.refresh(movie_record)
        
        return BaseResponse(
            success=True,
            message="电影记录更新成功",
            data=MovieRecord.from_orm(movie_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新电影记录失败: {str(e)}")


@router.delete("/movie/{movie_id}", response_model=BaseResponse)
async def delete_movie_record(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """删除电影记录"""
    try:
        movie_record = db.query(MovieRecordModel).filter(MovieRecordModel.id == movie_id).first()
        if not movie_record:
            raise HTTPException(status_code=404, detail="电影记录不存在")
        
        db.delete(movie_record)
        db.commit()
        
        return BaseResponse(
            success=True,
            message="电影记录删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除电影记录失败: {str(e)}")


@router.get("/movie/stats/summary", response_model=BaseResponse)
async def get_movie_stats(db: Session = Depends(get_db)):
    """获取电影记录统计"""
    try:
        # 总数统计
        total_count = db.query(MovieRecordModel).count()
        
        # 最近30天统计
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = db.query(MovieRecordModel).filter(
            MovieRecordModel.created_at >= thirty_days_ago
        ).count()
        
        # 类型统计
        genre_stats = db.query(
            MovieRecordModel.genre,
            func.count(MovieRecordModel.id).label('count')
        ).filter(
            MovieRecordModel.genre.isnot(None)
        ).group_by(MovieRecordModel.genre).all()
        
        categories = [
            {"name": genre[0] or "未分类", "count": genre[1]} 
            for genre in genre_stats
        ]
        
        # 月度统计
        monthly_stats = db.query(
            func.date_format(MovieRecordModel.created_at, '%Y-%m').label('month'),
            func.count(MovieRecordModel.id).label('count')
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
            message="获取电影统计成功",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影统计失败: {str(e)}")