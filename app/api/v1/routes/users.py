from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
from core.utils import handle_server_down
from core.security import create_access_token
# API dependencies
from api.v1.schemas.users import UserRead, UserCreate, Token
from api.v1.crud.users import create_new_user, get_user_by_email, get_user_by_id, authenticate_user


router = APIRouter(
    prefix="/api/v1",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/users/create/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    user_info = get_user_by_email(user.mail, db)
    Logger.debug(f"Verifying user: {user.mail}")
    Logger.debug(f"User found: {user_info}")
    if user_info.get("status") is False:
        return create_new_user(user, db)
    else:
        raise HTTPException(
            status_code=409, detail="El email proporcionado ya está en uso.")


@router.get("/users/get/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    db_user = get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado.")
    return db_user


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Usuario o contraseña incorrectos.", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = create_access_token(data={"sub": user.user_id})
    return {"access_token": access_token_expires, "token_type": "bearer"}
