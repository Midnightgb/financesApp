from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
from core.utils import handle_server_down
# API dependencies
from api.v1.schemas.category import CategoryCreate, CategoryRead
from api.v1.crud.categories import create_new_category, get_category_by_id, get_all_categories, update_category, delete_category

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create/", response_model=CategoryRead)
async def create_category(
        category: CategoryCreate,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return create_new_category(category, db)


@router.get("/{category_id}/info", response_model=CategoryRead)
async def get_category(category_id: str, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return get_category_by_id(category_id, db)


@router.get("/", response_model=list[CategoryRead])
async def get_categories(
        db: Session = Depends(get_database),
        offset: int = 0, limit: int = 10):
    if not server_status(db):
        return handle_server_down()
    return get_all_categories(db, offset, limit)


@router.put("/update/{category_id}", response_model=CategoryRead)
async def update_category_data(
        category_id: str,
        category: CategoryCreate,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return update_category(category_id, category, db)


@router.delete("/delete/{category_id}", response_model=CategoryRead)
async def delete_category_data(
        category_id: str,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return delete_category(category_id, db)

