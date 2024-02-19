import sys
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.v1.models.user import User
from api.v1.schemas.users import UserRead, UserCreate

from core.database import server_status
from core.logger import Logger
from core.utils import handle_server_down, generate_user_id
from core.security import get_hashed_password, verify_password


def create_new_user(user: UserCreate, rol: str, db: Session):
    db_user = User(
        user_id=generate_user_id(),
        full_name=user.full_name,
        mail=user.mail,
        passhash=get_hashed_password(user.passhash),
        user_role=rol,
        user_status=user.user_status
    )
    try:
        if not server_status(db):
            return handle_server_down()
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        Logger.error(f"Error creating new user: {str(e)}", file=sys.stderr)
        raise HTTPException(
            status_code=500, detail=f"Error al crear el usuario: {str(e)}")


def get_user_by_email(email: str, db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        user = db.query(User).filter(User.mail == email).first()
        if user:
            return {"status": True, "user": user}
        return {"status": False, "message": "No se encontró el usuario con el email proporcionado."}
    except Exception as e:
        Logger.error(f"Error getting user by email: {str(e)}", file=sys.stderr)
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el usuario por email: {str(e)}")


def get_user_by_id(user_id: str, db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        user = db.query(User).filter(User.user_id == user_id).first()
        return user
    except Exception as e:
        Logger.error(f"Error getting user by id: {str(e)}", file=sys.stderr)
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el usuario por id: {str(e)}")


def authenticate_user(email: str, password: str, db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        user = db.query(User).filter(User.mail == email).first()
        if user:
            if verify_password(password, user.passhash):
                return {"status": True, "user": user}
            return {"status": False, "message": "Contraseña incorrecta."}
        return {"status": False, "message": "No se encontró el usuario con el email proporcionado."}
    except Exception as e:
        Logger.error(f"Error authenticating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al autenticar el usuario: {str(e)}")


def check_user_permissions(current_user: UserRead, user_id: str):
    if current_user.user_role == "admin" or current_user.user_id == user_id:
        return True
    return False


def update_user(user_id: str, user: UserRead, current_user_role: str, db: Session):
    try:
        if not server_status(db):
            return handle_server_down()

        db_user = db.query(User).filter(User.user_id == user_id).first()
        db_user.full_name = user.full_name
        db_user.mail = user.mail
        db_user.user_status = user.user_status

        if current_user_role == "admin":
            db_user.user_role = user.user_role
            
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        Logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")
