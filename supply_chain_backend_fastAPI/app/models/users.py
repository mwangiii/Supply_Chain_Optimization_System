from sqlalchemy import Column, String, DateTime, Boolean, func
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    userid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(userid='{self.userid}', email='{self.email}')>"
    
    @property
    def full_name(self):
        """Get full name of user"""
        return f"{self.firstname} {self.lastname}"