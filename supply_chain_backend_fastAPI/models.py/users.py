from sqlalchemy import Column, String, DateTime, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    userid = Column(String, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())