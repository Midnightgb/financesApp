from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.v1.routes import user_router, category_router, health_check
from core.logger import Logger
from core.config import Settings


Logger.info("Starting API")

app = FastAPI(
    title=Settings.PROJECT_NAME,
    description=Settings.PROJECT_DESCRIPTION,
    version=Settings.PROJECT_VERSION,
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(health_check.router, tags=["Test Connection"])
app.include_router(user_router.router, tags=["Users"])
app.include_router(category_router.router, tags=["Categories"])
