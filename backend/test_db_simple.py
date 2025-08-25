#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版数据库连接测试脚本
不依赖pydantic配置，直接测试数据库连接
"""

import pymysql
import sys

# 数据库配置（直接写入，避免pydantic问题）
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'xiaoyuweihan',
    'password': 'Duan1999',
    'database': 'xiaoyuweihan',
    'charset': 'utf8mb4'
}

def test_database_connection():
    """测试数据库连接"""
    print("🔍 简化版数据库连接测试...")
    print(f"数据库主机: {DB_CONFIG['host']}")
    print(f"数据库端口: {DB_CONFIG['port']}")
    print(f"数据库用户: {DB_CONFIG['user']}")
    print(f"数据库名称: {DB_CONFIG['database']}")
    print("-" * 50)
    
    try:
        # 使用pymysql测试连接
        connection = pymysql.connect(**DB_CONFIG)
        
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
                
            # 测试创建表的权限
            try:
                cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)")
                cursor.execute("DROP TABLE test_table")
                print("✅ 用户拥有创建和删除表的权限")
            except Exception as e:
                print(f"⚠️  用户权限受限: {str(e)}")
        
        connection.close()
        print("\n🎉 数据库配置正确，可以继续部署！")
        return True
        
    except pymysql.Error as e:
        print(f"❌ 数据库连接失败!")
        print(f"错误代码: {e.args[0]}")
        print(f"错误信息: {e.args[1]}")
        
        # 提供解决建议
        print("\n💡 解决建议:")
        if e.args[0] == 1045:  # Access denied
            print("1. 检查用户名和密码是否正确")
            print("2. 尝试使用以下命令测试:")
            print(f"   mysql -u {DB_CONFIG['user']} -p")
            print("3. 如果上述命令失败，可能需要:")
            print("   - 在宝塔面板中创建用户xiaoyuweihan")
            print("   - 或者修改配置使用root用户")
        elif e.args[0] == 2003:  # Can't connect
            print("1. 检查MySQL服务状态: systemctl status mysql")
            print("2. 检查MySQL端口是否开放: netstat -tlnp | grep 3306")
        elif e.args[0] == 1049:  # Unknown database
            print("1. 检查数据库是否存在: SHOW DATABASES;")
            print("2. 在宝塔面板中创建数据库xiaoyuweihan")
        
        print(f"\n🔧 如果使用root用户，请修改以下配置:")
        print(f"   用户名: root")
        print(f"   密码: Duan1999")
        
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n✅ 建议：现在可以运行部署脚本 sudo ./deploy-baota.sh")
    else:
        print("\n❌ 建议：先解决数据库连接问题，再运行部署脚本")
    sys.exit(0 if success else 1)