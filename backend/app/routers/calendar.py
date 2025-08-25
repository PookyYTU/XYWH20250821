from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from ..database import get_db
from ..models import CalendarNote as CalendarNoteModel
from ..schemas import CalendarNote, CalendarNoteCreate, CalendarNoteUpdate, ResponseBase, ListResponse

router = APIRouter()

@router.get("/", response_model=ListResponse)
async def get_calendar_notes(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    year: Optional[int] = Query(None, description="年份"),
    month: Optional[int] = Query(None, ge=1, le=12, description="月份"),
    db: Session = Depends(get_db)
):
    """获取日历备注列表"""
    try:
        query = db.query(CalendarNoteModel)
        
        # 按年份过滤
        if year:
            query = query.filter(CalendarNoteModel.date.like(f"{year}-%"))
            
            # 按月份过滤
            if month:
                month_str = f"{month:02d}"
                query = query.filter(CalendarNoteModel.date.like(f"{year}-{month_str}-%"))
        
        # 按日期排序
        query = query.order_by(CalendarNoteModel.date.desc())
        
        # 分页
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        
        return ListResponse(
            success=True,
            message="获取日历备注成功",
            data=[{
                "id": record.id,
                "date": record.date,
                "content": record.content,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            } for record in records],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日历备注失败: {str(e)}")

@router.get("/{date_str}", response_model=ResponseBase)
async def get_note_by_date(date_str: str, db: Session = Depends(get_db)):
    """根据日期获取备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        record = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date_str).first()
        
        if not record:
            return ResponseBase(
                success=True,
                message="该日期暂无备注",
                data=None
            )
        
        return ResponseBase(
            success=True,
            message="获取备注成功",
            data={
                "id": record.id,
                "date": record.date,
                "content": record.content,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取备注失败: {str(e)}")

@router.post("/", response_model=ResponseBase)
async def create_note(note: CalendarNoteCreate, db: Session = Depends(get_db)):
    """创建日历备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(note.date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        # 检查是否已存在该日期的备注
        existing_note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == note.date).first()
        if existing_note:
            raise HTTPException(status_code=400, detail="该日期已有备注，请使用更新接口")
        
        db_note = CalendarNoteModel(**note.dict())
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        return ResponseBase(
            success=True,
            message="备注创建成功",
            data={
                "id": db_note.id,
                "date": db_note.date,
                "content": db_note.content,
                "created_at": db_note.created_at.isoformat()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建备注失败: {str(e)}")

@router.put("/{date_str}", response_model=ResponseBase)
async def update_note_by_date(
    date_str: str, 
    note_update: CalendarNoteUpdate, 
    db: Session = Depends(get_db)
):
    """根据日期更新备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        db_note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date_str).first()
        
        if not db_note:
            # 如果不存在，创建新备注
            db_note = CalendarNoteModel(
                date=date_str,
                content=note_update.content
            )
            db.add(db_note)
            message = "备注创建成功"
        else:
            # 如果存在，更新备注
            db_note.content = note_update.content
            message = "备注更新成功"
        
        db.commit()
        db.refresh(db_note)
        
        return ResponseBase(
            success=True,
            message=message,
            data={
                "id": db_note.id,
                "date": db_note.date,
                "content": db_note.content,
                "created_at": db_note.created_at.isoformat(),
                "updated_at": db_note.updated_at.isoformat() if db_note.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新备注失败: {str(e)}")

@router.delete("/{date_str}", response_model=ResponseBase)
async def delete_note_by_date(date_str: str, db: Session = Depends(get_db)):
    """根据日期删除备注"""
    try:
        # 验证日期格式
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        db_note = db.query(CalendarNoteModel).filter(CalendarNoteModel.date == date_str).first()
        if not db_note:
            raise HTTPException(status_code=404, detail="该日期的备注未找到")
        
        db.delete(db_note)
        db.commit()
        
        return ResponseBase(
            success=True,
            message="备注删除成功",
            data={"date": date_str}
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除备注失败: {str(e)}")

@router.get("/month/{year}/{month}")
async def get_month_notes(year: int, month: int, db: Session = Depends(get_db)):
    """获取指定月份的所有备注"""
    try:
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="月份必须在1-12之间")
        
        month_str = f"{month:02d}"
        date_pattern = f"{year}-{month_str}-%"
        
        notes = db.query(CalendarNoteModel).filter(
            CalendarNoteModel.date.like(date_pattern)
        ).order_by(CalendarNoteModel.date.asc()).all()
        
        # 转换为字典格式，方便前端使用
        notes_dict = {}
        for note in notes:
            notes_dict[note.date] = {
                "id": note.id,
                "content": note.content,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat() if note.updated_at else None
            }
        
        return ResponseBase(
            success=True,
            message=f"获取{year}年{month}月备注成功",
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

@router.get("/search/content")
async def search_notes_by_content(
    keyword: str = Query(..., description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """根据内容搜索备注"""
    try:
        search_pattern = f"%{keyword}%"
        notes = db.query(CalendarNoteModel).filter(
            CalendarNoteModel.content.like(search_pattern)
        ).order_by(CalendarNoteModel.date.desc()).all()
        
        return ResponseBase(
            success=True,
            message=f"搜索到{len(notes)}条相关备注",
            data={
                "keyword": keyword,
                "results": [{
                    "id": note.id,
                    "date": note.date,
                    "content": note.content,
                    "created_at": note.created_at.isoformat(),
                    "updated_at": note.updated_at.isoformat() if note.updated_at else None
                } for note in notes],
                "count": len(notes)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@router.get("/stats/summary")
async def get_calendar_stats(db: Session = Depends(get_db)):
    """获取日历备注统计信息"""
    try:
        total_notes = db.query(CalendarNoteModel).count()
        
        # 获取最早和最晚的备注日期
        earliest_note = db.query(CalendarNoteModel).order_by(
            CalendarNoteModel.date.asc()
        ).first()
        
        latest_note = db.query(CalendarNoteModel).order_by(
            CalendarNoteModel.date.desc()
        ).first()
        
        # 统计各年份的备注数量
        yearly_stats = {}
        notes = db.query(CalendarNoteModel).all()
        for note in notes:
            year = note.date.split('-')[0]
            yearly_stats[year] = yearly_stats.get(year, 0) + 1
        
        return ResponseBase(
            success=True,
            message="获取统计信息成功",
            data={
                "total_notes": total_notes,
                "earliest_date": earliest_note.date if earliest_note else None,
                "latest_date": latest_note.date if latest_note else None,
                "yearly_distribution": yearly_stats
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")