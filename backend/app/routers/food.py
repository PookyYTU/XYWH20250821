# -*- coding: utf-8 -*-
"""
美食记录API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional

from app.database import get_db
from app.models import FoodRecord as FoodRecordModel
from app.schemas import (
    FoodRecord, FoodRecordCreate, FoodRecordUpdate, 
    BaseResponse, PaginatedResponse, StatsResponse
)

router = APIRouter()


@router.get("/food", response_model=PaginatedResponse)
async def get_food_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    category: Optional[str] = Query(None, description="分类筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取美食记录列表"""
    try:
        # 构建查询
        query = db.query(FoodRecordModel)
        
        # 分类筛选
        if category:
            query = query.filter(FoodRecordModel.category == category)
        
        # 关键词搜索
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (FoodRecordModel.name.like(search_term)) |
                (FoodRecordModel.location.like(search_term)) |
                (FoodRecordModel.description.like(search_term))
            )
        
        # 总数统计
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        records = query.order_by(desc(FoodRecordModel.created_at)).offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            message="获取美食记录成功",
            data=[FoodRecord.from_orm(record) for record in records],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食记录失败: {str(e)}")


@router.post("/food/", response_model=BaseResponse)
async def create_food_record(
    food_data: FoodRecordCreate,
    db: Session = Depends(get_db)
):
    """创建美食记录"""
    try:
        food_record = FoodRecordModel(**food_data.dict())
        db.add(food_record)
        db.commit()
        db.refresh(food_record)
        
        return BaseResponse(
            success=True,
            message="美食记录创建成功",
            data=FoodRecord.from_orm(food_record)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建美食记录失败: {str(e)}")


@router.get("/food/{food_id}", response_model=BaseResponse)
async def get_food_record(
    food_id: int,
    db: Session = Depends(get_db)
):
    """获取单个美食记录"""
    try:
        food_record = db.query(FoodRecordModel).filter(FoodRecordModel.id == food_id).first()
        if not food_record:
            raise HTTPException(status_code=404, detail="美食记录不存在")
        
        return BaseResponse(
            success=True,
            message="获取美食记录成功",
            data=FoodRecord.from_orm(food_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食记录失败: {str(e)}")


@router.put("/food/{food_id}", response_model=BaseResponse)
async def update_food_record(
    food_id: int,
    food_data: FoodRecordUpdate,
    db: Session = Depends(get_db)
):
    """更新美食记录"""
    try:
        food_record = db.query(FoodRecordModel).filter(FoodRecordModel.id == food_id).first()
        if not food_record:
            raise HTTPException(status_code=404, detail="美食记录不存在")
        
        # 更新字段
        update_data = food_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(food_record, field, value)
        
        db.commit()
        db.refresh(food_record)
        
        return BaseResponse(
            success=True,
            message="美食记录更新成功",
            data=FoodRecord.from_orm(food_record)
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新美食记录失败: {str(e)}")


@router.delete("/food/{food_id}", response_model=BaseResponse)
async def delete_food_record(
    food_id: int,
    db: Session = Depends(get_db)
):
    """删除美食记录"""
    try:
        food_record = db.query(FoodRecordModel).filter(FoodRecordModel.id == food_id).first()
        if not food_record:
            raise HTTPException(status_code=404, detail="美食记录不存在")
        
        db.delete(food_record)
        db.commit()
        
        return BaseResponse(
            success=True,
            message="美食记录删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除美食记录失败: {str(e)}")


@router.get("/food/stats/summary", response_model=BaseResponse)
async def get_food_stats(db: Session = Depends(get_db)):
    """获取美食记录统计"""
    try:
        # 总数统计
        total_count = db.query(FoodRecordModel).count()
        
        # 最近30天统计
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = db.query(FoodRecordModel).filter(
            FoodRecordModel.created_at >= thirty_days_ago
        ).count()
        
        # 分类统计
        category_stats = db.query(
            FoodRecordModel.category,
            func.count(FoodRecordModel.id).label('count')
        ).filter(
            FoodRecordModel.category.isnot(None)
        ).group_by(FoodRecordModel.category).all()
        
        categories = [
            {"name": cat[0] or "未分类", "count": cat[1]} 
            for cat in category_stats
        ]
        
        # 月度统计
        monthly_stats = db.query(
            func.date_format(FoodRecordModel.created_at, '%Y-%m').label('month'),
            func.count(FoodRecordModel.id).label('count')
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
            message="获取美食统计成功",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食统计失败: {str(e)}")