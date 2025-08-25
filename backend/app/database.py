from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,  # 开发环境下打印SQL语句
    pool_pre_ping=True,   # 启用连接池健康检查
    pool_recycle=3600,    # 每小时重新创建连接
    pool_size=10,         # 连接池大小
    max_overflow=20       # 最大溢出连接数
)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()