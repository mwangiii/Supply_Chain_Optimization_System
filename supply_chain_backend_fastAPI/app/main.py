from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database
from app.core.database import engine, Base
from app.api.api_v1.api import api_router
from app.core.config import settings

# Define startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created or verified")
    yield
    # Shutdown: Close connections, etc.
    # Any cleanup can be added here

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing supply chain operations and analytics",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configure CORS
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():  # Make this async
    return {
        "status": "success",
        "message": "Welcome to the Supply Chain Management System API!",
        "docs": f"{settings.API_V1_STR}/docs"
    }

def main():
    print("Starting data population process...")
    
    # Skip clearing existing data since it's failing
    print("Skipping data clearing due to backend error...")
    
    # Upload core data (products, inventory, sales, logistics)
    uploaded_data = upload_sample_data()
    
    if uploaded_data:
        # Continue with the rest of the operations only if data upload was successful
        # Create suppliers and their items
        suppliers = create_suppliers(count=10)
        items = create_supplier_items(suppliers, items_per_supplier=5)
        
        if items:
            restock_items(items, restock_count=15)
        else:
            print("No items created. Skipping restocking.")
        
        # Train forecasting model
        trained_forecast = train_forecast_model()
        if trained_forecast:
            refine_forecast_model()
        
        # Train AI models
        for _ in range(3):
            train_ai_model()
        
        # Create and update orders
        orders = create_orders(count=25)
        update_order_status(orders, update_count=15)
    
    print("Data population completed!")

# Run the application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
