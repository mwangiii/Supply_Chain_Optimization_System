from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DataCollection
import uuid

# Define Pydantic models for request and response
class DataCollectionBase(BaseModel):
    title: str
    description: str
    data: Dict[str, Any]

class DataCollectionCreate(DataCollectionBase):
    pass

class DataCollectionResponse(DataCollectionBase):
    dataid: str
    
    class Config:
        orm_mode = True

class StandardResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[List[Dict[str, Any]]] = None

# Create APIRouter (FastAPI's equivalent to Flask's Blueprint)
router = APIRouter(prefix="/ai/models", tags=["AI Models"])

@router.get("/", response_model=StandardResponse, status_code=status.HTTP_200_OK)
async def get_all_models(db: Session = Depends(get_db)):
    """
    Get all AI models.
    
    Returns:
        List of all AI models in the database
    """
    models = db.query(DataCollection).all()
    models_list = [
        {
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        } for model in models
    ]
    
    return StandardResponse(
        status="success",
        data=models_list
    )

@router.post("/train", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def train_model(model_data: DataCollectionCreate, db: Session = Depends(get_db)):
    """
    Train a new AI model.
    
    Args:
        model_data: Data required to train the model
        
    Returns:
        The newly created model details
    """
    # FastAPI automatically validates the request body against the DataCollectionCreate model
    # No need for manual validation as in Flask
    
    new_model = DataCollection(
        dataid=uuid.uuid4().hex,
        title=model_data.title,
        description=model_data.description,
        data=model_data.data
    )
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    return StandardResponse(
        status="success",
        message="Model trained successfully",
        data={
            "dataid": new_model.dataid,
            "title": new_model.title,
            "description": new_model.description,
            "data": new_model.data
        }
    )

@router.get("/{dataid}/status", response_model=StandardResponse)
async def get_model_status(dataid: str, db: Session = Depends(get_db)):
    """
    Get the status of a specific AI model.
    
    Args:
        dataid: The unique identifier of the model
        
    Returns:
        The model details
        
    Raises:
        HTTPException: If the model is not found
    """
    model = db.query(DataCollection).filter(DataCollection.dataid == dataid).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return StandardResponse(
        status="success",
        data={
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    )

@router.get("/{dataid}/performance", response_model=StandardResponse)
async def get_model_performance(dataid: str, db: Session = Depends(get_db)):
    """
    Get the performance metrics of a specific AI model.
    
    Args:
        dataid: The unique identifier of the model
        
    Returns:
        The model performance details
        
    Raises:
        HTTPException: If the model is not found
    """
    model = db.query(DataCollection).filter(DataCollection.dataid == dataid).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return StandardResponse(
        status="success",
        data={
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    )

@router.post("/{dataid}/retrain", response_model=StandardResponse)
async def retrain_model(dataid: str, db: Session = Depends(get_db)):
    """
    Retrain an existing AI model.
    
    Args:
        dataid: The unique identifier of the model to retrain
        
    Returns:
        The retrained model details
        
    Raises:
        HTTPException: If the model is not found
    """
    model = db.query(DataCollection).filter(DataCollection.dataid == dataid).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    # In a real implementation, you would add retraining logic here
    
    return StandardResponse(
        status="success",
        message="Model retrained successfully",
        data={
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    )

@router.delete("/{dataid}", response_model=StandardResponse)
async def delete_model(dataid: str, db: Session = Depends(get_db)):
    """
    Delete an AI model.
    
    Args:
        dataid: The unique identifier of the model to delete
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If the model is not found
    """
    model = db.query(DataCollection).filter(DataCollection.dataid == dataid).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    db.delete(model)
    db.commit()
    
    return StandardResponse(
        status="success",
        message="Model deleted successfully"
    )