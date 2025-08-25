# 小雨微寒 - API接口文档

## 📋 目录

- [概述](#概述)
- [认证方式](#认证方式)
- [通用响应格式](#通用响应格式)
- [错误码说明](#错误码说明)
- [美食记录API](#美食记录api)
- [电影记录API](#电影记录api)
- [日历备注API](#日历备注api)
- [文件管理API](#文件管理api)
- [系统API](#系统api)

## 📖 概述

小雨微寒项目提供RESTful API接口，用于管理个人回忆数据，包括美食记录、电影记录、日历备注和文件管理等功能。

### 基本信息

- **基础URL**: `http://47.105.52.49/api`
- **API版本**: v1
- **数据格式**: JSON
- **字符编码**: UTF-8
- **在线文档**: `http://47.105.52.49/docs`

## 🔐 认证方式

当前版本暂未实现身份认证，所有接口均可直接访问。后续版本将添加Token认证机制。

## 📄 通用响应格式

### 成功响应

```json
{
    "success": true,
    "data": {
        // 具体业务数据
    },
    "message": "操作成功",
    "timestamp": "2025-01-15T10:30:00Z"
}
```

### 错误响应

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "错误描述信息",
        "details": {
            // 详细错误信息（可选）
        }
    },
    "timestamp": "2025-01-15T10:30:00Z"
}
```

## ❌ 错误码说明

| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| VALIDATION_ERROR | 422 | 数据验证失败 |
| NOT_FOUND | 404 | 资源不存在 |
| DUPLICATE_ENTRY | 409 | 数据重复 |
| DATABASE_ERROR | 500 | 数据库操作失败 |
| FILE_TOO_LARGE | 413 | 文件过大 |
| INVALID_FILE_TYPE | 415 | 无效文件类型 |

## 🍽️ 美食记录API

### 获取美食记录列表

**接口地址**: `GET /api/food/`

**请求参数**:

| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过记录数 |
| limit | int | 否 | 100 | 返回记录数限制 |
| rating | int | 否 | - | 按评分筛选(1-5) |
| location | string | 否 | - | 按地点筛选 |
| start_date | string | 否 | - | 开始日期(YYYY-MM-DD) |
| end_date | string | 否 | - | 结束日期(YYYY-MM-DD) |

**请求示例**:
```bash
GET /api/food/?skip=0&limit=10&rating=5
```

**响应示例**:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "麻辣火锅",
            "location": "海底捞火锅店",
            "price": 168.00,
            "rating": 5,
            "date": "2025-01-15",
            "notes": "和宝贝一起吃的，非常开心",
            "created_at": "2025-01-15T18:30:00Z",
            "updated_at": "2025-01-15T18:30:00Z"
        }
    ],
    "message": "获取成功"
}
```

### 创建美食记录

**接口地址**: `POST /api/food/`

**请求体**:
```json
{
    "name": "麻辣火锅",
    "location": "海底捞火锅店",
    "price": 168.00,
    "rating": 5,
    "date": "2025-01-15",
    "notes": "和宝贝一起吃的，非常开心"
}
```

**字段说明**:

| 字段 | 类型 | 必需 | 约束 | 说明 |
|------|------|------|------|------|
| name | string | 是 | 1-255字符 | 美食名称 |
| location | string | 是 | 1-255字符 | 用餐地点 |
| price | decimal | 是 | >0 | 价格 |
| rating | int | 是 | 1-5 | 评分 |
| date | string | 是 | YYYY-MM-DD | 用餐日期 |
| notes | string | 否 | - | 备注 |

**响应示例**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "麻辣火锅",
        "location": "海底捞火锅店",
        "price": 168.00,
        "rating": 5,
        "date": "2025-01-15",
        "notes": "和宝贝一起吃的，非常开心",
        "created_at": "2025-01-15T18:30:00Z",
        "updated_at": "2025-01-15T18:30:00Z"
    },
    "message": "创建成功"
}
```

### 获取单个美食记录

**接口地址**: `GET /api/food/{id}`

**路径参数**:
- `id`: 美食记录ID (int)

**响应示例**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "麻辣火锅",
        "location": "海底捞火锅店",
        "price": 168.00,
        "rating": 5,
        "date": "2025-01-15",
        "notes": "和宝贝一起吃的，非常开心",
        "created_at": "2025-01-15T18:30:00Z",
        "updated_at": "2025-01-15T18:30:00Z"
    },
    "message": "获取成功"
}
```

### 更新美食记录

**接口地址**: `PUT /api/food/{id}`

**路径参数**:
- `id`: 美食记录ID (int)

**请求体**: 同创建接口

**响应示例**: 同创建接口

### 删除美食记录

**接口地址**: `DELETE /api/food/{id}`

**路径参数**:
- `id`: 美食记录ID (int)

**响应示例**:
```json
{
    "success": true,
    "data": null,
    "message": "删除成功"
}
```

### 获取美食统计信息

**接口地址**: `GET /api/food/stats/summary`

**响应示例**:
```json
{
    "success": true,
    "data": {
        "total_records": 25,
        "total_spent": 2580.50,
        "average_price": 103.22,
        "average_rating": 4.2,
        "favorite_location": "海底捞火锅店",
        "most_expensive": {
            "name": "高档牛排",
            "price": 588.00
        },
        "rating_distribution": {
            "5": 10,
            "4": 8,
            "3": 5,
            "2": 2,
            "1": 0
        }
    },
    "message": "获取统计信息成功"
}
```

## 🎬 电影记录API

### 获取电影记录列表

**接口地址**: `GET /api/movie/`

**请求参数**:

| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过记录数 |
| limit | int | 否 | 100 | 返回记录数限制 |
| rating | int | 否 | - | 按评分筛选(1-5) |
| genre | string | 否 | - | 按类型筛选 |
| cinema | string | 否 | - | 按影院筛选 |

**响应示例**:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "阿凡达：水之道",
            "cinema": "万达影城",
            "date": "2025-01-15",
            "rating": 5,
            "review": "视觉效果震撼，情节感人",
            "genre": "科幻",
            "director": "詹姆斯·卡梅隆",
            "actors": "萨姆·沃辛顿, 佐伊·萨尔达娜",
            "created_at": "2025-01-15T20:30:00Z",
            "updated_at": "2025-01-15T20:30:00Z"
        }
    ],
    "message": "获取成功"
}
```

### 创建电影记录

**接口地址**: `POST /api/movie/`

**请求体**:
```json
{
    "name": "阿凡达：水之道",
    "cinema": "万达影城",
    "date": "2025-01-15",
    "rating": 5,
    "review": "视觉效果震撼，情节感人",
    "genre": "科幻",
    "director": "詹姆斯·卡梅隆",
    "actors": "萨姆·沃辛顿, 佐伊·萨尔达娜"
}
```

**字段说明**:

| 字段 | 类型 | 必需 | 约束 | 说明 |
|------|------|------|------|------|
| name | string | 是 | 1-255字符 | 电影名称 |
| cinema | string | 是 | 1-255字符 | 影院名称 |
| date | string | 是 | YYYY-MM-DD | 观影日期 |
| rating | int | 是 | 1-5 | 评分 |
| review | string | 否 | - | 影评 |
| genre | string | 否 | 1-100字符 | 电影类型 |
| director | string | 否 | 1-255字符 | 导演 |
| actors | string | 否 | - | 主演 |

### 按评分搜索电影

**接口地址**: `GET /api/movie/search/by-rating/{rating}`

**路径参数**:
- `rating`: 评分 (1-5)

**响应示例**: 同获取电影列表

## 📅 日历备注API

### 获取日历备注列表

**接口地址**: `GET /api/calendar/`

**请求参数**:

| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| start_date | string | 否 | - | 开始日期(YYYY-MM-DD) |
| end_date | string | 否 | - | 结束日期(YYYY-MM-DD) |
| is_important | bool | 否 | - | 是否重要 |
| keyword | string | 否 | - | 关键词搜索 |

**响应示例**:
```json
{
    "success": true,
    "data": [
        {
            "date": "2025-01-15",
            "note": "宝贝的生日，要准备惊喜",
            "is_important": true,
            "created_at": "2025-01-10T10:00:00Z",
            "updated_at": "2025-01-10T10:00:00Z"
        }
    ],
    "message": "获取成功"
}
```

### 创建日历备注

**接口地址**: `POST /api/calendar/`

**请求体**:
```json
{
    "date": "2025-01-15",
    "note": "宝贝的生日，要准备惊喜",
    "is_important": true
}
```

**字段说明**:

| 字段 | 类型 | 必需 | 约束 | 说明 |
|------|------|------|------|------|
| date | string | 是 | YYYY-MM-DD | 日期 |
| note | string | 是 | 非空 | 备注内容 |
| is_important | bool | 否 | - | 是否重要 |

### 获取指定日期备注

**接口地址**: `GET /api/calendar/{date}`

**路径参数**:
- `date`: 日期 (YYYY-MM-DD)

### 更新日期备注

**接口地址**: `PUT /api/calendar/{date}`

**路径参数**:
- `date`: 日期 (YYYY-MM-DD)

**请求体**: 同创建接口

### 删除日期备注

**接口地址**: `DELETE /api/calendar/{date}`

**路径参数**:
- `date`: 日期 (YYYY-MM-DD)

### 获取月份备注

**接口地址**: `GET /api/calendar/month/{year}/{month}`

**路径参数**:
- `year`: 年份 (int)
- `month`: 月份 (1-12)

**响应示例**:
```json
{
    "success": true,
    "data": {
        "year": 2025,
        "month": 1,
        "notes": [
            {
                "date": "2025-01-15",
                "note": "宝贝的生日",
                "is_important": true
            }
        ],
        "important_dates": ["2025-01-15"],
        "total_notes": 1
    },
    "message": "获取月份备注成功"
}
```

## 📁 文件管理API

### 获取文件列表

**接口地址**: `GET /api/files/`

**请求参数**:

| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| skip | int | 否 | 0 | 跳过记录数 |
| limit | int | 否 | 100 | 返回记录数限制 |
| file_type | string | 否 | - | 按文件类型筛选 |
| keyword | string | 否 | - | 关键词搜索 |

**响应示例**:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "filename": "12345678-90ab-cdef-1234-567890abcdef.jpg",
            "original_name": "我们的合照.jpg",
            "file_size": 2048576,
            "file_type": "image/jpeg",
            "file_path": "/uploads/12345678-90ab-cdef-1234-567890abcdef.jpg",
            "description": "在海边拍的照片",
            "created_at": "2025-01-15T14:30:00Z",
            "updated_at": "2025-01-15T14:30:00Z"
        }
    ],
    "message": "获取成功"
}
```

### 上传文件

**接口地址**: `POST /api/files/upload`

**请求方式**: `multipart/form-data`

**请求参数**:

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| file | file | 是 | 上传的文件 |
| description | string | 否 | 文件描述 |

**支持的文件类型**:
- 图片: `.jpg`, `.jpeg`, `.png`, `.gif`
- 文档: `.pdf`, `.doc`, `.docx`, `.txt`
- 其他: 根据需求扩展

**文件大小限制**: 10MB

**响应示例**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "filename": "12345678-90ab-cdef-1234-567890abcdef.jpg",
        "original_name": "我们的合照.jpg",
        "file_size": 2048576,
        "file_type": "image/jpeg",
        "file_path": "/uploads/12345678-90ab-cdef-1234-567890abcdef.jpg",
        "description": "在海边拍的照片",
        "download_url": "/api/files/download/1",
        "created_at": "2025-01-15T14:30:00Z"
    },
    "message": "上传成功"
}
```

### 下载文件

**接口地址**: `GET /api/files/download/{id}`

**路径参数**:
- `id`: 文件ID (int)

**响应**: 直接返回文件流

### 更新文件信息

**接口地址**: `PUT /api/files/{id}`

**路径参数**:
- `id`: 文件ID (int)

**请求体**:
```json
{
    "description": "更新后的文件描述"
}
```

### 删除文件

**接口地址**: `DELETE /api/files/{id}`

**路径参数**:
- `id`: 文件ID (int)

**响应示例**:
```json
{
    "success": true,
    "data": null,
    "message": "文件删除成功"
}
```

## 🔧 系统API

### 健康检查

**接口地址**: `GET /api/health`

**响应示例**:
```json
{
    "status": "healthy",
    "message": "服务运行正常",
    "timestamp": "2025-01-15T10:30:00Z",
    "version": "1.0.0",
    "database": "connected"
}
```

### API文档

**接口地址**: `GET /api/docs`

返回Swagger UI界面，提供交互式API文档。

### OpenAPI规范

**接口地址**: `GET /api/openapi.json`

返回完整的OpenAPI 3.0规范JSON文件。

## 📚 使用示例

### JavaScript示例

```javascript
// 创建美食记录
async function createFoodRecord(data) {
    try {
        const response = await fetch('/api/food/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (result.success) {
            console.log('创建成功:', result.data);
        } else {
            console.error('创建失败:', result.error);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 上传文件
async function uploadFile(file, description) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('description', description);
        
        const response = await fetch('/api/files/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('上传失败:', error);
        throw error;
    }
}
```

### Python示例

```python
import requests
import json

# API基础URL
BASE_URL = "http://47.105.52.49/api"

# 获取美食记录列表
def get_food_records():
    response = requests.get(f"{BASE_URL}/food/")
    return response.json()

# 创建美食记录
def create_food_record(data):
    response = requests.post(
        f"{BASE_URL}/food/",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    return response.json()

# 使用示例
food_data = {
    "name": "麻辣火锅",
    "location": "海底捞",
    "price": 168.00,
    "rating": 5,
    "date": "2025-01-15",
    "notes": "很好吃"
}

result = create_food_record(food_data)
print(result)
```

## 📝 注意事项

1. **日期格式**: 所有日期参数使用 `YYYY-MM-DD` 格式
2. **时间格式**: 所有时间戳使用 ISO 8601 格式
3. **文件上传**: 需要使用 `multipart/form-data` 格式
4. **错误处理**: 请检查响应中的 `success` 字段判断操作是否成功
5. **数据验证**: 所有必需字段必须提供，可选字段可以省略
6. **字符编码**: 请确保使用 UTF-8 编码处理中文内容

---

*更多详细信息请访问在线API文档: http://47.105.52.49/docs*