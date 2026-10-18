import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.analysis_service import AnalysisService
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_analysis_service():
    with patch('app.api.analysis.analysis_service') as mock:
        yield mock

@pytest.mark.asyncio
async def test_analyze_endpoint_success():
    # Arrange
    mock_data = {
        "symbol": "AAPL",
        "metrics": {"sharpe": 1.5},
        "summary": {"auc": 0.75},
        "score_now": 0.8,
        "message": None
    }
    
    with patch('app.api.analysis.analysis_service.analyze_symbol', return_value=mock_data):
        # Act
        response = client.post("/analysis/analyze", json={
            "symbol": "AAPL",
            "timeframe": "1d",
            "period": "max",
            "source": "yahoo"
        })
        
        # Assert
        assert response.status_code == 200
        assert response.json()["symbol"] == "AAPL"
        assert response.json()["metrics"]["sharpe"] == 1.5

@pytest.mark.asyncio
async def test_analyze_endpoint_nan_handling():
    # Test that NaN values are converted to null in JSON response
    mock_data = {
        "symbol": "AAPL",
        "metrics": {"sharpe": float('nan')}, # This is what caused the crash before
        "summary": {"auc": float('nan')},
        "score_now": None,
        "message": None
    }
    
    with patch('app.api.analysis.analysis_service.analyze_symbol', return_value=mock_data):
        response = client.post("/analysis/analyze", json={"symbol": "AAPL"})
        
        assert response.status_code == 200
        # Check that NaN was converted to None/null
        assert response.json()["metrics"]["sharpe"] is None
        assert response.json()["summary"]["auc"] is None

@pytest.mark.asyncio
async def test_analyze_endpoint_error():
    with patch('app.api.analysis.analysis_service.analyze_symbol', side_effect=RuntimeError("Core Error")):
        response = client.post("/analysis/analyze", json={"symbol": "FAIL"})
        
        assert response.status_code == 500
        assert "Core Error" in response.json()["detail"]
