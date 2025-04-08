# app/services/route_optimization_service.py
import pickle
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

class RouteOptimizationService:
    """Service for route optimization using machine learning models"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RouteOptimizationService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.load_model()
        return cls._instance
    
    def load_model(self):
        """Load the route optimization model"""
        model_path = os.environ.get("ROUTE_MODEL_PATH", "app/models/ml/route_optimization.pkl")
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            print(f"Route optimization model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading route optimization model: {e}")
            self.model = None
    
    def optimize_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize delivery routes based on input data"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Route optimization model not loaded")
        
        try:
            # Process input data for model consumption
            route_data = self._prepare_route_data(data)
            
            # Make optimization predictions
            optimized_route = self.model.predict(route_data)
            
            # Process output for API response
            result = self._process_optimization_result(optimized_route, data)
            
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Route optimization error: {str(e)}")
    
    def batch_optimize(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch optimize multiple routes"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Route optimization model not loaded")
        
        try:
            results = []
            for data in data_list:
                route_data = self._prepare_route_data(data)
                optimized_route = self.model.predict(route_data)
                result = self._process_optimization_result(optimized_route, data)
                results.append(result)
            
            return results
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Batch route optimization error: {str(e)}")
    
    def _prepare_route_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare route data for model input"""
        # Convert the input data to a pandas DataFrame
        required_fields = ['origin', 'destination', 'waypoints', 'vehicle_capacity',
                          'delivery_time_windows', 'traffic_conditions']
        
        # Validate input data has required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Create a DataFrame from the input data
        route_df = pd.DataFrame([data])
        
        # Additional processing can be performed here based on model requirements
        
        return route_df
    
    def _process_optimization_result(self, optimized_route, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process optimization result into API response format"""
        # Convert model output to response format
        # This will depend on what your model returns
        
        # Example response structure
        response = {
            "optimized_route": optimized_route.tolist() if isinstance(optimized_route, np.ndarray) else optimized_route,
            "estimated_time": self._calculate_estimated_time(optimized_route, original_data),
            "distance": self._calculate_distance(optimized_route),
            "fuel_consumption": self._calculate_fuel_consumption(optimized_route, original_data),
            "original_data": original_data
        }
        
        return response
    
    def _calculate_estimated_time(self, route, data: Dict[str, Any]) -> float:
        """Calculate estimated time for the optimized route"""
        # This is a placeholder for actual time calculation logic
        # In a real implementation, this would use distance and traffic data
        return 120.5  # Example: 120.5 minutes
    
    def _calculate_distance(self, route) -> float:
        """Calculate total distance for the optimized route"""
        # This is a placeholder for actual distance calculation logic
        return 45.7  # Example: 45.7 kilometers
    
    def _calculate_fuel_consumption(self, route, data: Dict[str, Any]) -> float:
        """Calculate estimated fuel consumption for the route"""
        # This is a placeholder for actual fuel consumption calculation
        # In a real implementation, this would consider vehicle type, load, route, etc.
        return 14.3  # Example: 14.3 liters