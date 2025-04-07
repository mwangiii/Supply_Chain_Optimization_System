from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database
from supply_chain_backend_fastAPI.core.database import engine, Base
from supply_chain_backend_fastAPI.api.api_v1.api import api_router
from supply_chain_backend_fastAPI.core.config import settings

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
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
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
def root():
    return {
        "status": "success",
        "message": "Welcome to the Supply Chain Management System API!",
        "docs": f"{settings.API_V1_STR}/docs"
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run("supply_chain_backend_fastAPI.main:app", host="0.0.0.0", port=8000, reload=True)