from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    full_name: str
    mail: EmailStr


class UserCreate(UserBase):
    passhash: str
    user_role: UserRole
    user_status: bool = True


class UserCreate(UserBase):
    passhash: str
    user_role: UserRole
    user_status: bool = True


class UserRead(UserBase):
    user_id: str
    user_role: UserRole
    user_status: bool
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
    # Cuando orm_mode esta habilitado, Pydantic permitirá pasar objetos SQLAlchemy directamente a los modelos Pydantic sin necesidad de definir explícitamente los campos.
