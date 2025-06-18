

import os
from functools import lru_cache
from pydantic_settings import BaseSettings  # type: ignore
from pathlib import Path
from dotenv import load_dotenv  # type: ignore

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # App
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-default-secret-key")

    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "http://localhost:3000")

    # SQLite Database Config
    SQLITE_DB_FILE: str = os.getenv("SQLITE_DB_FILE", "app.db")
    DATABASE_URI: str = f"sqlite:///{SQLITE_DB_FILE}"

    # Mailpit (local SMTP dev) Config
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 1025))
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@test.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "FastAPI App")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "False").lower() == "true"

    # Real SMTP Settings (e.g. Gmail)
    REAL_MAIL_ENABLED: bool = os.getenv("REAL_MAIL_ENABLED", "False").lower() == "true"
    REAL_MAIL_SERVER: str = os.getenv("REAL_MAIL_SERVER", "")
    REAL_MAIL_PORT: int = int(os.getenv("REAL_MAIL_PORT", 587))
    REAL_MAIL_USERNAME: str = os.getenv("REAL_MAIL_USERNAME", "")
    REAL_MAIL_PASSWORD: str = os.getenv("REAL_MAIL_PASSWORD", "")
    REAL_MAIL_FROM: str = os.getenv("REAL_MAIL_FROM", "")
    REAL_MAIL_FROM_NAME: str = os.getenv("REAL_MAIL_FROM_NAME", "")
    REAL_MAIL_TLS: bool = os.getenv("REAL_MAIL_TLS", "True").lower() == "true"

    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

@lru_cache()
def get_settings() -> Settings:
    return Settings()
