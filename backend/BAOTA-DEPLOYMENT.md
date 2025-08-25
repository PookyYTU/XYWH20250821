# 小雨微寒宝塔部署指南

## 宝塔环境部署步骤

### 前置条件
- ✅ 已安装宝塔面板
- ✅ 已安装MySQL 5.7+（通过宝塔面板安装）
- ✅ 服务器：47.105.52.49
- ✅ 数据库：xiaoyuweihan，密码：Duan1999

### 1. 拉取项目代码

在服务器上执行以下命令：

```bash
# 进入宝塔网站根目录
cd /www/wwwroot

# 从GitHub拉取项目（如果还没有拉取）
git clone <your-github-repo-url> xiaoyuweihan

# 或者如果已经有项目，更新代码
cd xiaoyuweihan
git pull origin main
```

### 2. 运行宝塔部署脚本

```bash
cd /www/wwwroot/xiaoyuweihan/backend

# 给脚本执行权限
chmod +x deploy-baota.sh

# 运行部署脚本
sudo ./deploy-baota.sh
```

脚本会自动完成：
- ✅ 检查宝塔环境
- ✅ 安装Python依赖
- ✅ 创建虚拟环境
- ✅ 配置数据库
- ✅ 设置系统服务
- ✅ 配置Nginx反向代理
- ✅ 启动所有服务

### 3. 宝塔面板配置

#### 3.1 网站配置
1. 登录宝塔面板
2. 进入"网站"管理
3. 你会看到自动配置的站点：`47.105.52.49`
4. 站点根目录：`/www/wwwroot/xiaoyuweihan`

#### 3.2 SSL配置（可选）
如果需要HTTPS：
1. 在宝塔面板的网站管理中点击你的站点
2. 进入"SSL"选项卡
3. 申请Let's Encrypt免费证书或上传自己的证书

#### 3.3 防火墙配置
确保以下端口开放：
- 80 (HTTP)
- 443 (HTTPS，如果使用SSL)
- 8000 (后端API，内部使用)

### 4. 验证部署

访问以下地址验证部署是否成功：

- **前端网站**: http://47.105.52.49/
- **API文档**: http://47.105.52.49/docs
- **健康检查**: http://47.105.52.49/api/health

### 5. 日常管理

#### 服务管理
```bash
# 查看后端服务状态
sudo systemctl status xiaoyuweihan-backend

# 重启后端服务
sudo systemctl restart xiaoyuweihan-backend

# 查看后端日志
sudo journalctl -u xiaoyuweihan-backend -f
```

#### 代码更新
```bash
cd /www/wwwroot/xiaoyuweihan

# 拉取最新代码
git pull origin main

# 如果后端代码有更新，重启后端服务
sudo systemctl restart xiaoyuweihan-backend

# 如果前端代码有更新，清除浏览器缓存即可
```

#### 数据库管理
可以通过宝塔面板的"数据库"功能管理：
- 查看表结构
- 备份数据库
- 导入/导出数据

### 6. 监控和维护

#### 日志文件位置
- **后端应用日志**: `/www/wwwroot/xiaoyuweihan/backend/logs/`
- **Nginx访问日志**: `/www/wwwlogs/xiaoyuweihan_access.log`
- **Nginx错误日志**: `/www/wwwlogs/xiaoyuweihan_error.log`

#### 定期维护
1. **数据库备份**：在宝塔面板设置自动备份
2. **日志清理**：定期清理旧的日志文件
3. **系统更新**：保持系统和软件包更新

### 7. 故障排除

#### 常见问题

**1. 后端服务无法启动**
```bash
# 查看详细错误信息
sudo journalctl -u xiaoyuweihan-backend -n 50

# 检查端口是否被占用
sudo netstat -tlnp | grep 8000
```

**2. 前端无法访问**
- 检查Nginx配置是否正确
- 确认项目文件是否完整
- 查看Nginx错误日志

**3. API调用失败**
- 检查后端服务是否正常运行
- 确认数据库连接是否正常
- 查看CORS配置

**4. 文件上传失败**
```bash
# 检查上传目录权限
ls -la /www/wwwroot/xiaoyuweihan/backend/uploads/

# 修复权限（如果需要）
sudo chown -R www:www /www/wwwroot/xiaoyuweihan/backend/uploads/
sudo chmod -R 755 /www/wwwroot/xiaoyuweihan/backend/uploads/
```

### 8. 性能优化

#### Nginx优化
在宝塔面板的Nginx配置中可以添加：
- Gzip压缩
- 静态文件缓存
- 连接池优化

#### 数据库优化
- 定期优化数据库表
- 添加必要的索引
- 监控慢查询

### 9. 安全配置

#### 建议安全措施
1. **修改默认端口**：可在宝塔面板修改SSH端口
2. **设置防火墙**：只开放必要端口
3. **定期更新**：保持系统和软件更新
4. **备份策略**：设置自动备份

## 宝塔部署优势

✅ **简单易用**：图形界面管理  
✅ **一键备份**：数据库和文件自动备份  
✅ **SSL证书**：免费申请和自动续期  
✅ **监控面板**：实时查看服务器状态  
✅ **日志管理**：集中的日志查看和管理  

---

## 联系支持

如遇到问题，可以：
1. 查看宝塔面板的系统日志
2. 检查本文档的故障排除部分
3. 联系技术支持

部署完成后，你的个人网站就可以正常访问了！🎉