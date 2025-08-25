from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Database URL (e.g., SQLite, PostgreSQL)
# For SQLite, use "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (
    "sqlite:///sqlite:///./opal_suite.db"  # Central database for OpalSuite
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
