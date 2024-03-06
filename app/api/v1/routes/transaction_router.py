from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Core dependencies
from core.database import get_database, server_status
from core.logger import Logger
from core.utils import handle_server_down
# API dependencies
from api.v1.schemas.transaction import TransactionCreate, TransactionRead
from api.v1.crud.transactions import create_new_transaction, get_transaction_by_id, get_all_transactions, update_transaction, delete_transaction

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=TransactionRead)
async def create_transaction(
        transaction: TransactionCreate,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return create_new_transaction(transaction, db)


@router.get("/{transaction_id}/info", response_model=TransactionRead)
async def get_transaction(transaction_id: str, db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return get_transaction_by_id(transaction_id, db)


@router.get("/", response_model=list[TransactionRead])
async def get_transactions(
        db: Session = Depends(get_database),
        offset: int = 0,
        limit: int = 10,
        category_id: int = None,
        t_type: str = None):
    if not server_status(db):
        return handle_server_down()
    return get_all_transactions(db, offset, limit, category_id, t_type)


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transactions(
        transaction_id: str,
        transaction: TransactionCreate,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return update_transaction(transaction_id, transaction, db)


@router.delete("/{transaction_id}", response_model=dict)
async def delete_transactions(
        transaction_id: str,
        db: Session = Depends(get_database)):
    if not server_status(db):
        return handle_server_down()
    return delete_transaction(transaction_id, db)
