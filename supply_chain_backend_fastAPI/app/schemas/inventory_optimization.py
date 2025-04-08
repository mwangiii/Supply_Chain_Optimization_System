# app/schemas/inventory_optimization.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class InventoryOptimizationInput(BaseModel):
    """Input schema for inventory optimization prediction"""
    product_id: str = Field(..., description="Product ID")
    location_id: str = Field(..., description="Warehouse/store location ID")
    current_stock: float = Field(..., description="Current inventory level")
    historical_demand: float = Field(..., description="Historical average demand")
    lead_time: float = Field(..., description="Lead time for replenishment in days")
    holding_cost: float = Field(..., description="Cost to hold one unit of inventory per day")
    stockout_cost: float = Field(..., description="Cost of stockout per unit")
    seasonality_factor: Optional[float] = Field(1.0, description="Seasonal demand factor")
    is_perishable: bool = Field(False, description="Whether the product is perishable")
    
class BatchInventoryOptimizationInput(BaseModel):
    """Input schema for batch inventory optimization prediction"""
    items: List[InventoryOptimizationInput]

class InventoryOptimizationOutput(BaseModel):
    """Output schema for inventory optimization prediction"""
    optimal_inventory_level: float
    input_features: Dict[str, Any]
    model_info: Dict[str, Any]

class BatchInventoryOptimizationOutput(BaseModel):
    """Output schema for batch inventory optimization prediction"""
    results: List[Dict[str, Any]]