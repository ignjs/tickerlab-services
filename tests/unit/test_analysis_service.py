from unittest.mock import MagicMock, patch
import pytest
from app.services.analysis_service import AnalysisService

@pytest.fixture
def analysis_service():
    return AnalysisService()

def test_analyze_symbol_success(analysis_service):
    # Mock the analyze_ticker function from tickerlab.analysis.engine
    with patch("app.services.analysis_service.analyze_ticker") as mock_analyze:
        mock_result = {"symbol": "AAPL", "status": "success", "metrics": {}}
        mock_analyze.return_value = mock_result

        import asyncio
        result = asyncio.run(analysis_service.analyze_symbol("AAPL"))

        assert result == mock_result
        mock_analyze.assert_called_once_with(
            symbol="AAPL",
            timeframe="1d",
            source="yahoo",
            cache_dir=analysis_service.cache_dir,
            period="max"
        )

def test_analyze_symbol_failure(analysis_service):
    with patch("app.services.analysis_service.analyze_ticker") as mock_analyze:
        mock_analyze.side_effect = Exception("Core engine error")

        import asyncio
        with pytest.raises(RuntimeError) as excinfo:
            asyncio.run(analysis_service.analyze_symbol("INVALID"))
        
        assert "Error en el núcleo de análisis: Core engine error" in str(excinfo.value)
