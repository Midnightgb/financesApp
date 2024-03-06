from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from api.v1.models.base_class import Base


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String(180), primary_key=True)
    user_id = Column(String(30), ForeignKey('users.user_id'))
    token_status = Column(Boolean, default=True)
    token_created_at = Column(TIMESTAMP, default=datetime.utcnow())
