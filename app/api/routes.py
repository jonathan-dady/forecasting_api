from fastapi import APIRouter, HTTPException
from app.domain.models import ForecastRequest, ForecastResponse
from app.services.forecasting import ForecastingService

router = APIRouter()

@router.post("/forecast", response_model=ForecastResponse, summary="Generate Forecast", description="Generates a forecast based on historical data.")
async def forecast(request: ForecastRequest):
    try:
        return ForecastingService.generate_forecast(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
