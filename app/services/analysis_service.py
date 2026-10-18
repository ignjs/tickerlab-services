from pathlib import Path
from typing import Any, Optional
from tickerlab.analysis.engine import analyze_ticker

class AnalysisService:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)

    async def analyze_symbol(
        self, 
        symbol: str, 
        timeframe: str = "1d", 
        period: str = "max", 
        source: str = "yahoo"
    ) -> dict[str, Any]:
        """
        Ejecuta el pipeline de análisis completo del núcleo para un símbolo dado.
        """
        try:
            # El núcleo es síncrono, lo ejecutamos directamente 
            # (en una implementación productiva se podría usar run_in_threadpool)
            result = analyze_ticker(
                symbol=symbol,
                timeframe=timeframe,
                source=source,
                cache_dir=self.cache_dir,
                period=period
            )
            return result
        except Exception as e:
            raise RuntimeError(f"Error en el núcleo de análisis: {str(e)}")
