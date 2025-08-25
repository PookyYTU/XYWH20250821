# 小雨微寒 - 技术文档

## 📋 目录

- [技术架构概览](#技术架构概览)
- [数据库设计](#数据库设计)
- [API设计](#api设计)
- [前端架构](#前端架构)
- [后端架构](#后端架构)
- [安全机制](#安全机制)

## 🏗️ 技术架构概览

### 整体架构图

```
用户浏览器 ◄──► Nginx服务器 ◄──► 静态文件存储
              │
              ▼
         FastAPI应用
         (Gunicorn)
              │
              ▼
         MySQL数据库
```

### 技术栈详情

#### 前端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 语义化页面结构 |
| CSS3 | - | 现代样式设计 |
| JavaScript ES6+ | - | 原生交互逻辑 |

#### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10.12 | 编程语言 |
| FastAPI | 0.104.1 | Web框架 |
| Gunicorn | 21.2.0 | WSGI服务器 |
| SQLAlchemy | 2.0.23 | ORM框架 |
| Pydantic | 2.5.0 | 数据验证 |

#### 基础设施
| 组件 | 版本 | 用途 |
|------|------|------|
| MySQL | 5.7.40 | 数据存储 |
| Nginx | 1.26.1 | 反向代理 |
| systemd | - | 服务管理 |

## 🗄️ 数据库设计

### 主要数据表

#### 美食记录表 (food_records)
```sql
CREATE TABLE food_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL COMMENT '美食名称',
    location VARCHAR(255) NOT NULL COMMENT '用餐地点',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    date DATE NOT NULL COMMENT '用餐日期',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 电影记录表 (movie_records)
```sql
CREATE TABLE movie_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL COMMENT '电影名称',
    cinema VARCHAR(255) NOT NULL COMMENT '影院名称',
    date DATE NOT NULL COMMENT '观影日期',
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT COMMENT '影评',
    genre VARCHAR(100) COMMENT '电影类型',
    director VARCHAR(255) COMMENT '导演',
    actors TEXT COMMENT '主演',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 日历备注表 (calendar_notes)
```sql
CREATE TABLE calendar_notes (
    date DATE PRIMARY KEY COMMENT '日期',
    note TEXT NOT NULL COMMENT '备注内容',
    is_important BOOLEAN DEFAULT FALSE COMMENT '是否重要',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 文件记录表 (file_records)
```sql
CREATE TABLE file_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL COMMENT '存储文件名',
    original_name VARCHAR(255) NOT NULL COMMENT '原始文件名',
    file_size BIGINT NOT NULL COMMENT '文件大小',
    file_type VARCHAR(100) NOT NULL COMMENT '文件类型',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    description TEXT COMMENT '文件描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 🌐 API设计

### 统一响应格式

#### 成功响应
```json
{
    "success": true,
    "data": { /* 具体数据 */ },
    "message": "操作成功"
}
```

#### 错误响应
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "数据验证失败"
    }
}
```

### 主要API端点

#### 美食记录 API
- `GET /api/food/` - 获取美食记录列表
- `POST /api/food/` - 创建美食记录
- `PUT /api/food/{id}` - 更新美食记录
- `DELETE /api/food/{id}` - 删除美食记录
- `GET /api/food/stats/summary` - 获取统计信息

#### 电影记录 API
- `GET /api/movie/` - 获取电影记录列表
- `POST /api/movie/` - 创建电影记录
- `PUT /api/movie/{id}` - 更新电影记录
- `DELETE /api/movie/{id}` - 删除电影记录

#### 日历备注 API
- `GET /api/calendar/` - 获取日历备注列表
- `POST /api/calendar/` - 创建日历备注
- `PUT /api/calendar/{date}` - 更新日期备注
- `DELETE /api/calendar/{date}` - 删除日期备注

#### 文件管理 API
- `GET /api/files/` - 获取文件列表
- `POST /api/files/upload` - 上传文件
- `GET /api/files/download/{id}` - 下载文件
- `DELETE /api/files/{id}` - 删除文件

## 🎨 前端架构

### 模块化设计

```
scripts/
├── main.js          # 主要业务逻辑
├── music.js         # 音乐播放器模块
├── calendar.js      # 日历组件模块
├── data.js          # 本地数据管理
├── api.js           # API服务模块
└── api-data.js      # 数据管理器
```

### 核心组件

#### API服务模块
```javascript
class ApiService {
    constructor() {
        this.baseURL = '/api';
    }
    
    async request(method, url, data = null) {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) options.body = JSON.stringify(data);
        return fetch(this.baseURL + url, options);
    }
}
```

#### 数据管理器
```javascript
class DataManager {
    constructor() {
        this.mode = 'offline'; // 'online' | 'offline'
        this.apiService = new ApiService();
    }
    
    async switchToOnlineMode() {
        try {
            await this.apiService.request('GET', '/health');
            this.mode = 'online';
            return true;
        } catch (error) {
            return false;
        }
    }
}
```

## ⚡ 后端架构

### FastAPI应用结构

#### 主应用配置
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="小雨微寒 API",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 数据模型示例
```python
from sqlalchemy import Column, Integer, String, Decimal, Date, Text

class FoodRecord(Base):
    __tablename__ = "food_records"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    rating = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text)
```

#### Pydantic模式
```python
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class FoodRecordCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    location: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    date: date
    notes: str = None
```

## 🔒 安全机制

### 输入验证
- Pydantic数据验证
- SQL注入防护（参数化查询）
- XSS防护（输入转义）
- 文件上传安全检查

### 数据安全
- 数据库访问控制
- 敏感信息加密
- 定期数据备份
- 访问日志记录

### 文件上传安全
```python
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_file(file: UploadFile):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {file_ext}")
    if file.size > MAX_FILE_SIZE:
        raise ValueError("文件大小超过限制")
```

## 📊 性能优化

### 数据库优化
- 合理创建索引
- 查询语句优化
- 连接池配置

### 前端优化
- 图片懒加载
- 防抖优化
- 缓存策略

### 缓存机制
- Redis缓存（可选）
- 内存缓存
- 浏览器缓存

## 🔧 部署配置

### 服务配置
```ini
# xiaoyuweihan-backend.service
[Unit]
Description=小雨微寒后端服务
After=network.target

[Service]
Type=exec
User=www
WorkingDirectory=/www/wwwroot/xiaoyuweihan/backend
Environment=PATH=/www/wwwroot/xiaoyuweihan/backend/venv/bin
ExecStart=/www/wwwroot/xiaoyuweihan/backend/venv/bin/gunicorn main:app -c gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx配置
```nginx
server {
    listen 80;
    server_name 47.105.52.49;
    
    # API路径代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 静态文件服务
    location / {
        root /www/wwwroot/xiaoyuweihan;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## 📝 开发规范

### 代码规范
- Python: 遵循PEP 8
- JavaScript: 使用驼峰命名
- CSS: 使用BEM命名规范
- 详细的中文注释

### Git提交规范
- feat: 新功能
- fix: 错误修复
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构

---

*本文档描述了小雨微寒项目的核心技术架构和实现细节*