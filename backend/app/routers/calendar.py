# -*- coding: utf-8 -*-
"""
日历备注API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import calendar

from app.database import get_db
from app.models import CalendarNote as CalendarNoteModel
from app.schemas import (
    CalendarNote, CalendarNoteCreate, CalendarNoteUpdate,
    BaseResponse, PaginatedResponse
)

router = APIRouter()


@router.get("/calendar", response_model=PaginatedResponse)
async def get_calendar_notes(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    start_date: Optional[str] = Query(None, description="开始日期(YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期(YYYY-MM-DD)"),
    is_special: Optional[bool] = Query(None, description="特殊日期筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取日历备注列表"""
    try:
        # 构建查询
        query = db.query(CalendarNoteModel)
        
        # 日期范围筛选
        if start_date:
            query = query.filter(CalendarNoteModel.date >= start_date)
        if end_date:
            query = query.filter(CalendarNoteModel.date <= end_date)
        
        # 特殊日期筛选
        if is_special is not None:
            query = query.filter(CalendarNoteModel.is_special == is_special)
        
        # 关键词搜索
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (CalendarNoteModel.content.like(search_term)) |
                (CalendarNoteModel.mood.like(search_term))
            )
        
        # 总数统计
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        notes = query.order_by(desc(CalendarNoteModel.date)).offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            message="获取日历备注成功",
            data=[CalendarNote.from_orm(note) for note in notes],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日历备注失败: {str(e)}")


@router.get("/calendar/{date}", response_model=BaseResponse)
async def get_note_by_date(
    date: str,
    db: Session = Depends(get_db)
):
    """获取指定日期的备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")
        
        note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date).first()
        
        return BaseResponse(
            success=True,
            message="获取日历备注成功",
            data=CalendarNote.from_orm(note) if note else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日历备注失败: {str(e)}")


@router.put("/calendar/{date}", response_model=BaseResponse)
async def create_or_update_note(
    date: str,
    content: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """创建或更新指定日期的备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")
        
        # 查找现有备注
        existing_note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date).first()
        
        if existing_note:
            # 更新现有备注
            if content.strip():
                existing_note.content = content.strip()
                db.commit()
                db.refresh(existing_note)
                return BaseResponse(
                    success=True,
                    message="日历备注更新成功",
                    data=CalendarNote.from_orm(existing_note)
                )
            else:
                # 内容为空则删除备注
                db.delete(existing_note)
                db.commit()
                return BaseResponse(
                    success=True,
                    message="日历备注删除成功"
                )
        else:
            # 创建新备注
            if content.strip():
                new_note = CalendarNoteModel(
                    date=date,
                    content=content.strip()
                )
                db.add(new_note)
                db.commit()
                db.refresh(new_note)
                return BaseResponse(
                    success=True,
                    message="日历备注创建成功",
                    data=CalendarNote.from_orm(new_note)
                )
            else:
                return BaseResponse(
                    success=True,
                    message="备注内容为空，无需创建"
                )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建或更新日历备注失败: {str(e)}")


@router.delete("/calendar/{date}", response_model=BaseResponse)
async def delete_note(
    date: str,
    db: Session = Depends(get_db)
):
    """删除指定日期的备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")
        
        note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date).first()
        if not note:
            raise HTTPException(status_code=404, detail="日历备注不存在")
        
        db.delete(note)
        db.commit()
        
        return BaseResponse(
            success=True,
            message="日历备注删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除日历备注失败: {str(e)}")


@router.get("/calendar/month/{year}/{month}", response_model=BaseResponse)
async def get_month_notes(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """获取指定月份的所有备注"""
    try:
        # 验证年月
        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="月份必须在1-12之间")
        
        if not (1900 <= year <= 2100):
            raise HTTPException(status_code=400, detail="年份超出有效范围")
        
        # 计算月份的第一天和最后一天
        first_day = f"{year}-{month:02d}-01"
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_day = f"{year}-{month:02d}-{last_day_of_month:02d}"
        
        # 查询月份内的所有备注
        notes = db.query(CalendarNoteModel).filter(
            and_(
                CalendarNoteModel.date >= first_day,
                CalendarNoteModel.date <= last_day
            )
        ).order_by(CalendarNoteModel.date).all()
        
        # 转换为字典格式，key为日期，value为备注内容
        notes_dict = {note.date: note.content for note in notes}
        
        return BaseResponse(
            success=True,
            message="获取月份备注成功",
            data={
                "year": year,
                "month": month,
                "notes": notes_dict,
                "count": len(notes)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取月份备注失败: {str(e)}")


@router.get("/calendar/stats/summary", response_model=BaseResponse)
async def get_calendar_stats(db: Session = Depends(get_db)):
    """获取日历备注统计"""
    try:
        # 总数统计
        total_count = db.query(CalendarNoteModel).count()
        
        # 特殊日期统计
        special_count = db.query(CalendarNoteModel).filter(
            CalendarNoteModel.is_special == True
        ).count()
        
        # 最近30天统计
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = db.query(CalendarNoteModel).filter(
            CalendarNoteModel.created_at >= thirty_days_ago
        ).count()
        
        # 月度统计
        monthly_stats = db.query(
            func.substr(CalendarNoteModel.date, 1, 7).label('month'),
            func.count(CalendarNoteModel.id).label('count')
        ).group_by('month').order_by('month').limit(12).all()
        
        monthly_data = [
            {"month": month[0], "count": month[1]} 
            for month in monthly_stats
        ]
        
        return BaseResponse(
            success=True,
            message="获取日历统计成功",
            data={
                "total_count": total_count,
                "special_count": special_count,
                "recent_count": recent_count,
                "monthly_data": monthly_data
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日历统计失败: {str(e)}")