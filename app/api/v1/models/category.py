from sqlalchemy import Column, String, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from api.v1.models.base_class import Base

class Category(Base):
    __tablename__ = "category"

    category_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    category_name = Column(String(50))
    category_description = Column(String(120))
    category_status = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="category")