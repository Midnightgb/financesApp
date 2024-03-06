from pydantic import BaseModel
from typing import Optional
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
