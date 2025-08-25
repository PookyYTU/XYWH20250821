# 小雨微寒 - Memory 💕

> 一个温馨的个人网站，记录生活中的美好时光

## 项目介绍

小雨微寒是一个个人纪念网站，用于记录生活中的美食、电影、重要日期和文件。包含前端展示和后端API服务。

### 主要功能

- 🍽️ **美食记录** - 记录品尝过的美食，包括地点、价格、评分等
- 🎬 **电影记录** - 记录观看过的电影，包括影院、评分、影评等  
- 📅 **时光日历** - 日历备注功能，记录特殊的日子
- 📁 **文件暂存** - 上传和管理各类文件
- 🎵 **音乐播放** - 背景音乐播放功能
- 💕 **时光计数** - 相恋天数和生日倒计时

## 技术栈

### 前端
- **HTML5** + **CSS3** + **原生JavaScript**
- **响应式设计** - 支持移动端访问
- **PWA特性** - 支持离线访问

### 后端
- **Python 3.8+**
- **FastAPI** - 现代、快速的API框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL 5.7+** - 数据存储
- **Gunicorn** - WSGI服务器

### 部署
- **Nginx** - 反向代理和静态文件服务
- **systemd** - 服务管理
- **Ubuntu/CentOS** - 服务器环境

## 项目结构

```
xiaoyuweihan/
├── index.html              # 主页面
├── styles/                 # CSS样式文件
│   ├── main.css
│   ├── components.css
│   └── responsive.css
├── scripts/                # JavaScript脚本
│   ├── main.js            # 主要功能
│   ├── api.js             # API服务
│   ├── api-data.js        # 数据管理
│   ├── calendar.js        # 日历功能
│   ├── music.js           # 音乐播放
│   └── data.js            # 原数据管理（兼容）
├── logo/                   # 图标和Logo
├── background_music/       # 背景音乐
├── backend/               # 后端API服务
│   ├── main.py            # FastAPI主应用
│   ├── app/               # 应用模块
│   │   ├── config.py      # 配置管理
│   │   ├── database.py    # 数据库连接
│   │   ├── models.py      # 数据模型
│   │   ├── schemas.py     # Pydantic模式
│   │   └── routers/       # API路由
│   │       ├── food.py    # 美食API
│   │       ├── movie.py   # 电影API
│   │       ├── calendar.py # 日历API
│   │       └── files.py   # 文件API
│   ├── requirements.txt   # Python依赖
│   ├── .env              # 环境配置
│   ├── gunicorn.conf.py  # Gunicorn配置
│   ├── nginx.conf        # Nginx配置
│   ├── deploy.sh         # 部署脚本
│   └── DEPLOYMENT.md     # 部署文档
└── README.md             # 项目说明
```

## 快速开始

### 开发环境

1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd xiaoyuweihan
   ```

2. **前端开发**
   ```bash
   # 直接在浏览器中打开 index.html
   # 或使用简单的HTTP服务器
   python -m http.server 8080
   ```

3. **后端开发**
   ```bash
   cd backend
   
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 文件设置数据库配置
   
   # 启动开发服务器
   python main.py
   ```

4. **数据库配置**
   ```sql
   CREATE DATABASE xiaoyuweihan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 生产环境部署

#### 方案1：宝塔面板部署（推荐）

如果你使用宝塔面板，可以快速部署：

```bash
# 1. 拉取项目到宝塔目录
cd /www/wwwroot
git clone <your-repo-url> xiaoyuweihan

# 2. 运行宝塔部署脚本
cd xiaoyuweihan/backend
sudo chmod +x deploy-baota.sh
sudo ./deploy-baota.sh
```

详细指南：[backend/BAOTA-DEPLOYMENT.md](backend/BAOTA-DEPLOYMENT.md)

#### 方案2：传统部署

详细部署指南请查看：[backend/DEPLOYMENT.md](backend/DEPLOYMENT.md)

**快速部署**（适用于Ubuntu/CentOS）：
```bash
cd backend
sudo chmod +x deploy.sh
sudo ./deploy.sh
```

## API文档

后端服务启动后，可通过以下地址查看API文档：
- **Swagger UI**: http://your-server:8000/docs
- **ReDoc**: http://your-server:8000/redoc

### 主要API端点

- `GET /api/health` - 健康检查
- `GET /api/food/` - 获取美食记录
- `POST /api/food/` - 创建美食记录
- `GET /api/movie/` - 获取电影记录
- `POST /api/movie/` - 创建电影记录
- `GET /api/calendar/` - 获取日历备注
- `PUT /api/calendar/{date}` - 创建/更新日历备注
- `POST /api/files/upload` - 上传文件
- `GET /api/files/download/{file_id}` - 下载文件

## 配置说明

### 环境变量配置

在 `backend/.env` 文件中配置：

```env
# 基础配置
DEBUG=False
SECRET_KEY=your-secret-key

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=xiaoyuweihan

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=50000000

# CORS配置
ALLOWED_ORIGINS=http://your-domain.com
```

## 功能特性

### 离线支持
- 前端支持离线访问
- 网络断开时自动切换到本地存储
- 网络恢复时自动同步数据

### 响应式设计
- 完美适配手机、平板、桌面设备
- 移动端优化的交互体验

### 数据安全
- API接口身份验证
- 文件上传类型限制
- SQL注入防护

### 性能优化
- 静态文件缓存
- 数据库连接池
- Gzip压缩

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

此项目为个人项目，仅供学习和参考使用。

## 联系方式

如有问题或建议，欢迎联系：
- 📧 Email: your-email@example.com
- 🌐 Website: http://47.105.52.49

---

**小雨微寒 - 记录每一个美好瞬间** 💕