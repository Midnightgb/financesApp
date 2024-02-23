from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .logger import Logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from core.config import get_settings


Logger.info("Database connection in progress...")
settings = get_settings()

if settings.DATABASE_URL is None:
    Logger.error("Database connection failed: No database URL provided")
    raise ValueError("Database URL not provided")

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        Logger.warning("Closing database connection")
        database.close()


def server_status(db):
    try:
        db.execute(text('SELECT 1'))
        return True
    except OperationalError:
        Logger.error("Database server status: ERROR")
        return False
