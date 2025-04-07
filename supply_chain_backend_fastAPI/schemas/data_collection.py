from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from datetime import datetime

class DataCollectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the data collection")
    description: Optional[str] = Field(None, description="Optional description of the data collection")
    data: Dict[str, Any] = Field(..., description="The actual data in JSON format")

class DataCollectionCreate(DataCollectionBase):
    """Schema for creating a new data collection"""
    pass

class DataCollectionUpdate(BaseModel):
    """Schema for updating an existing data collection"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class DataCollectionInDB(DataCollectionBase):
    """Schema for data collection as stored in the database"""
    dataid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DataCollectionResponse(DataCollectionInDB):
    """Schema for data collection response"""
    pass

class StandardResponse(BaseModel):
    """Standard API response format"""
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
    
class DataCollectionListResponse(StandardResponse):
    """Response for a list of data collections"""
    data: List[DataCollectionResponse]