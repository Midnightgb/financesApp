from fastapi import APIRouter
from core.logger import Logger
from core.database import get_database, server_status
from fastapi import Depends
from sqlalchemy.orm import Session
from core.utils import handle_server_down, handle_server_up

router = APIRouter(
    prefix="/api/v1",
    tags=["Test Connection"],
    responses={404: {"description": "Not found"}},
)


@router.get("/test_connection")
async def test_connection(db: Session = Depends(get_database)):
    if server_status(db):
        return handle_server_up()
    return handle_server_down()
