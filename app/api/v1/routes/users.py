from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
#Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
from core.utils import handle_server_down
#API dependencies
from api.v1.schemas.users import UserRead, UserCreate
from api.v1.models.User import User
from api.v1.crud.users import create_new_user, get_user_by_email


router = APIRouter(
    prefix="/api/v1",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
@router.post("/users/create/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    verify_user = get_user_by_email(user.mail, db)
    if verify_user is None:
        return create_new_user(user, db)
    else:
        raise HTTPException(status_code=400, detail="El email proporcionado ya está en uso.")


@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
