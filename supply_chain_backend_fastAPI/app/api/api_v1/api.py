from fastapi import APIRouter

from supply_chain_backend_fastAPI.api.api_v1.endpoints import (
    auth,
    data_collection,
    demand_forecasting,
    logistics,
    reports,
    suppliers,
    system_analytics,
    tracking,
)

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(data_collection.router, prefix="/data", tags=["Data Collection"])
api_router.include_router(demand_forecasting.router, prefix="/forecast", tags=["Demand Forecasting"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(system_analytics.router, prefix="/ai/models", tags=["AI Models"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])