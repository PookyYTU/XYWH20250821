from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import FoodRecord as FoodRecordModel
from ..schemas import FoodRecord, FoodRecordCreate, FoodRecordUpdate, ResponseBase, ListResponse

router = APIRouter()

@router.get("/", response_model=ListResponse)
async def get_food_records(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方式"),
    db: Session = Depends(get_db)
):
    """获取美食记录列表"""
    try:
        query = db.query(FoodRecordModel)
        
        # 搜索功能
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                FoodRecordModel.name.like(search_pattern) |
                FoodRecordModel.location.like(search_pattern) |
                FoodRecordModel.notes.like(search_pattern)
            )
        
        # 排序
        if hasattr(FoodRecordModel, sort_by):
            order_column = getattr(FoodRecordModel, sort_by)
            if sort_order == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        # 分页
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        
        return ListResponse(
            success=True,
            message="获取美食记录成功",
            data=[{
                "id": record.id,
                "name": record.name,
                "location": record.location,
                "price": record.price,
                "rating": record.rating,
                "date": record.date,
                "notes": record.notes,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            } for record in records],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食记录失败: {str(e)}")

@router.get("/{record_id}", response_model=ResponseBase)
async def get_food_record(record_id: int, db: Session = Depends(get_db)):
    """获取单个美食记录"""
    try:
        record = db.query(FoodRecordModel).filter(FoodRecordModel.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="美食记录未找到")
        
        return ResponseBase(
            success=True,
            message="获取美食记录成功",
            data={
                "id": record.id,
                "name": record.name,
                "location": record.location,
                "price": record.price,
                "rating": record.rating,
                "date": record.date,
                "notes": record.notes,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食记录失败: {str(e)}")

@router.post("/", response_model=ResponseBase)
async def create_food_record(record: FoodRecordCreate, db: Session = Depends(get_db)):
    """创建美食记录"""
    try:
        db_record = FoodRecordModel(**record.dict())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return ResponseBase(
            success=True,
            message="美食记录创建成功",
            data={
                "id": db_record.id,
                "name": db_record.name,
                "location": db_record.location,
                "price": db_record.price,
                "rating": db_record.rating,
                "date": db_record.date,
                "notes": db_record.notes,
                "created_at": db_record.created_at.isoformat()
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建美食记录失败: {str(e)}")

@router.put("/{record_id}", response_model=ResponseBase)
async def update_food_record(
    record_id: int, 
    record_update: FoodRecordUpdate, 
    db: Session = Depends(get_db)
):
    """更新美食记录"""
    try:
        db_record = db.query(FoodRecordModel).filter(FoodRecordModel.id == record_id).first()
        if not db_record:
            raise HTTPException(status_code=404, detail="美食记录未找到")
        
        # 更新字段
        update_data = record_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_record, field, value)
        
        db.commit()
        db.refresh(db_record)
        
        return ResponseBase(
            success=True,
            message="美食记录更新成功",
            data={
                "id": db_record.id,
                "name": db_record.name,
                "location": db_record.location,
                "price": db_record.price,
                "rating": db_record.rating,
                "date": db_record.date,
                "notes": db_record.notes,
                "created_at": db_record.created_at.isoformat(),
                "updated_at": db_record.updated_at.isoformat() if db_record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新美食记录失败: {str(e)}")

@router.delete("/{record_id}", response_model=ResponseBase)
async def delete_food_record(record_id: int, db: Session = Depends(get_db)):
    """删除美食记录"""
    try:
        db_record = db.query(FoodRecordModel).filter(FoodRecordModel.id == record_id).first()
        if not db_record:
            raise HTTPException(status_code=404, detail="美食记录未找到")
        
        db.delete(db_record)
        db.commit()
        
        return ResponseBase(
            success=True,
            message="美食记录删除成功",
            data={"id": record_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除美食记录失败: {str(e)}")

@router.get("/stats/summary")
async def get_food_stats(db: Session = Depends(get_db)):
    """获取美食记录统计信息"""
    try:
        total_records = db.query(FoodRecordModel).count()
        
        # 计算平均评分
        avg_rating_result = db.query(
            db.func.avg(FoodRecordModel.rating)
        ).scalar()
        avg_rating = round(float(avg_rating_result), 2) if avg_rating_result else 0
        
        # 计算总花费
        total_cost_result = db.query(
            db.func.sum(FoodRecordModel.price)
        ).scalar()
        total_cost = float(total_cost_result) if total_cost_result else 0
        
        # 最高评分记录
        highest_rated = db.query(FoodRecordModel).filter(
            FoodRecordModel.rating == 5
        ).count()
        
        return ResponseBase(
            success=True,
            message="获取统计信息成功",
            data={
                "total_records": total_records,
                "avg_rating": avg_rating,
                "total_cost": total_cost,
                "highest_rated_count": highest_rated
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")