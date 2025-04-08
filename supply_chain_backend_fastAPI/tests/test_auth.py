# tests/test_auth.py
from fastapi.testclient import TestClient


def test_register_user(test_client: TestClient):
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "firstname": "Test",
            "lastname": "User",
            "email": "test@example.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["email"] == "test@example.com"


def test_login(test_client: TestClient):
    # First register a user
    test_client.post(
        "/api/v1/auth/register",
        json={
            "firstname": "Test",
            "lastname": "User",
            "email": "test@example.com",
            "password": "Password123",
        },
    )
    
    # Then try to login
    response = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["email"] == "test@example.com"

