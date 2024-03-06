from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.v1.models.category import Category
from api.v1.schemas.category import CategoryCreate, CategoryRead

from core.database import server_status
from core.logger import Logger
from core.utils import handle_server_down


def create_new_category(category: CategoryCreate, db: Session):
    if not server_status(db):
        return handle_server_down()
    try:
        category_info = db.query(Category).filter(
            Category.category_name == category.category_name).first()
        if category_info:
            raise HTTPException(
                status_code=404, detail="La categoría ya existe.")
    except Exception as e:
        Logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=404, detail="Error creando la categoría.")
    try:
        new_category = Category(
            category_name=category.category_name,
            category_description=category.category_description,
            category_status=category.category_status,
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as e:
        Logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=404, detail="Error creando la categoría.")


def get_category_by_id(category_id: str, db: Session):
    if not server_status(db):
        return handle_server_down()
    category = db.query(Category).filter(
        Category.category_id == category_id).first()
    if category:
        return category
    else:
        raise HTTPException(
            status_code=404, detail="Categoría no encontrada.")


def get_all_categories(db: Session, offset: int = 0, limit: int = 10):
    if not server_status(db):
        return handle_server_down()
    categories = db.query(Category).offset(offset).limit(limit).all()
    return categories


def update_category(category_id: str, category: CategoryCreate, db: Session):
    if not server_status(db):
        return handle_server_down()
    category_data = get_category_by_id(category_id, db)
    if category_data:
        category_data.category_name = category.category_name
        category_data.category_description = category.category_description
        category_data.category_status = category.category_status
        db.commit()
        return category_data
    else:
        raise HTTPException(
            status_code=404, detail="Categoría no encontrada.")


def delete_category(category_id: str, db: Session):
    if not server_status(db):
        return handle_server_down()
    category = get_category_by_id(category_id, db)
    if category:
        category.category_status = False
        db.commit()
        db.refresh(category)
        return category
    else:
        raise HTTPException(
            status_code=404, detail="Categoría no encontrada.")
