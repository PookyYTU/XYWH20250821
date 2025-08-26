# -*- coding: utf-8 -*-
"""
Pydantic模式定义 - 用于API请求和响应的数据验证
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime


# 基础响应模式
class BaseResponse(BaseModel):
    """基础响应模式"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[Any] = None


class PaginatedResponse(BaseResponse):
    """分页响应模式"""
    total: int = 0
    page: int = 1
    page_size: int = 10
    total_pages: int = 0


# 美食记录相关模式
class FoodRecordBase(BaseModel):
    """美食记录基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="美食名称")
    location: Optional[str] = Field(None, max_length=200, description="地点")
    rating: Optional[float] = Field(None, ge=0, le=10, description="评分")
    description: Optional[str] = Field(None, description="描述")
    date: Optional[str] = Field(None, description="日期")
    category: Optional[str] = Field(None, max_length=100, description="分类")
    price: Optional[float] = Field(None, ge=0, description="价格")
    image_url: Optional[str] = Field(None, max_length=500, description="图片URL")


class FoodRecordCreate(FoodRecordBase):
    """创建美食记录模式"""
    pass


class FoodRecordUpdate(BaseModel):
    """更新美食记录模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=200)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, ge=0)
    image_url: Optional[str] = Field(None, max_length=500)


class FoodRecord(FoodRecordBase):
    """美食记录响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 电影记录相关模式
class MovieRecordBase(BaseModel):
    """电影记录基础模式"""
    title: str = Field(..., min_length=1, max_length=200, description="电影标题")
    director: Optional[str] = Field(None, max_length=200, description="导演")
    genre: Optional[str] = Field(None, max_length=100, description="类型")
    rating: Optional[float] = Field(None, ge=0, le=10, description="评分")
    review: Optional[str] = Field(None, description="观后感")
    watch_date: Optional[str] = Field(None, description="观看日期")
    duration: Optional[int] = Field(None, ge=0, description="时长(分钟)")
    poster_url: Optional[str] = Field(None, max_length=500, description="海报URL")
    imdb_id: Optional[str] = Field(None, max_length=50, description="IMDB ID")
    is_favorite: Optional[bool] = Field(False, description="是否收藏")


class MovieRecordCreate(MovieRecordBase):
    """创建电影记录模式"""
    pass


class MovieRecordUpdate(BaseModel):
    """更新电影记录模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=200)
    genre: Optional[str] = Field(None, max_length=100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    review: Optional[str] = None
    watch_date: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)
    poster_url: Optional[str] = Field(None, max_length=500)
    imdb_id: Optional[str] = Field(None, max_length=50)
    is_favorite: Optional[bool] = None


class MovieRecord(MovieRecordBase):
    """电影记录响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 日历备注相关模式
class CalendarNoteBase(BaseModel):
    """日历备注基础模式"""
    content: str = Field(..., min_length=1, description="备注内容")
    mood: Optional[str] = Field(None, max_length=50, description="心情")
    weather: Optional[str] = Field(None, max_length=50, description="天气")
    is_special: Optional[bool] = Field(False, description="是否特殊日期")


class CalendarNoteCreate(CalendarNoteBase):
    """创建日历备注模式"""
    date: str = Field(..., regex=r'^\d{4}-\d{2}-\d{2}$', description="日期(YYYY-MM-DD)")


class CalendarNoteUpdate(BaseModel):
    """更新日历备注模式"""
    content: Optional[str] = Field(None, min_length=1)
    mood: Optional[str] = Field(None, max_length=50)
    weather: Optional[str] = Field(None, max_length=50)
    is_special: Optional[bool] = None


class CalendarNote(CalendarNoteBase):
    """日历备注响应模式"""
    id: int
    date: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 文件记录相关模式
class FileRecordBase(BaseModel):
    """文件记录基础模式"""
    description: Optional[str] = Field(None, description="文件描述")
    category: Optional[str] = Field(None, max_length=100, description="文件分类")
    is_public: Optional[bool] = Field(False, description="是否公开")


class FileRecordCreate(FileRecordBase):
    """创建文件记录模式"""
    pass


class FileRecordUpdate(BaseModel):
    """更新文件记录模式"""
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    is_public: Optional[bool] = None


class FileRecord(FileRecordBase):
    """文件记录响应模式"""
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: Optional[str]
    mime_type: Optional[str]
    download_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 统计相关模式
class StatsResponse(BaseModel):
    """统计响应模式"""
    total_count: int = 0
    recent_count: int = 0
    categories: List[dict] = []
    monthly_data: List[dict] = []


# 健康检查模式
class HealthResponse(BaseModel):
    """健康检查响应模式"""
    status: str = "healthy"
    message: str = "API服务运行正常"
    version: str = "2.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)