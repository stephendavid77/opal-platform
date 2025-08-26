from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Database URL (e.g., SQLite, PostgreSQL)
# For SQLite, use "sqlite:///./sql_app.db"
import os

# Construct the absolute path to the database file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
DATABASE_FILE = os.path.join(BASE_DIR, "shared", "database_base", "data", "opal_suite.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

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
