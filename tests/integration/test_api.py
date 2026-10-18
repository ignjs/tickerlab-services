import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to TickerLab Services API" in response.json()["message"]

from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to TickerLab Services API" in response.json()["message"]

def test_analyze_endpoint_success():
    # Mock the AnalysisService.analyze_symbol method
    with patch("app.api.analysis.analysis_service.analyze_symbol") as mock_analyze:
        mock_result = {"symbol": "AAPL", "result": "bullish"}
        mock_analyze.return_value = mock_result

        response = client.post(
            "/analysis/analyze", 
            json={"symbol": "AAPL", "timeframe": "1d", "period": "max", "source": "yahoo"}
        )
        
        assert response.status_code == 200
        assert response.json() == mock_result
        mock_analyze.assert_called_once()

def test_analyze_endpoint_core_error():
    # Mock the service to raise a RuntimeError
    with patch("app.api.analysis.analysis_service.analyze_symbol") as mock_analyze:
        mock_analyze.side_effect = RuntimeError("Core failure")

        response = client.post(
            "/analysis/analyze", 
            json={"symbol": "AAPL"}
        )
        
        assert response.status_code == 500
        assert "Core failure" in response.json()["detail"]

@pytest.mark.parametrize("invalid_payload", [
    {}, 
    {"symbol": ""},
    {"symbol": "AAPL", "timeframe": 123}
])
def test_analyze_endpoint_validation_error(invalid_payload):
    response = client.post("/analysis/analyze", json=invalid_payload)
    assert response.status_code == 422
