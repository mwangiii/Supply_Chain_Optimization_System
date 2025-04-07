from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import uvicorn

# Import routers
from app.routes.system_analytics import router as system_analytics_router
from app.routes.tracking import router as tracking_router
from app.routes.users import router as auth_router, index

# Import database
from app.database import engine, Base

# Define startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Close connections, etc.
    # This would be implemented as needed

# Create FastAPI application
app = FastAPI(
    title="Supply Chain Management System API",
    description="API for managing supply chain operations and analytics",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(system_analytics_router)
app.include_router(tracking_router)
app.include_router(auth_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return index()

# Custom OpenAPI schema to add more information
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Supply Chain Management System API",
        version="1.0.0",
        description="API for managing supply chain operations and analytics",
        routes=app.routes,
    )
    
    # Add any custom OpenAPI extensions here if needed
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)