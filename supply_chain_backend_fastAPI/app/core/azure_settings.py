# app/core/azure_settings.py
import os
from app.core.config import Settings

class AzureSettings(Settings):
    # Azure-specific settings
    AZURE_STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_CONTAINER: str = os.getenv("AZURE_STORAGE_CONTAINER", "models")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/models/ml/demand_forecasting.pkl")
    INVENTORY_MODEL_PATH: str = os.getenv("INVENTORY_MODEL_PATH", "app/models/ml/inventory_optimization.pkl")  
    
    # Override database settings for Azure
    @property
    def DATABASE_URL(self) -> str:
        """Get the database URL, overriding with Azure SQL if available"""
        azure_sql = os.getenv("AZURE_SQL_CONNECTION_STRING")
        if azure_sql:
            return azure_sql
        return super().DATABASE_URL