from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func

from api.v1.models.transaction import Transaction
from api.v1.schemas.transaction import TransactionCreate, TransactionUpdate

from core.database import server_status
from core.logger import Logger
from core.utils import handle_server_down


def create_new_transaction(
        transaction: TransactionCreate,
        db: Session):
    db_transaction = Transaction(
        user_id=transaction.user_id,
        category_id=transaction.category_id,
        amount=transaction.amount,
        t_description=transaction.t_description,
        t_type=transaction.t_type,
        t_date=transaction.t_date
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
        transaction = db.query(Transaction).filter(
            Transaction.transactions_id == transaction_id).first()
        if transaction:
            return transaction
        raise HTTPException(
            status_code=404, detail="Transacción no encontrada")
    except Exception as e:
        Logger.error(f"Error getting transaction by id: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al obtener la transacción: {str(e)}")


def get_all_transactions(
        db: Session,
        user_id: str = None,
        offset: int = 0,
        limit: int = 20,
        category_id: int = None,
        t_type: str = None,
        t_date_from: str = None,
        t_date_to: str = None):
    try:
        if not server_status(db):
            return handle_server_down()
        query = db.query(Transaction)
        conditions = []
        if category_id:
            conditions.append(Transaction.category_id == category_id)
        if t_type:
            conditions.append(Transaction.t_type == t_type)
        if user_id:
            conditions.append(Transaction.user_id == user_id)
        if t_date_from:
            conditions.append(Transaction.t_date >= t_date_from)
        if t_date_to:
            conditions.append(Transaction.t_date <= t_date_to)
        if conditions:
            query = query.filter(and_(*conditions))
        transactions = query.offset(offset).limit(limit).all()
        count = db.query(Transaction).count()
        revenue = query.filter(Transaction.t_type == "revenue").with_entities(func.sum(Transaction.amount)).scalar()
        revenue = round(revenue, 2)
        expenses = query.filter(Transaction.t_type == "expenses").with_entities(func.sum(Transaction.amount)).scalar()
        expenses = round(expenses, 2)
        print("revenue: ", revenue)
        print("expenses: ", expenses)
        print("Count: ", count)
        if not transactions:
            raise HTTPException(
                status_code=404, detail="No se encontraron transacciones")
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
        db_transaction = db.query(Transaction).filter(
            Transaction.transactions_id == transaction_id).first()
        if db_transaction:
            db_transaction.user_id = transaction.user_id
            db_transaction.category_id = transaction.category_id
            db_transaction.amount = transaction.amount
            db_transaction.t_description = transaction.t_description
            db_transaction.t_type = transaction.t_type
            db_transaction.t_date = transaction.t_date
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        return {"status": "false", "message": "Transacción no encontrada"}
    except Exception as e:
        db.rollback()
        Logger.error(f"Error updating transaction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar la transacción: {str(e)}")


def delete_transaction(
        transaction_id: int,
        db: Session):
    try:
        if not server_status(db):
            return handle_server_down()
        db_transaction = db.query(Transaction).filter(
            Transaction.transactions_id == transaction_id).first()
        if db_transaction:
            db.delete(db_transaction)
            db.commit()
            return db_transaction
        return {"status": "false", "message": "Transacción no encontrada"}
    except Exception as e:
        db.rollback()
        Logger.error(f"Error deleting transaction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar la transacción: {str(e)}")
