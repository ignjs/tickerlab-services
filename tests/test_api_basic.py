import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

@pytest.mark.asyncio
async def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to TickerLab Services API" in response.json()["message"]
