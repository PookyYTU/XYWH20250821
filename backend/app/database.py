# -*- coding: utf-8 -*-
"""
数据库连接和会话管理
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging

from app.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库引擎配置
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.debug,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False
    }
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基础模型类
Base = declarative_base()

# 元数据
metadata = MetaData()


def get_db() -> Session:
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """创建所有数据库表"""
    try:
        logger.info("正在创建数据库表...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库表创建完成")
    except Exception as e:
        logger.error(f"❌ 创建数据库表失败: {e}")
        raise


def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("✅ 数据库连接测试成功")
            return True
    except Exception as e:
        logger.error(f"❌ 数据库连接测试失败: {e}")
        return False


if __name__ == "__main__":
    # 测试数据库连接
    test_connection()