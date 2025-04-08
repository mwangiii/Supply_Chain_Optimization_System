# app/api/api_v1/endpoints/route_optimization.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from app.services.route_optimization_service import RouteOptimizationService
from app.utils.helpers import success_response

# Define input/output models
class WaypointModel(BaseModel):
    """Model for a waypoint in a route"""
    location_id: str
    lat: float
    lng: float
    delivery_size: float = 0
    priority: int = 1

class TimeWindowModel(BaseModel):
    """Model for a delivery time window"""
    location_id: str
    start_time: str
    end_time: str

class RouteOptimizationInput(BaseModel):
    """Input schema for route optimization"""
    origin: Dict[str, float] = Field(..., description="Origin coordinates {lat, lng}")
    destination: Dict[str, float] = Field(..., description="Destination coordinates {lat, lng}")
    waypoints: List[WaypointModel] = Field(..., description="List of waypoints")
    vehicle_capacity: float = Field(..., description="Vehicle cargo capacity")
    delivery_time_windows: List[TimeWindowModel] = Field([], description="Time windows for deliveries")
    traffic_conditions: str = Field("normal", description="Traffic conditions: light, normal, heavy")
    vehicle_type: str = Field("truck", description="Type of vehicle")
    optimization_priority: str = Field("time", description="Optimization priority: time, fuel, distance")

class BatchRouteOptimizationInput(BaseModel):
    """Input schema for batch route optimization"""
    routes: List[RouteOptimizationInput]

class RouteOptimizationOutput(BaseModel):
    """Output schema for route optimization"""
    optimized_route: List[Dict[str, Any]]
    estimated_time: float
    distance: float
    fuel_consumption: float
    original_data: Dict[str, Any]

class BatchRouteOptimizationOutput(BaseModel):
    """Output schema for batch route optimization"""
    results: List[RouteOptimizationOutput]

# Create router
router = APIRouter()

@router.post("/optimize", response_model=Dict[str, Any])
async def optimize_routes(input_data: RouteOptimizationInput):
    """
    Optimize delivery routes based on various parameters.
    """
    route_service = RouteOptimizationService()
    optimized_route = route_service.optimize_route(input_data.dict())
    return success_response(data=optimized_route)

@router.post("/batch-optimize", response_model=Dict[str, Any])
async def batch_optimize_routes(input_data: BatchRouteOptimizationInput):
    """
    Perform batch optimization for multiple routes.
    """
    route_service = RouteOptimizationService()
    feature_list = [route.dict() for route in input_data.routes]
    optimized_routes = route_service.batch_optimize(feature_list)
    return success_response(data={"results": optimized_routes})

@router.get("/model/info")
async def get_model_info():
    """
    Get information about the current route optimization model.
    """
    route_service = RouteOptimizationService()
    if route_service.model is None:
        raise HTTPException(status_code=500, detail="Route optimization model not loaded")
    
    model_info = {
        "model_type": type(route_service.model).__name__,
        "features": route_service.model.feature_names_ if hasattr(route_service.model, "feature_names_") else "Unknown"
    }
    return success_response(data=model_info)

@router.get("/vehicle-types")
async def get_vehicle_types():
    """
    Get available vehicle types for route optimization.
    """
    vehicle_types = [
        {"id": "truck", "name": "Truck", "capacity": 1000, "fuel_efficiency": 0.25},
        {"id": "van", "name": "Van", "capacity": 500, "fuel_efficiency": 0.15},
        {"id": "car", "name": "Car", "capacity": 100, "fuel_efficiency": 0.08}
    ]
    
    return success_response(data=vehicle_types)

@router.get("/traffic-conditions")
async def get_traffic_conditions():
    """
    Get current traffic conditions from external sources.
    """
    # In a real implementation, this would call an external traffic API
    traffic_data = {
        "conditions": "normal",
        "congestion_areas": [
            {"lat": 40.7128, "lng": -74.0060, "level": "high"},
            {"lat": 40.7300, "lng": -73.9950, "level": "medium"}
        ],
        "last_updated": "2025-04-08T10:30:00Z"
    }
    
    return success_response(data=traffic_data)

@router.get("/model/status")
async def get_model_status():
    """
    Get route optimization model status and metrics.
    """
    route_service = RouteOptimizationService()
    status = "loaded" if route_service.model is not None else "not loaded"
    return success_response(message="Route optimization model status",
                           data={"status": status})