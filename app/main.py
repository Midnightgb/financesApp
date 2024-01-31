from fastapi import FastAPI
from starlette.requests import Request
import os
from dotenv import load_dotenv
from logger.Logger import Logger
from api.v1.routes import test_connection

load_dotenv()

Logger.info("Starting API")

app = FastAPI()

@app.get("/")
def root(request: Request):
    return {"message": "API IS RUNNING"}

app.include_router(test_connection.router, tags=["Test Connection"])
