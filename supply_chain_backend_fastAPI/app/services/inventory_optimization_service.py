# app/services/inventory_optimization_service.py
import pickle
import os
import pandas as pd
from typing import Dict, Any, List
from fastapi import HTTPException

class InventoryOptimizationService:
    """Service for loading and using the inventory optimization ML model"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryOptimizationService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.load_model()
        return cls._instance
    
    def load_model(self):
        """Load the inventory optimization model"""
        model_path = os.environ.get("INVENTORY_MODEL_PATH", "app/models/ml/inventory_optimization.pkl")
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            print(f"Error loading inventory optimization model: {e}")
            self.model = None
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make inventory optimization predictions"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Inventory optimization model not loaded")
        
        try:
            # Convert input features to appropriate format
            input_df = pd.DataFrame([features])
            # Make prediction
            prediction = self.model.predict(input_df)
            # Add prediction results to response
            result = {
                "optimal_inventory_level": float(prediction[0]),
                "input_features": features,
                "model_info": {
                    "model_type": type(self.model).__name__
                }
            }
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Inventory optimization prediction error: {str(e)}")
            
    def batch_predict(self, features_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make batch inventory optimization predictions"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Inventory optimization model not loaded")
        
        try:
            input_df = pd.DataFrame(features_list)
            predictions = self.model.predict(input_df)
            
            results = []
            for i, features in enumerate(features_list):
                results.append({
                    "optimal_inventory_level": float(predictions[i]),
                    "input_features": features
                })
            return results
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Batch inventory optimization prediction error: {str(e)}")