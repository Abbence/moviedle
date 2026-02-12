from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL, DATABASE_VERBOSE_LOGGING

engine = create_engine(DATABASE_URL, echo=DATABASE_VERBOSE_LOGGING)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()