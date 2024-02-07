from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
#Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
#API dependencies
from api.utils.handlers import handle_server_down
from api.v1.schemas.users import UserRead


router = APIRouter(
    prefix="/api/v1",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
