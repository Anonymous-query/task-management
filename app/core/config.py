from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    project_name: str = "Task Manager API"
    version: str = "1.0.0"
    description: str = "A comprehensive task management API with JWT authentication"
    
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()