from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Forecast API",
    description="API de forecasting avancée avec support d'inputs flexibles.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "version": "2.0.0"}
