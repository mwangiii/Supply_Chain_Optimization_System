# Supply Chain Backend

This is a FastAPI-based backend application for supply chain management.

## Features

- User authentication with JWT
- Data collection and management
- Demand forecasting
- Logistics optimization
- Reporting and analytics
- Supplier and inventory management
- Order tracking

## Project Structure

```
supply_chain_backend_fastAPI/
│
├── __init__.py
├── main.py                # Application entry point
├── core/                  # Core application components
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection and session management
│   └── security.py        # Authentication and security utilities
│
├── api/                   # API routes organized by resource
│   ├── __init__.py
│   ├── api_v1/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── data_collection.py
│   │   │   ├── demand_forecasting.py
│   │   │   ├── logistics.py
│   │   │   ├── reports.py
│   │   │   ├── suppliers.py
│   │   │   ├── system_analytics.py
│   │   │   └── tracking.py
│   │   └── api.py         # API router aggregation
│
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── users.py
│   └── data_collection.py
│
├── schemas/               # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── users.py
│   └── data_collection.py
│
├── crud/                  # Database operations
│   ├── __init__.py
│   ├── base.py            # Base CRUD operations
│   ├── users.py
│   └── data_collection.py
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── helpers.py
│
└── middleware/            # Custom middleware
    ├── __init__.py
    └── auth_middleware.py
```

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

FastAPI automatically generates interactive API documentation. After starting the application, you can access:

- Swagger UI: http://127.0.0.1:8000/api/v1/docs/
- ReDoc: http://localhost:8000/redoc

## Development

This project uses:
- FastAPI for the API framework
- SQLAlchemy for ORM
- Pydantic for data validation
- JWT for authentication