from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from sqlalchemy import create_engine
from app.core.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URI,
    connect_args={"check_same_thread": False}  # Needed only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
