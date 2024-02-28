import os
from pathlib import Path
from dotenv import load_dotenv
from .logger import Logger
from pymongo import MongoClient

env_path = Path(".") / ".env"
prueba = os.path.join(os.path.dirname(__file__), '..', '.env')

load_dotenv()


class Settings():
    PROJECT_NAME: str = "Gastos-Ingresos"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Aplicación para el control de gastos e ingresos"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{
        DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    MGDB_USER: str = os.getenv("MGDP_USER")
    MGDB_PASS: str = os.getenv("MGDB_PASS")
    MGDB_CLUSTER: str = os.getenv("MGDB_CLUSTER")
    MGDB_APPNAME: str = os.getenv("MGDB_APPNAME")
    MONGODB_URL: str = f"mongodb+srv://{MGDB_USER}:{MGDB_PASS}@{MGDB_CLUSTER}.mongodb.net/?retryWrites=true&w=majority&appName={MGDB_APPNAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM: str = os.getenv("ALGORITHM")

    @classmethod
    def are_settings_valid(cls):
        invalid_settings = [attr for attr in dir(cls) if not callable(getattr(
            cls, attr)) and not attr.startswith("__") and getattr(cls, attr) is None]
        return invalid_settings[0] if invalid_settings else None


def get_settings() -> Settings:
    if not Settings.are_settings_valid():
        Logger.error(f"Error loading settings: {Settings.DATABASE_URL}")
        Logger.error(f"Error loading settings: {Settings.DB_USER}")
        Logger.error(f"Error loading settings: {Settings.DB_PASS}")
        Logger.error(f"Error loading settings: {Settings.DB_NAME}")
        Logger.error(f"Error loading settings: {Settings.DB_HOST}")
        Logger.error(f"Error loading settings: {Settings.DB_PORT}")
        Logger.error(f"Error loading settings: {Settings.MONGODB_URL}")
        Logger.error(f"Error loading settings: {Settings.MGDB_USER}")
        Logger.error(f"Error loading settings: {Settings.MGDB_PASS}")
        Logger.error(f"Error loading settings: {Settings.MGDB_CLUSTER}")
        Logger.error(f"Error loading settings: {Settings.MGDB_APPNAME}")
        Logger.error(f"Error loading settings: {Settings.SECRET_KEY}")
        Logger.error(f"Error loading settings: {Settings.TOKEN_EXPIRE_MINUTES}")
        Logger.error(f"Error loading settings: {Settings.ALGORITHM}")
    Logger.success(f"Settings loaded: {Settings.DATABASE_URL}")
    return Settings()
