from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import MovieRecord as MovieRecordModel
from ..schemas import MovieRecord, MovieRecordCreate, MovieRecordUpdate, ResponseBase, ListResponse

router = APIRouter()

@router.get("/", response_model=ListResponse)
async def get_movie_records(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方式"),
    db: Session = Depends(get_db)
):
    """获取电影记录列表"""
    try:
        query = db.query(MovieRecordModel)
        
        # 搜索功能
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                MovieRecordModel.name.like(search_pattern) |
                MovieRecordModel.cinema.like(search_pattern) |
                MovieRecordModel.review.like(search_pattern) |
                MovieRecordModel.director.like(search_pattern) |
                MovieRecordModel.genre.like(search_pattern)
            )
        
        # 排序
        if hasattr(MovieRecordModel, sort_by):
            order_column = getattr(MovieRecordModel, sort_by)
            if sort_order == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        # 分页
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        
        return ListResponse(
            success=True,
            message="获取电影记录成功",
            data=[{
                "id": record.id,
                "name": record.name,
                "cinema": record.cinema,
                "date": record.date,
                "rating": record.rating,
                "review": record.review,
                "genre": record.genre,
                "director": record.director,
                "actors": record.actors,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            } for record in records],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影记录失败: {str(e)}")

@router.get("/{record_id}", response_model=ResponseBase)
async def get_movie_record(record_id: int, db: Session = Depends(get_db)):
    """获取单个电影记录"""
    try:
        record = db.query(MovieRecordModel).filter(MovieRecordModel.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="电影记录未找到")
        
        return ResponseBase(
            success=True,
            message="获取电影记录成功",
            data={
                "id": record.id,
                "name": record.name,
                "cinema": record.cinema,
                "date": record.date,
                "rating": record.rating,
                "review": record.review,
                "genre": record.genre,
                "director": record.director,
                "actors": record.actors,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat() if record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影记录失败: {str(e)}")

@router.post("/", response_model=ResponseBase)
async def create_movie_record(record: MovieRecordCreate, db: Session = Depends(get_db)):
    """创建电影记录"""
    try:
        db_record = MovieRecordModel(**record.dict())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return ResponseBase(
            success=True,
            message="电影记录创建成功",
            data={
                "id": db_record.id,
                "name": db_record.name,
                "cinema": db_record.cinema,
                "date": db_record.date,
                "rating": db_record.rating,
                "review": db_record.review,
                "genre": db_record.genre,
                "director": db_record.director,
                "actors": db_record.actors,
                "created_at": db_record.created_at.isoformat()
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建电影记录失败: {str(e)}")

@router.put("/{record_id}", response_model=ResponseBase)
async def update_movie_record(
    record_id: int, 
    record_update: MovieRecordUpdate, 
    db: Session = Depends(get_db)
):
    """更新电影记录"""
    try:
        db_record = db.query(MovieRecordModel).filter(MovieRecordModel.id == record_id).first()
        if not db_record:
            raise HTTPException(status_code=404, detail="电影记录未找到")
        
        # 更新字段
        update_data = record_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_record, field, value)
        
        db.commit()
        db.refresh(db_record)
        
        return ResponseBase(
            success=True,
            message="电影记录更新成功",
            data={
                "id": db_record.id,
                "name": db_record.name,
                "cinema": db_record.cinema,
                "date": db_record.date,
                "rating": db_record.rating,
                "review": db_record.review,
                "genre": db_record.genre,
                "director": db_record.director,
                "actors": db_record.actors,
                "created_at": db_record.created_at.isoformat(),
                "updated_at": db_record.updated_at.isoformat() if db_record.updated_at else None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新电影记录失败: {str(e)}")

@router.delete("/{record_id}", response_model=ResponseBase)
async def delete_movie_record(record_id: int, db: Session = Depends(get_db)):
    """删除电影记录"""
    try:
        db_record = db.query(MovieRecordModel).filter(MovieRecordModel.id == record_id).first()
        if not db_record:
            raise HTTPException(status_code=404, detail="电影记录未找到")
        
        db.delete(db_record)
        db.commit()
        
        return ResponseBase(
            success=True,
            message="电影记录删除成功",
            data={"id": record_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除电影记录失败: {str(e)}")

@router.get("/stats/summary")
async def get_movie_stats(db: Session = Depends(get_db)):
    """获取电影记录统计信息"""
    try:
        total_records = db.query(MovieRecordModel).count()
        
        # 计算平均评分
        avg_rating_result = db.query(
            db.func.avg(MovieRecordModel.rating)
        ).scalar()
        avg_rating = round(float(avg_rating_result), 2) if avg_rating_result else 0
        
        # 最高评分记录
        highest_rated = db.query(MovieRecordModel).filter(
            MovieRecordModel.rating == 5
        ).count()
        
        # 统计类型分布
        genre_stats = {}
        records = db.query(MovieRecordModel).all()
        for record in records:
            if record.genre:
                genres = [g.strip() for g in record.genre.split(',')]
                for genre in genres:
                    if genre:
                        genre_stats[genre] = genre_stats.get(genre, 0) + 1
        
        return ResponseBase(
            success=True,
            message="获取统计信息成功",
            data={
                "total_records": total_records,
                "avg_rating": avg_rating,
                "highest_rated_count": highest_rated,
                "genre_distribution": genre_stats
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@router.get("/search/by-rating/{rating}")
async def get_movies_by_rating(rating: int, db: Session = Depends(get_db)):
    """根据评分获取电影"""
    try:
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="评分必须在1-5之间")
        
        records = db.query(MovieRecordModel).filter(
            MovieRecordModel.rating == rating
        ).order_by(MovieRecordModel.created_at.desc()).all()
        
        return ResponseBase(
            success=True,
            message=f"获取{rating}星电影成功",
            data={
                "records": [{
                    "id": record.id,
                    "name": record.name,
                    "cinema": record.cinema,
                    "date": record.date,
                    "rating": record.rating,
                    "review": record.review,
                    "genre": record.genre,
                    "director": record.director,
                    "actors": record.actors,
                    "created_at": record.created_at.isoformat()
                } for record in records],
                "count": len(records)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")