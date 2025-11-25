import pandas as pd
from prophet import Prophet
from app.domain.models import ForecastRequest, ForecastResponse
from app.adapters.parsers import DataParser

class ForecastingService:
    @staticmethod
    def generate_forecast(request: ForecastRequest) -> ForecastResponse:
        # 1. Parse Data
        df = DataParser.parse(request.data, request.date_column, request.value_column)
        
        # 2. Configure Model
        # We can add more configuration options here later (seasonality, etc.)
        model = Prophet()
        model.fit(df)
        
        # 3. Make Future Dataframe
        # freq mapping: D, W, M, Y are standard pandas frequencies which Prophet uses
        future = model.make_future_dataframe(periods=request.horizon, freq=request.frequency.value)
        
        # 4. Predict
        forecast = model.predict(future)
        
        # 5. Extract Results
        # We only want the future part for the response, or maybe the whole thing?
        # The original code did tail(horizon), which implies only future.
        # Let's stick to that for now.
        result = forecast.tail(request.horizon)
        
        return ForecastResponse(
            dates=result["ds"].dt.strftime("%Y-%m-%d").tolist(),
            forecast=result["yhat"].round(2).tolist(),
            lower_bound=result["yhat_lower"].round(2).tolist(),
            upper_bound=result["yhat_upper"].round(2).tolist()
        )
