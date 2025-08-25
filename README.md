# 小雨微寒 - 个人回忆网站

> 一个用于记录美好回忆的个人网站，采用清新的浅蓝色和粉色设计风格

![项目状态](https://img.shields.io/badge/状态-已部署-green)
![技术栈](https://img.shields.io/badge/前端-HTML%2FCSS%2FJS-blue)
![后端](https://img.shields.io/badge/后端-Python%2FFastAPI-green)
![数据库](https://img.shields.io/badge/数据库-MySQL-orange)

## 📋 项目简介

小雨微寒是一个专为情侣记录美好回忆而设计的个人网站。网站以清新自然的浅蓝色和粉色为主色调，提供美食记录、电影记录、日历备注、文件暂存等功能，让每一个美好的瞬间都能被永久保存。

### 🌟 主要特色

- **📱 响应式设计** - 完美适配桌面端和移动端
- **💕 情感化设计** - 温馨的色彩搭配和优雅的动画效果
- **🗄️ 数据持久化** - 基于MySQL数据库的可靠存储
- **🎵 音乐播放器** - 可拖动的迷你音乐播放器
- **📅 智能日历** - 支持备注和重要日期标记
- **🍽️ 生活记录** - 美食和电影的详细记录管理

## 🏗️ 技术架构

### 前端技术栈
- **HTML5** - 语义化标记
- **CSS3** - 现代样式特性（Grid、Flexbox、CSS变量）
- **原生JavaScript** - 无框架依赖，纯净高效
- **响应式设计** - 移动端优先的布局策略

### 后端技术栈
- **Python 3.10** - 现代Python版本
- **FastAPI** - 高性能Web框架
- **Gunicorn** - WSGI生产服务器
- **SQLAlchemy** - ORM数据库操作
- **Pydantic** - 数据验证和序列化

### 基础设施
- **MySQL 5.7.40** - 关系型数据库
- **Nginx 1.26.1** - 反向代理和静态文件服务
- **systemd** - 服务管理
- **宝塔面板** - 服务器管理工具

## 📁 项目结构

```
XYWH20250821/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # 应用配置
│   │   ├── database.py        # 数据库连接
│   │   ├── models.py          # 数据模型
│   │   ├── schemas.py         # Pydantic模式
│   │   └── routers/           # API路由
│   │       ├── food.py        # 美食记录API
│   │       ├── movie.py       # 电影记录API
│   │       ├── calendar.py    # 日历备注API
│   │       └── files.py       # 文件管理API
│   ├── main.py                # FastAPI应用入口
│   ├── requirements.txt       # Python依赖
│   ├── gunicorn.conf.py      # Gunicorn配置
│   ├── deploy-baota.sh       # 宝塔部署脚本
│   └── xiaoyuweihan-backend.service  # systemd服务配置
├── scripts/                   # 前端JavaScript
│   ├── main.js               # 主要逻辑
│   ├── music.js              # 音乐播放器
│   ├── calendar.js           # 日历组件
│   ├── data.js               # 数据管理
│   ├── api.js                # API服务
│   └── api-data.js           # 数据管理器
├── styles/                    # 前端样式
│   ├── main.css              # 主要样式
│   ├── components.css        # 组件样式
│   └── responsive.css        # 响应式样式
├── logo/                      # 网站图标
├── background_music/          # 背景音乐
├── index.html                 # 主页文件
├── background.png             # 背景图片
├── qiuqiu1.jpg               # 纪念照片
└── README.md                  # 项目文档
```

## 🚀 快速开始

### 环境要求

- **服务器**: CentOS 7+ 或 Ubuntu 18+
- **Python**: 3.10+
- **MySQL**: 5.7+
- **Nginx**: 1.20+

### 本地开发

1. **克隆项目**
```bash
git clone <your-repo-url>
cd XYWH20250821
```

2. **启动前端**
```bash
# 使用Python简单服务器
python -m http.server 8000

# 访问 http://localhost:8000
```

3. **配置后端**
```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **配置数据库**
```bash
# 创建MySQL数据库
CREATE DATABASE xiaoyuweihan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **启动后端服务**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 生产部署

#### 宝塔面板部署（推荐）

1. **准备环境**
   - 安装宝塔面板
   - 安装MySQL 5.7+
   - 配置域名或使用IP访问

2. **部署项目**
```bash
# 上传项目到服务器
cd /www/wwwroot
git clone <your-repo-url> xiaoyuweihan

# 运行部署脚本
cd xiaoyuweihan/backend
chmod +x deploy-baota.sh
sudo ./deploy-baota.sh
```

3. **验证部署**
```bash
# 检查服务状态
systemctl status xiaoyuweihan-backend.service

# 测试API
curl http://your-domain/api/health
```

## 🎯 功能特色

### 时光计数器
- 实时计算恋爱天数
- 生日倒计时显示
- 自动更新机制

### 美食记录
- 详细的用餐信息记录
- 价格和评分管理
- 地点和备注功能
- 统计分析功能

### 电影记录
- 观影历史管理
- 评分和影评功能
- 影院信息记录
- 按评分筛选

### 日历备注
- 按日期管理备注
- 月份视图展示
- 关键词搜索
- 重要日期标记

### 文件暂存
- 多格式文件上传
- 分类管理系统
- 文件预览功能
- 安全下载机制

### 音乐播放器
- 可拖动迷你播放器
- 支持触摸操作
- 进度条控制
- 后台播放

### 球球纪念角
- 宠物纪念专区
- 温馨的文字内容
- 优美的动画效果
- 情感化设计

## 🛠️ 开发指南

### 代码规范

**前端规范**
- CSS使用BEM命名规范
- JavaScript使用驼峰命名
- 详细的中文注释
- 模块化组织结构

**后端规范**
- 遵循PEP 8代码规范
- 类型注解完整
- 详细的接口文档
- 完善的错误处理

### API接口

#### 美食记录
- `GET /api/food/` - 获取美食记录列表
- `POST /api/food/` - 创建美食记录
- `PUT /api/food/{id}` - 更新美食记录
- `DELETE /api/food/{id}` - 删除美食记录
- `GET /api/food/stats/summary` - 获取统计信息

#### 电影记录
- `GET /api/movie/` - 获取电影记录列表
- `POST /api/movie/` - 创建电影记录
- `PUT /api/movie/{id}` - 更新电影记录
- `DELETE /api/movie/{id}` - 删除电影记录
- `GET /api/movie/search/by-rating/{rating}` - 按评分搜索

#### 日历备注
- `GET /api/calendar/` - 获取日历备注列表
- `POST /api/calendar/` - 创建日历备注
- `PUT /api/calendar/{date}` - 更新日期备注
- `DELETE /api/calendar/{date}` - 删除日期备注
- `GET /api/calendar/month/{year}/{month}` - 获取月份备注

#### 文件管理
- `GET /api/files/` - 获取文件列表
- `POST /api/files/upload` - 上传文件
- `GET /api/files/download/{id}` - 下载文件
- `PUT /api/files/{id}` - 更新文件信息
- `DELETE /api/files/{id}` - 删除文件

### 数据库设计

#### 主要数据表

**美食记录表 (food_records)**
```sql
CREATE TABLE food_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**电影记录表 (movie_records)**
```sql
CREATE TABLE movie_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    cinema VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    genre VARCHAR(100),
    director VARCHAR(255),
    actors TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🎨 设计理念

### 色彩搭配
- **主色调**: 浅蓝色 (#E3F2FD) - 宁静清新
- **辅助色**: 粉色 (#FCE4EC) - 温馨浪漫
- **渐变效果**: 多层次渐变增强视觉层次
- **语义化颜色**: 成功绿、警告橙、错误红

### 交互设计
- **即时反馈**: 操作后立即显示状态
- **确认机制**: 重要操作前用户确认
- **加载状态**: 异步操作的视觉反馈
- **错误处理**: 友好的错误提示信息

### 响应式设计
- **移动端优先**: 从小屏幕开始设计
- **触摸优化**: 触摸按钮最小44px
- **弹性布局**: Grid和Flexbox布局
- **汉堡菜单**: 移动端侧边滑出菜单

## 🔧 运维管理

### 服务管理

**启动服务**
```bash
systemctl start xiaoyuweihan-backend.service
systemctl start nginx
```

**重启服务**
```bash
systemctl restart xiaoyuweihan-backend.service
systemctl reload nginx
```

**查看日志**
```bash
# 后端服务日志
journalctl -u xiaoyuweihan-backend.service -f

# Nginx访问日志
tail -f /www/wwwlogs/xiaoyuweihan_access.log

# Nginx错误日志
tail -f /www/wwwlogs/xiaoyuweihan_error.log
```

### 数据备份

**数据库备份**
```bash
mysqldump -u xiaoyuweihan -p xiaoyuweihan > backup_$(date +%Y%m%d_%H%M%S).sql
```

**文件备份**
```bash
tar -czf website_backup_$(date +%Y%m%d_%H%M%S).tar.gz /www/wwwroot/xiaoyuweihan
```

### 更新部署

**更新代码**
```bash
cd /www/wwwroot/xiaoyuweihan
git pull origin main

# 如果后端有更新
systemctl restart xiaoyuweihan-backend.service

# 如果前端有更新，清除浏览器缓存即可
```

## 🔒 安全配置

### 服务器安全
- SSH密钥认证
- 防火墙配置
- 定期安全更新
- 访问日志监控

### 应用安全
- SQL注入防护
- XSS攻击防护
- CSRF令牌验证
- 文件上传安全检查

### 数据安全
- 定期数据备份
- 数据库访问控制
- 敏感信息加密
- 访问权限管理

## 🐛 故障排除

### 常见问题

**后端服务无法启动**
```bash
# 检查Python环境
which python3.10
source /www/wwwroot/xiaoyuweihan/backend/venv/bin/activate

# 检查数据库连接
mysql -u xiaoyuweihan -p xiaoyuweihan

# 查看详细错误
journalctl -u xiaoyuweihan-backend.service -n 50
```

**Nginx配置问题**
```bash
# 测试Nginx配置
nginx -t

# 检查配置文件
cat /www/server/panel/vhost/nginx/47.105.52.49.conf

# 重新加载配置
nginx -s reload
```

**前端功能异常**
- 检查浏览器控制台错误
- 验证API接口响应
- 清除浏览器缓存
- 检查网络连接

## 📈 性能优化

### 前端优化
- 静态资源缓存
- 图片格式优化
- JavaScript代码压缩
- CSS样式合并

### 后端优化
- 数据库索引优化
- API响应缓存
- 连接池配置
- 异步处理优化

### 服务器优化
- Nginx配置调优
- 系统内核参数优化
- 磁盘I/O优化
- 内存使用优化

## 🤝 贡献指南

### 开发流程
1. Fork项目到个人仓库
2. 创建功能分支
3. 提交代码变更
4. 发起Pull Request
5. 代码审查和合并

### 提交规范
- feat: 新功能
- fix: 错误修复
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构

## 📞 技术支持

### 联系方式
- **项目地址**: http://47.105.52.49
- **API文档**: http://47.105.52.49/docs
- **健康检查**: http://47.105.52.49/api/health

### 问题反馈
如遇到问题，请按以下步骤进行排查：
1. 查看错误日志
2. 检查服务状态
3. 验证配置文件
4. 联系技术支持

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目贡献代码和想法的朋友们：Qoder & Trae。
---

*用代码记录爱情，让回忆永远闪闪发光 ✨*