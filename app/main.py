from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analysis
import uvicorn

app = FastAPI(
    title="TickerLab Services API",
    description="Orquestador de análisis cuantitativo para TickerLab",
    version="0.1.0"
)

# Configuración de CORS para permitir que la UI se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(analysis.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to TickerLab Services API",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
