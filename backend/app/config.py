from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    DEBUG: bool = True
    SECRET_KEY: str = "xiaoyuweihan_secret_key_2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "xiaoyuweihan"  # 宝塔创建的专用数据库用户
    DB_PASSWORD: str = "Duan1999"
    DB_NAME: str = "xiaoyuweihan"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50000000  # 50MB
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.gif,.bmp,.webp,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.md,.mp3,.mp4,.avi,.mov,.zip,.rar"
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://47.105.52.49",
        "http://47.105.52.49:8000",
        "http://47.105.52.49:80",
        "http://47.105.52.49:443",
        "*"  # 开发环境允许所有来源
    ]
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        """数据库连接URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """允许的文件扩展名列表"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

settings = Settings()