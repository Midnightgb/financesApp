from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class token(Base):
    __tablename__ = "tokens"

    token = Column(String(180), primary_key=True)
    user_id = Column(String(30))
    token_status = Column(Boolean, default=True)
    token_created_at = Column(TIMESTAMP, default=datetime.utcnow())
