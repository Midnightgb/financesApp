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
    user_id: int
    user_role: UserRole
    user_status: bool
    created_at: datetime
    updated_at: datetime
