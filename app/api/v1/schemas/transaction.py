from pydantic import BaseModel
from enum import Enum
from datetime import date


class TransactionType(str, Enum):
    revenue = "revenue"
    expenses = "expenses"


class TransactionBase(BaseModel):
    amount: float
    t_description: str
    t_type: TransactionType
    t_date: date


class TransactionCreate(TransactionBase):
    user_id: str
    category_id: int


class TransactionRead(TransactionBase):
    transactions_id: int
    user_id: str
    category_id: int


class TransactionUpdate(TransactionRead):
    pass


class TransactionDelete(BaseModel):
    transactions_id: int
