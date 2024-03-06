from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from api.v1.models.transaction import Transaction
from api.v1.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete

from core.database import server_status
from core.logger import Logger
from core.utils import handle_server_down


def create_new_transaction(
        transaction: TransactionCreate,
        db: Session):
    db_transaction = Transaction(
        amount=transaction.amount,
        t_description=transaction.t_description,
        t_type=transaction.t_type,
        t_date=transaction.t_date,
        user_id=transaction.user_id,
        category_id=transaction.category_id
    )
    try:
        if not server_status(db):
            return handle_server_down()
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        Logger.error(f"Error creating new transaction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al crear la transacción: {str(e)}")
    
def get_transaction_by_id(
        transaction_id: int,
        db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        transaction = db.query(Transaction).filter(Transaction.transactions_id == transaction_id).first()
        if transaction:
            return transaction
        return None
    except Exception as e:
        Logger.error(f"Error getting transaction by id: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al obtener la transacción por id: {str(e)}")
    
def get_all_transactions(
        db: Session,
        offset: int = 0, 
        limit: int = 10,
        category_id: int = None,
        t_type: str = None):
    try:
        if not server_status(db):
            return handle_server_down()
        query = db.query(Transaction)
        conditions = []
        if category_id:
            conditions.append(Transaction.category_id == category_id)
        if t_type:
            conditions.append(Transaction.t_type == t_type)
        if conditions:
            query = query.filter(and_(*conditions))
        transactions = query.offset(offset).limit(limit).all()
        return transactions
    except Exception as e:
        Logger.error(f"Error getting all transactions: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al obtener todas las transacciones: {str(e)}")
    
def update_transaction(
        transaction_id: int,
        transaction: TransactionUpdate,
        db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        db_transaction = db.query(Transaction).filter(Transaction.transactions_id == transaction_id).first()
        if db_transaction:
            db_transaction.amount = transaction.amount
            db_transaction.t_description = transaction.t_description
            db_transaction.t_type = transaction.t_type
            db_transaction.t_date = transaction.t_date
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        return None
    except Exception as e:
        db.rollback()
        Logger.error(f"Error updating transaction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar la transacción: {str(e)}")

    

""" from pydantic import BaseModel
from enum import Enum
from datetime import date

class TransactionType(Enum):
    revenue = "revenue"
    expenses = "expenses"

class TransactionBase(BaseModel):
    amount: float
    t_description: str
    t_type: TransactionType
    t_date: date

class TransactionRead(TransactionBase):
    transactions_id: int
    user_id: str
    category_id: int

class TransactionCreate(TransactionRead):
    pass

class TransactionUpdate(TransactionRead):
    pass

class TransactionDelete(BaseModel):
    transactions_id: int
 """