import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from supply_chain_backend_fastAPI.core.database import get_db
from supply_chain_backend_fastAPI.models.data_collection import DataCollection
from supply_chain_backend_fastAPI.schemas.data_collection import DataCollectionCreate, DataCollectionResponse
from supply_chain_backend_fastAPI.api.api_v1.endpoints.auth import get_current_user
from supply_chain_backend_fastAPI.models.users import User
from supply_chain_backend_fastAPI.utils.helpers import success_response

router = APIRouter()

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_data(data_info: DataCollectionCreate, db: Session = Depends(get_db)):
    new_data = DataCollection(
        dataid=uuid.uuid4().hex,
        title=data_info.title,
        description=data_info.description,
        data=data_info.data
    )
    
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    
    return success_response(
        message="Data uploaded successfully",
        data={
            "dataid": new_data.dataid,
            "title": new_data.title,
            "description": new_data.description,
            "data": new_data.data
        }
    )

@router.get("/", response_model=dict)
async def get_all_data(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    data_list = []
    
    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })
    
    return success_response(data=data_list)

@router.get("/{dataid}", response_model=dict)
async def get_data(dataid: str, db: Session = Depends(get_db)):
    data = db.query(DataCollection).filter(DataCollection.dataid == dataid).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )
    
    return success_response(
        data={
            "dataid": data.dataid,
            "title": data.title,
            "description": data.description,
            "data": data.data
        }
    )

@router.get("/status", response_model=dict)
async def get_data_status(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    data_list = []
    
    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })
    
    return success_response(data=data_list)

@router.get("/inventory", response_model=dict)
async def get_data_inventory(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    data_list = []
    
    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })
    
    return success_response(data=data_list)

@router.get("/sales", response_model=dict)
async def get_data_sales(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    data_list = []
    
    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })
    
    return success_response(data=data_list)

@router.get("/logistics", response_model=dict)
async def get_data_logistics(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    data_list = []
    
    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })
    
    return success_response(data=data_list)

@router.delete("/clear", response_model=dict)
async def clear_data(db: Session = Depends(get_db)):
    data = db.query(DataCollection).all()
    for item in data:
        db.delete(item)
    
    db.commit()
    
    return success_response(message="All data cleared")