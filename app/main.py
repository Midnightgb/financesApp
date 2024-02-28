from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.routes import user_router
from core.logger import Logger
from core.config import Settings
from api.v1.routes import test_connection


Logger.info("Starting API")

app = FastAPI(
    title=Settings.PROJECT_NAME,
    description=Settings.PROJECT_DESCRIPTION,
    version=Settings.PROJECT_VERSION,
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(test_connection.router, tags=["Test Connection"])
app.include_router(user_router.router, tags=["Users"])
