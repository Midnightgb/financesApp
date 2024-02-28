from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    category_name: str
    category_description: Optional[str]


class CategoryCreate(CategoryBase):
    category_status: bool = True


class CategoryRead(CategoryBase):
    category_id: str
    category_status: bool
