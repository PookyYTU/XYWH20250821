from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

# 美食记录相关模式
class FoodRecordBase(BaseModel):
    name: str
    location: str
    price: float
    rating: int
    date: str
    notes: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('评分必须在1-5之间')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('价格不能为负数')
        return v

class FoodRecordCreate(FoodRecordBase):
    pass

class FoodRecordUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[int] = None
    date: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('评分必须在1-5之间')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('价格不能为负数')
        return v

class FoodRecord(FoodRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 电影记录相关模式
class MovieRecordBase(BaseModel):
    name: str
    cinema: str
    date: str
    rating: int
    review: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('评分必须在1-5之间')
        return v

class MovieRecordCreate(MovieRecordBase):
    pass

class MovieRecordUpdate(BaseModel):
    name: Optional[str] = None
    cinema: Optional[str] = None
    date: Optional[str] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('评分必须在1-5之间')
        return v

class MovieRecord(MovieRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 日历备注相关模式
class CalendarNoteBase(BaseModel):
    date: str
    content: str

class CalendarNoteCreate(CalendarNoteBase):
    pass

class CalendarNoteUpdate(BaseModel):
    content: str

class CalendarNote(CalendarNoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 文件记录相关模式
class FileRecordBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str
    category: str
    description: Optional[str] = None

class FileRecordCreate(FileRecordBase):
    pass

class FileRecordUpdate(BaseModel):
    filename: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class FileRecord(FileRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 响应模式
class ResponseBase(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ListResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]
    total: int