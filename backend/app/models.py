from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from .database import Base

class FoodRecord(Base):
    """美食记录模型"""
    __tablename__ = "food_records"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="美食名称")
    location = Column(String(200), nullable=False, comment="地点")
    price = Column(Float, nullable=False, comment="价格")
    rating = Column(Integer, nullable=False, comment="评分(1-5)")
    date = Column(String(20), nullable=False, comment="日期")
    notes = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

class MovieRecord(Base):
    """电影记录模型"""
    __tablename__ = "movie_records"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="电影名称")
    cinema = Column(String(200), nullable=False, comment="影院")
    date = Column(String(20), nullable=False, comment="观影日期")
    rating = Column(Integer, nullable=False, comment="评分(1-5)")
    review = Column(Text, comment="影评")
    genre = Column(String(100), comment="类型")
    director = Column(String(100), comment="导演")
    actors = Column(Text, comment="主演(JSON格式)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

class CalendarNote(Base):
    """日历备注模型"""
    __tablename__ = "calendar_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(20), nullable=False, unique=True, comment="日期(YYYY-MM-DD)")
    content = Column(Text, nullable=False, comment="备注内容")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

class FileRecord(Base):
    """文件记录模型"""
    __tablename__ = "file_records"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(200), nullable=False, comment="文件名")
    original_filename = Column(String(200), nullable=False, comment="原始文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小(字节)")
    file_type = Column(String(50), nullable=False, comment="文件类型")
    category = Column(String(50), nullable=False, comment="文件分类")
    description = Column(Text, comment="文件描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")