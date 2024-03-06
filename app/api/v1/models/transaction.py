from sqlalchemy import Column, String, SmallInteger, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base_class import Base
from api.v1.models.category import Category


class Transaction(Base):
    __tablename__ = "transactions"

    transactions_id = Column(
        SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(30), ForeignKey('users.user_id'))
    category_id = Column(SmallInteger, ForeignKey('category.category_id'))
    amount = Column(Float(10, 2))
    t_description = Column(String(120))
    t_type = Column(Enum('revenue', 'expenses'))
    t_date = Column(Date)

    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
