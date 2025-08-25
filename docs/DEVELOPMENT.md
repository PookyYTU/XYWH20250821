# 小雨微寒 - 开发指南

## 📋 目录

- [环境配置](#环境配置)
- [项目结构](#项目结构)
- [前端开发](#前端开发)
- [后端开发](#后端开发)
- [数据库开发](#数据库开发)
- [测试指南](#测试指南)
- [调试技巧](#调试技巧)
- [代码规范](#代码规范)

## 🛠️ 环境配置

### 环境要求

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 后端开发语言 |
| MySQL | 5.7+ | 数据库系统 |
| Git | 2.0+ | 版本控制 |

### 本地开发环境搭建

#### 1. 克隆项目
```bash
git clone <your-repo-url>
cd XYWH20250821
```

#### 2. 后端环境配置
```bash
cd backend

# 创建虚拟环境
python3.10 -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate
# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置文件
cp .env.example .env
```

#### 3. 数据库配置
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE xiaoyuweihan_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 4. 配置环境变量
编辑 `backend/.env` 文件：
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=xiaoyuweihan_dev

ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
DEBUG=True
```

#### 5. 启动开发服务器

**后端服务**:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端服务**:
```bash
# 在项目根目录
python -m http.server 3000
```

## 📁 项目结构

```
XYWH20250821/
├── backend/                    # 后端代码
│   ├── app/                    # 应用代码
│   │   ├── config.py          # 应用配置
│   │   ├── database.py        # 数据库连接
│   │   ├── models.py          # 数据模型
│   │   ├── schemas.py         # Pydantic模式
│   │   └── routers/           # API路由
│   ├── main.py                # FastAPI应用入口
│   └── requirements.txt       # Python依赖
├── scripts/                   # 前端JavaScript
│   ├── main.js               # 主要业务逻辑
│   ├── api.js                # API服务
│   └── api-data.js           # 数据管理器
├── styles/                    # 前端样式
│   ├── main.css              # 主要样式
│   └── components.css        # 组件样式
└── docs/                      # 项目文档
```

## 🎨 前端开发

### HTML开发规范

```html
<!-- 使用语义化标签 -->
<header class="site-header">
    <nav class="main-navigation">
        <ul class="nav-list">
            <li class="nav-item">
                <a href="#food" class="nav-link">美食记录</a>
            </li>
        </ul>
    </nav>
</header>

<main class="main-content">
    <section class="food-section">
        <h2 class="section-title">美食记录</h2>
    </section>
</main>
```

### CSS开发规范

#### BEM命名规范
```css
/* Block块 */
.food-card {
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 8px;
}

/* Element元素 */
.food-card__image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.food-card__title {
    font-size: 1.2em;
    font-weight: bold;
    margin: 0.5em 0;
}

/* Modifier修饰符 */
.food-card--featured {
    border-color: #007bff;
    box-shadow: 0 4px 8px rgba(0,123,255,0.1);
}
```

#### CSS变量使用
```css
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
}

.button {
    background-color: var(--primary-color);
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    border-radius: 4px;
}
```

### JavaScript开发规范

#### 模块化结构
```javascript
// api.js - API服务模块
class ApiService {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }
    
    async request(method, url, data = null) {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) options.body = JSON.stringify(data);
        return fetch(this.baseURL + url, options);
    }
    
    async getFoodRecords(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `/food/?${queryString}` : '/food/';
        return this.request('GET', url);
    }
    
    async createFoodRecord(data) {
        return this.request('POST', '/food/', data);
    }
}
```

#### 事件处理最佳实践
```javascript
// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// 搜索防抖
const debouncedSearch = debounce(async (query) => {
    try {
        const results = await api.searchFood(query);
        displaySearchResults(results);
    } catch (error) {
        showError('搜索失败: ' + error.message);
    }
}, 300);

// 添加事件监听
document.getElementById('search-input').addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});
```

## ⚡ 后端开发

### FastAPI应用结构

#### 应用配置 (config.py)
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "xiaoyuweihan"
    
    # 跨域配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # 开发模式
    DEBUG: bool = False
    
    @property
    def database_url(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### 数据库连接 (database.py)
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=0
)

SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

#### 数据模型 (models.py)
```python
from sqlalchemy import Column, Integer, String, Decimal, Date, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class FoodRecord(Base):
    __tablename__ = "food_records"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    rating = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Pydantic模式 (schemas.py)
```python
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class FoodRecordBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    location: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    date: date
    notes: Optional[str] = None
    
    @validator('price')
    def validate_price(cls, v):
        return round(v, 2)

class FoodRecordCreate(FoodRecordBase):
    pass

class FoodRecordResponse(FoodRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### 路由开发

```python
# routers/food.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.database import get_db
from app.models import FoodRecord
from app.schemas import FoodRecordCreate, FoodRecordResponse

router = APIRouter(prefix="/api/food", tags=["美食记录"])

@router.get("/", response_model=List[FoodRecordResponse])
async def get_food_records(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    query = select(FoodRecord).offset(skip).limit(limit).order_by(desc(FoodRecord.created_at))
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=FoodRecordResponse)
async def create_food_record(
    food_data: FoodRecordCreate,
    db: AsyncSession = Depends(get_db)
):
    food_record = FoodRecord(**food_data.dict())
    db.add(food_record)
    await db.commit()
    await db.refresh(food_record)
    return food_record
```

## 🗄️ 数据库开发

### 数据库迁移

```python
# 创建迁移脚本
async def create_tables():
    """创建所有数据表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 删除表
async def drop_tables():
    """删除所有数据表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### 数据库索引优化

```sql
-- 为查询优化创建索引
CREATE INDEX idx_food_date_rating ON food_records(date, rating);
CREATE INDEX idx_movie_genre_date ON movie_records(genre, date);
CREATE INDEX idx_calendar_important ON calendar_notes(is_important);
```

## 🧪 测试指南

### 测试环境配置

```python
# conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

### API测试示例

```python
# test_food.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_food_record(test_client: AsyncClient):
    food_data = {
        "name": "测试美食",
        "location": "测试地点",
        "price": 50.0,
        "rating": 5,
        "date": "2025-01-15",
        "notes": "测试备注"
    }
    
    response = await test_client.post("/api/food/", json=food_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == food_data["name"]
    assert data["location"] == food_data["location"]
```

## 🔧 调试技巧

### 日志配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 常用调试命令

```bash
# 查看API文档
curl http://localhost:8000/docs

# 测试健康检查
curl http://localhost:8000/api/health

# 运行测试
pytest tests/ -v

# 检查代码风格
flake8 app/
black app/
```

## 📝 代码规范

### Python代码规范

- 遵循PEP 8规范
- 使用类型提示
- 编写详细的文档字符串
- 函数名使用snake_case
- 类名使用PascalCase

### JavaScript代码规范

- 使用驼峰命名法
- 使用const/let，避免var
- 添加详细注释
- 使用async/await处理异步操作

### Git提交规范

```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具的变动
```

## 🔄 版本控制

### 分支管理

- main: 生产环境分支
- develop: 开发分支
- feature/*: 功能分支
- hotfix/*: 热修复分支

### 开发流程

1. 从develop分支创建feature分支
2. 在feature分支上开发新功能
3. 提交代码并创建Pull Request
4. 代码审查通过后合并到develop
5. 测试完成后合并到main分支

---

*此开发指南提供了完整的开发环境配置和最佳实践建议*