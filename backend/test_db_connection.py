#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于验证宝塔数据库配置是否正确
"""

import sys
import pymysql
from app.config import settings

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    print(f"数据库主机: {settings.DB_HOST}")
    print(f"数据库端口: {settings.DB_PORT}")
    print(f"数据库用户: {settings.DB_USER}")
    print(f"数据库名称: {settings.DB_NAME}")
    print(f"数据库URL: {settings.database_url}")
    print("-" * 50)
    
    try:
        # 使用pymysql测试连接
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            charset='utf8mb4'
        )
        
        # 执行测试查询
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            print(f"✅ 数据库连接成功！测试查询结果: {result}")
            
            # 显示数据库信息
            cursor.execute("SELECT DATABASE(), VERSION(), USER()")
            db_info = cursor.fetchone()
            print(f"当前数据库: {db_info[0]}")
            print(f"MySQL版本: {db_info[1]}")
            print(f"当前用户: {db_info[2]}")
            
            # 检查数据库中的表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"数据库中的表: {[table[0] for table in tables]}")
            else:
                print("数据库中暂无表")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ 数据库连接失败!")
        print(f"错误代码: {e.args[0]}")
        print(f"错误信息: {e.args[1]}")
        
        # 提供解决建议
        print("\n💡 解决建议:")
        if e.args[0] == 1045:  # 认证失败
            print("1. 检查数据库用户名和密码是否正确")
            print("2. 确认宝塔面板中数据库用户xiaoyuweihan是否存在")
            print("3. 验证用户权限是否正确设置")
        elif e.args[0] == 2003:  # 连接被拒绝
            print("1. 检查MySQL服务是否正在运行")
            print("2. 验证数据库端口是否正确")
            print("3. 检查防火墙设置")
        elif e.args[0] == 1049:  # 数据库不存在
            print("1. 确认数据库xiaoyuweihan是否已创建")
            print("2. 检查数据库名称拼写是否正确")
        else:
            print("1. 检查MySQL服务状态: systemctl status mysql")
            print("2. 查看MySQL错误日志")
            print("3. 确认网络连接正常")
        
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)