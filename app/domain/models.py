from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class Frequency(str, Enum):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    YEARLY = "Y"

class ForecastModel(str, Enum):
    PROPHET = "prophet"
    ARIMA = "arima"

class ForecastRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of data points. Can be flexible.")
    horizon: int = Field(..., gt=0, description="Number of periods to forecast")
    frequency: Frequency = Field(default=Frequency.MONTHLY, description="Frequency of the data")
    model: ForecastModel = Field(default=ForecastModel.PROPHET, description="Forecasting model to use")
    
    # Optional mapping for flexible inputs
    date_column: Optional[str] = Field(None, description="Name of the date column if not 'date' or 'ds'")
    value_column: Optional[str] = Field(None, description="Name of the value column if not 'value' or 'y'")

class ForecastResponse(BaseModel):
    dates: List[str]
    forecast: List[float]
    lower_bound: Optional[List[float]] = None
    upper_bound: Optional[List[float]] = None
