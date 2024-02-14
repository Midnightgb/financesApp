from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
from core.utils import handle_server_down
from core.security import create_access_token, verify_token
# API dependencies
from api.v1.schemas.users import UserRead, UserCreate, Token
from api.v1.crud.users import create_new_user, get_user_by_email, get_user_by_id, authenticate_user


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
# OAuth2 scheme for token authentication and user verification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    user_id = await verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=401, detail="Invalid token")
    user_data = get_user_by_id(user_id, db)
    if user_data is None:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado.")
    return user_data


@router.post("/create/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    user_info = get_user_by_email(user.mail, db)
    Logger.debug(f"Verifying user: {user.mail}")
    Logger.debug(f"User found: {user_info}")
    if user_info.get("status") is False:
        Logger.debug(f"Creating new user: {user.mail}")
        return create_new_user(user, db)
    else:
        raise HTTPException(
            status_code=404, detail="El email proporcionado ya está en uso.")


@router.get("/get/{user_id}", response_model=UserRead)
async def read_user(user_id: str, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    # Check if the user is an admin
    if current_user.user_role == "admin" or current_user.user_id == user_id:
        user = get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado.")
        return user
    else:
        raise HTTPException(
            status_code=403, detail="No tiene permisos para ver este usuario.")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    # Authenticate the user and return the access token 
    # form_data is a dict with the username and password
    user = authenticate_user(form_data.username, form_data.password, db)
    if "status" in user and not user["status"]:
        Logger.error(user.get("message"))
        raise HTTPException(
            status_code=401, detail=f"{user.get("message")}", headers={"WWW-Authenticate": "Bearer"})
    user = user.get("user")
    access_token_expires = create_access_token(
        data={"sub": user.user_id})
    return {"access_token": access_token_expires, "token_type": "bearer"}
