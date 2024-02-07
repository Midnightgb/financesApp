from fastapi import FastAPI
from core.logger import Logger
from core.config import Settings
from api.v1.routes import test_connection, users


Logger.info("Starting API")

app = FastAPI(
    title=Settings.PROJECT_NAME,
    description=Settings.PROJECT_DESCRIPTION,
    version=Settings.PROJECT_VERSION,
)


@app.get("/")
async def root():
    return {"message": "API IS RUNNING"}


app.include_router(test_connection.router, tags=["Test Connection"])
app.include_router(users.router, tags=["Users"])
