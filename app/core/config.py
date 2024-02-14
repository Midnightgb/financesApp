import os
from pathlib import Path
from dotenv import load_dotenv
from .logger import Logger

env_path = Path(".") / ".env"

load_dotenv(dotenv_path=env_path)


class Settings():
    PROJECT_NAME: str = "Gastos-Ingresos"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Apliación para el control de gastos e ingresos"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{
        DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_EXPIRE_MINUTES: 30
    ALGORITHM: str = os.getenv("ALGORITHM")


def get_settings() -> Settings:
    Logger.debug("Loading settings from the environment")

    if "None" in Settings.DATABASE_URL:
        Logger.error("Settings not loaded: Database connection failed")
        raise ValueError("Database connection failed")

    Logger.success(f"Settings loaded: {Settings.DATABASE_URL}")
    return Settings()
