#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于验证数据库配置是否正确
"""

import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """测试数据库连接"""
    print("🔍 开始数据库连接测试...")
    print("=" * 50)
    
    try:
        # 导入配置和数据库模块
        from app.config import settings
        from app.database import engine, test_connection, create_tables
        from app.models import Base
        
        # 显示配置信息（隐藏敏感信息）
        print(f"📊 数据库配置信息:")
        print(f"   主机: {settings.db_host}")
        print(f"   端口: {settings.db_port}")
        print(f"   数据库: {settings.db_name}")
        print(f"   用户: {settings.db_user}")
        print(f"   密码: {'*' * len(settings.db_password)}")
        print()
        
        # 测试连接
        print("🔗 测试数据库连接...")
        if test_connection():
            print("✅ 数据库连接成功!")
        else:
            print("❌ 数据库连接失败!")
            return False
        
        # 获取数据库版本信息
        print("\n📋 数据库信息:")
        with engine.connect() as conn:
            result = conn.execute("SELECT VERSION() as version")
            version = result.fetchone()[0]
            print(f"   MySQL版本: {version}")
            
            # 检查数据库编码
            result = conn.execute(
                "SELECT @@character_set_database as charset, @@collation_database as collation"
            )
            charset_info = result.fetchone()
            print(f"   字符集: {charset_info[0]}")
            print(f"   排序规则: {charset_info[1]}")
        
        # 创建数据库表
        print("\n🗄️ 创建数据库表...")
        try:
            create_tables()
            print("✅ 数据库表创建成功!")
        except Exception as e:
            print(f"⚠️ 数据库表创建警告: {e}")
        
        # 检查表是否存在
        print("\n📝 检查数据表:")
        with engine.connect() as conn:
            result = conn.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = %s AND table_type = 'BASE TABLE'",
                (settings.db_name,)
            )
            tables = [row[0] for row in result]
            
            expected_tables = [
                'food_records', 'movie_records', 'calendar_notes', 
                'file_records', 'system_logs'
            ]
            
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table} (缺失)")
        
        # 测试基本数据操作
        print("\n🧪 测试基本数据操作...")
        test_basic_operations()
        
        print("\n" + "=" * 50)
        print("🎉 数据库测试完成!")
        print(f"⏰ 测试时间: {datetime.now()}")
        return True
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所需依赖: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False


def test_basic_operations():
    """测试基本的数据库操作"""
    try:
        from app.database import SessionLocal
        from app.models import FoodRecord, MovieRecord, CalendarNote
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 测试插入和查询
            print("   🔍 测试数据插入...")
            
            # 创建测试美食记录
            test_food = FoodRecord(
                name="测试美食",
                location="测试地点",
                rating=8.5,
                description="这是一个测试记录"
            )
            db.add(test_food)
            db.commit()
            db.refresh(test_food)
            
            # 查询测试记录
            found_food = db.query(FoodRecord).filter(FoodRecord.name == "测试美食").first()
            if found_food:
                print("   ✅ 数据插入和查询成功")
                
                # 删除测试记录
                db.delete(found_food)
                db.commit()
                print("   ✅ 数据删除成功")
            else:
                print("   ❌ 数据查询失败")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"   ⚠️ 基本操作测试警告: {e}")


def show_help():
    """显示帮助信息"""
    print("数据库连接测试脚本")
    print("=" * 30)
    print("用法:")
    print("  python test_db_connection.py        # 运行完整测试")
    print("  python test_db_connection.py --help # 显示帮助")
    print()
    print("功能:")
    print("  - 测试数据库连接")
    print("  - 检查数据库版本和编码")
    print("  - 创建数据库表")
    print("  - 验证表结构")
    print("  - 测试基本数据操作")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        show_help()
    else:
        success = test_database_connection()
        sys.exit(0 if success else 1)