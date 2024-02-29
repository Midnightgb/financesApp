from fastapi import APIRouter
from core.logger import Logger
from core.database import get_database, server_status
from fastapi import Depends
from sqlalchemy.orm import Session
from core.utils import handle_server_down, handle_server_up
from core.mongodb import get_mongodb, server_status_mongodb

router = APIRouter(
    prefix="/api/v1",
    tags=["Test Connection"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health_check")
async def health_check(db: Session = Depends(get_database)):
    if server_status(db):
        return handle_server_up()
    return handle_server_down()


@router.get("/health_check_mongo")
async def health_check_mongo():
    if server_status_mongodb():
        return handle_server_up()
    return handle_server_down()
