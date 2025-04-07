from sqlalchemy import Column, String, Text
from app.core.database import Base

class DataCollection(Base):
    __tablename__ = "data"
    
    dataid = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    data = Column(Text, nullable=False)