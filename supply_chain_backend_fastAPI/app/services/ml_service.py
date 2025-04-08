# app/services/ml_service.py
import pickle
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

class DemandForecastingService:
    """Service for loading and using ML models"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DemandForecastingService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.load_model()
        return cls._instance
    
    def load_model(self):
        """Load the demand forecasting model"""
        model_path = os.environ.get("MODEL_PATH", "app/models/ml/demand_forecasting.pkl")
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using the loaded model"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        try:
            # Convert input features to appropriate format
            input_df = pd.DataFrame([features])
            # Make prediction
            prediction = self.model.predict(input_df)
            # Add prediction results to response
            result = {
                "prediction": float(prediction[0]),
                "input_features": features,
                "model_info": {
                    "model_type": type(self.model).__name__
                }
            }
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
            
    def batch_predict(self, features_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make batch predictions"""
        if self.model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        try:
            input_df = pd.DataFrame(features_list)
            predictions = self.model.predict(input_df)
            
            results = []
            for i, features in enumerate(features_list):
                results.append({
                    "prediction": float(predictions[i]),
                    "input_features": features
                })
            return results
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")