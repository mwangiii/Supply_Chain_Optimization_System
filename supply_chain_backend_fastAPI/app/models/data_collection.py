from sqlalchemy import Column, String, Text, JSON, DateTime, func
from app.core.database import Base
import uuid

class DataCollection(Base):
    __tablename__ = "data_collections"
    
    dataid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=False)  # Changed to JSON type for better data handling
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<DataCollection(dataid='{self.dataid}', title='{self.title}')>"
    
