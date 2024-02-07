from fastapi import FastAPI
from core.logger import Logger
from api.v1.routes import test_connection


Logger.info("Starting API")

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API IS RUNNING"}


app.include_router(test_connection.router, tags=["Test Connection"])
