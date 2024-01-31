from fastapi import APIRouter
from logger.Logger import Logger
from db.connection import get_database, server_status
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/test_connection")
def test_connection(db: Session = Depends(get_database)):
    if server_status(db):
        return {
            "status": "true",
            "message": "Database connection successful"}
    return {
        "status": "true",
        "message": "Database connection failed"}
