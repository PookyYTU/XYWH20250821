# -*- coding: utf-8 -*-
"""
数据库模型定义
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base


class FoodRecord(Base):
    """美食记录模型"""
    __tablename__ = "food_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="美食名称")
    location = Column(String(200), nullable=True, comment="地点")
    rating = Column(Float, nullable=True, comment="评分")
    description = Column(Text, nullable=True, comment="描述")
    date = Column(String(20), nullable=True, comment="日期")
    category = Column(String(100), nullable=True, comment="分类")
    price = Column(Float, nullable=True, comment="价格")
    image_url = Column(String(500), nullable=True, comment="图片URL")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<FoodRecord(id={self.id}, name='{self.name}', location='{self.location}')>"


class MovieRecord(Base):
    """电影记录模型"""
    __tablename__ = "movie_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="电影标题")
    director = Column(String(200), nullable=True, comment="导演")
    genre = Column(String(100), nullable=True, comment="类型")
    rating = Column(Float, nullable=True, comment="评分")
    review = Column(Text, nullable=True, comment="观后感")
    watch_date = Column(String(20), nullable=True, comment="观看日期")
    duration = Column(Integer, nullable=True, comment="时长(分钟)")
    poster_url = Column(String(500), nullable=True, comment="海报URL")
    imdb_id = Column(String(50), nullable=True, comment="IMDB ID")
    is_favorite = Column(Boolean, default=False, comment="是否收藏")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<MovieRecord(id={self.id}, title='{self.title}', director='{self.director}')>"


class CalendarNote(Base):
    """日历备注模型"""
    __tablename__ = "calendar_notes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(String(10), nullable=False, unique=True, index=True, comment="日期(YYYY-MM-DD)")
    content = Column(Text, nullable=False, comment="备注内容")
    mood = Column(String(50), nullable=True, comment="心情")
    weather = Column(String(50), nullable=True, comment="天气")
    is_special = Column(Boolean, default=False, comment="是否特殊日期")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<CalendarNote(id={self.id}, date='{self.date}', content='{self.content[:20]}...')>"


class FileRecord(Base):
    """文件记录模型"""
    __tablename__ = "file_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False, comment="文件名")
    original_filename = Column(String(255), nullable=False, comment="原始文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小(字节)")
    file_type = Column(String(100), nullable=True, comment="文件类型")
    mime_type = Column(String(200), nullable=True, comment="MIME类型")
    description = Column(Text, nullable=True, comment="文件描述")
    category = Column(String(100), nullable=True, comment="文件分类")
    is_public = Column(Boolean, default=False, comment="是否公开")
    download_count = Column(Integer, default=0, comment="下载次数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<FileRecord(id={self.id}, filename='{self.filename}', size={self.file_size})>"


class SystemLog(Base):
    """系统日志模型"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(String(20), nullable=False, comment="日志级别")
    message = Column(Text, nullable=False, comment="日志消息")
    module = Column(String(100), nullable=True, comment="模块名称")
    function = Column(String(100), nullable=True, comment="函数名称")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(500), nullable=True, comment="用户代理")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', message='{self.message[:50]}...')>"