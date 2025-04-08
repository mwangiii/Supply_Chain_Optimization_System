# app/api/api_v1/endpoints/inventory_optimization.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.inventory_optimization_service import InventoryOptimizationService
from app.schemas.inventory_optimization import (
    InventoryOptimizationInput, 
    BatchInventoryOptimizationInput
)
from app.utils.helpers import success_response

router = APIRouter()

@router.post("/predict", response_model=Dict[str, Any])
async def predict_optimal_inventory(input_data: InventoryOptimizationInput):
    """
    Predict optimal inventory levels based on input features.
    """
    ml_service = InventoryOptimizationService()
    prediction = ml_service.predict(input_data.dict())
    return success_response(data=prediction)

@router.post("/batch-predict", response_model=Dict[str, Any])
async def batch_predict_optimal_inventory(input_data: BatchInventoryOptimizationInput):
    """
    Perform batch prediction for multiple inventory items.
    """
    ml_service = InventoryOptimizationService()
    feature_list = [item.dict() for item in input_data.items]
    predictions = ml_service.batch_predict(feature_list)
    return success_response(data={"results": predictions})

@router.get("/model/info")
async def get_model_info():
    """
    Get information about the current inventory optimization model.
    """
    ml_service = InventoryOptimizationService()
    if ml_service.model is None:
        raise HTTPException(status_code=500, detail="Inventory optimization model not loaded")
        
    model_info = {
        "model_type": type(ml_service.model).__name__,
        "features": ml_service.model.feature_names_ if hasattr(ml_service.model, "feature_names_") else "Unknown"
    }
    return success_response(data=model_info)

@router.get("/model/status")
async def get_model_status():
    """
    Get inventory optimization model status.
    """
    ml_service = InventoryOptimizationService()
    status = "loaded" if ml_service.model is not None else "not loaded"
    return success_response(message="Inventory optimization model status",
                           data={"status": status})