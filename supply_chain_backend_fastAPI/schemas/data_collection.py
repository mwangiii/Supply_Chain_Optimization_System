from pydantic import BaseModel, Field
from typing import Optional, List

class DataCollectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    data: str

class DataCollectionCreate(DataCollectionBase):
    pass

class DataCollectionResponse(DataCollectionBase):
    dataid: str
    
    class Config:
        from_attributes = True

class DataCollectionList(BaseModel):
    status: str
    data: List[DataCollectionResponse]

class ErrorResponse(BaseModel):
    message: str
    status_code: int

class ErrorList(BaseModel):
    status: str
    message: str
    errors: List[ErrorResponse]