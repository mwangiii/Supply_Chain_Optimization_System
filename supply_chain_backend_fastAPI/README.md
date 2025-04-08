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
- CI/CD with GitHub Actions

## Project Structure

```
supply_chain_backend_fastAPI/
│
├── .github/                 # GitHub Actions workflows
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline configuration
│
├── __init__.py
├── main.py                  # Application entry point
├── core/                    # Core application components
│   ├── __init__.py
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session management
│   └── security.py          # Authentication and security utilities
│
├── api/                     # API routes organized by resource
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
│   │   └── api.py           # API router aggregation
│
├── models/                  # SQLAlchemy models
│   ├── __init__.py
│   ├── users.py
│   └── data_collection.py
│
├── schemas/                 # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── users.py
│   └── data_collection.py
│
├── crud/                    # Database operations
│   ├── __init__.py
│   ├── base.py              # Base CRUD operations
│   ├── users.py
│   └── data_collection.py
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py
│
├── middleware/              # Custom middleware
│   ├── __init__.py
│   └── auth_middleware.py
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_data_collection.py # Data collection endpoint tests
│
├── Dockerfile               # Docker configuration for containerization
├── docker-compose.yml       # Docker Compose for local development
└── requirements.txt         # Project dependencies
```

## Installation

### Local Development

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
```bash
pip install -r requirements.txt
```

### Using Docker

```bash
# Build and start the container
docker-compose up -d

# Stop the container
docker-compose down
```

## Running the Application

### Local Development

```bash
uvicorn app.main:app --reload
```

### Using Docker

```bash
docker-compose up
```

## API Documentation

FastAPI automatically generates interactive API documentation. After starting the application, you can access:

- Swagger UI: http://127.0.0.1:8000/api/v1/docs/
- ReDoc: http://localhost:8000/redoc

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

1. **Testing**: Runs on every push to main/master/develop branches and on pull requests
   - Lint checking with flake8
   - Format checking with black and isort
   - Type checking with mypy
   - Unit tests with pytest

2. **Build and Push**: Runs after successful tests on pushes to main/master
   - Builds a Docker image
   - Pushes to Docker Hub

3. **Deployment**: Runs after successful build on pushes to main/master
   - Currently a placeholder for your deployment strategy

### Required Secrets

For the GitHub Actions workflow to function properly, add these secrets to your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

## Development

This project uses:
- FastAPI for the API framework
- SQLAlchemy for ORM
- Pydantic for data validation
- JWT for authentication
- GitHub Actions for CI/CD
- Docker for containerization

## Testing

Run tests with:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=app tests/
```