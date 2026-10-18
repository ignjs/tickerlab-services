import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_core_engine():
    """
    Mocks the tickerlab-core analysis engine to avoid 'Illegal instruction' 
    and depend on external data.
    """
    with patch('app.services.analysis_service.analyze_ticker') as mock:
        yield mock

def test_e2e_analysis_pipeline_success(mock_core_engine):
    # Arrange: Define a complete successful response from the core
    mock_result = {
        "symbol": "AAPL",
        "note": "Detected US stock",
        "quote": {"price": 150.0, "change": 1.2},
        "bars_count": 1000,
        "events_count": 50,
        "summary": {
            "hit_rate": 0.6,
            "mean_forward_return": 0.02,
            "median_forward_return": 0.015,
            "profit_factor": 1.8,
            "sharpe": 1.2,
            "max_drawdown": -0.1,
            "auc": 0.75,
            "brier_score": 0.2,
            "precision_at_k": 0.8,
            "stability_score": 0.9
        },
        "score_now": 0.85,
        "message": None
    }
    mock_core_engine.return_value = mock_result

    # Act: Call the API endpoint
    response = client.post("/analysis/analyze", json={
        "symbol": "AAPL",
        "timeframe": "1d",
        "period": "max",
        "source": "yahoo"
    })

    # Assert: Verify the API returns the core's result correctly
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["score_now"] == 0.85
    assert data["summary"]["auc"] == 0.75
    assert "metrics" not in data # Ensure we are returning the core result structure

def test_e2e_analysis_pipeline_core_failure(mock_core_engine):
    # Arrange: Simulate a core engine crash
    mock_core_engine.side_effect = RuntimeError("Core Engine Failure")

    # Act
    response = client.post("/analysis/analyze", json={"symbol": "FAIL"})

    # Assert: Verify the API handles the core error and returns 500
    assert response.status_code == 500
    assert "Core Engine Failure" in response.json()["detail"]

def test_e2e_analysis_pipeline_invalid_symbol(mock_core_engine):
    # Arrange: Simulate core returning an error message for invalid symbol
    mock_result = {
        "symbol": "INVALID",
        "note": None,
        "quote": None,
        "bars_count": 0,
        "events_count": 0,
        "summary": None,
        "score_now": None,
        "message": "No se encontraron datos para el símbolo 'INVALID'"
    }
    mock_core_engine.return_value = mock_result

    # Act
    response = client.post("/analysis/analyze", json={"symbol": "INVALID"})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "No se encontraron datos para el símbolo 'INVALID'"
