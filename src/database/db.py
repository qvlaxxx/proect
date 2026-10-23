# src/database/db.py
from sqlalchemy import select, Integer, String, create_engine, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///skills.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
