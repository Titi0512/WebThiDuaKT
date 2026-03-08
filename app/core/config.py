from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Hệ thống quản lý khen thưởng - Trường Sĩ quan Chính trị"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database settings (MariaDB)
    # Format: mysql+pymysql://username:password@host:port/database?charset=utf8mb4
    # Note: PyMySQL works with MariaDB (MariaDB is MySQL-compatible)
    # DATABASE_URL: str = "mysql+pymysql://'root':'1111'@localhost:3306/khen_thuong_db"
  #  DATABASE_URL=sqlite:///./demo.db
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env.example"
        case_sensitive = True


settings = Settings()
