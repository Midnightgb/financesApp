from sqlalchemy import Column, String, SmallInteger, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    transactions_id = Column(SmallInteger(
        3), primary_key=True, autoincrement=True)
    user_id = Column(String(30))
    category_id = Column(SmallInteger(3))
    amount = Column(Float(10, 2))
    t_description = Column(String(120))
    t_type = Column(Enum('revenue', 'expenses'))
    t_date = Column(Date)

    category = relationship("Category", backref="transactions")
    user = relationship("User", backref="transactions")
