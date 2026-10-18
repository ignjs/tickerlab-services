from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])
analysis_service = AnalysisService()

class AnalysisRequest(BaseModel):
    symbol: str
    timeframe: str = "1d"
    period: str = "max"
    source: str = "yahoo"

@router.post("/analyze")
async def analyze_symbol(request: AnalysisRequest):
    """
    Ejecuta el pipeline de análisis cuantitativo E2E para un activo.
    """
    try:
        result = await analysis_service.analyze_symbol(
            symbol=request.symbol,
            timeframe=request.timeframe,
            period=request.period,
            source=request.source
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error inesperado: {str(e)}")
