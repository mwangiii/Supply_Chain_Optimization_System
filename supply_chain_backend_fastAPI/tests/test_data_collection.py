# tests/test_data_collection.py
from fastapi.testclient import TestClient


def test_upload_data(test_client: TestClient):
    response = test_client.post(
        "/api/v1/data/upload",
        json={
            "title": "Test Data",
            "description": "Test data description",
            "data": {"test_key": "test_value"},
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["title"] == "Test Data"


def test_get_all_data(test_client: TestClient):
    # First upload some data
    test_client.post(
        "/api/v1/data/upload",
        json={
            "title": "Test Data",
            "description": "Test data description",
            "data": {"test_key": "test_value"},
        },
    )
    
    # Then get all data
    response = test_client.get("/api/v1/data/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0