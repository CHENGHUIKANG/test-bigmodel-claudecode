from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/user_db"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API配置
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"

settings = Settings()