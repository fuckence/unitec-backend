from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy import Column, String, DateTime, text
from .base import Base

class User(Base):
    __tablename__ = "users"
    aitu_user_id  = Column(String, primary_key=True, index=True)
    first_name    = Column(String, nullable=True)
    last_name     = Column(String, nullable=True)
    username      = Column(String, nullable=True)
    go            = Column(String, nullable=True)
    region        = Column(String, nullable=True)
    raion         = Column(String, nullable=True)
    office_number = Column(String, nullable=True)
    phone         = Column(String, nullable=True, index=True)
    updated_at    = Column(DateTime(timezone=True),
                          server_default=text("CURRENT_TIMESTAMP"),
                          nullable=False)
