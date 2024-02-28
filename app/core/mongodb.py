from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from .logger import Logger
from .config import get_settings
from contextlib import contextmanager

Logger.info("Database connection in progress...")
settings = get_settings()

if settings.MONGODB_URL is None:
    Logger.error("Database connection failed: No database URL provided")
    raise ValueError("Database URL not provided")


uri = settings.MONGODB_URL
Logger.info(f"Database uri: {uri}")
client = MongoClient(uri, server_api=ServerApi('1'))


@contextmanager
def get_database():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def server_status():
    try:
        client.admin.command('ping')  # Prueba de ping específica para MongoDB
        return True
    except OperationFailure:
        Logger.error("Database server status: ERROR")
        return False
