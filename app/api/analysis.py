import json
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])
analysis_service = AnalysisService()

class AnalysisRequest(BaseModel):
    symbol: str
    timeframe: str = "1d"
    period: str = "max"
    source: str = "yahoo"

def nan_to_null(obj):
    if isinstance(obj, float):
        if obj != obj: # check for NaN
            return None
        return obj
    if isinstance(obj, dict):
        return {k: nan_to_null(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [nan_to_null(v) for v in obj]
    return obj

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
        
        # Clean NaN values to ensure JSON compliance
        cleaned_result = nan_to_null(result)
        return JSONResponse(content=cleaned_result)
        
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error inesperado: {str(e)}")
