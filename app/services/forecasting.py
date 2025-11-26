import pandas as pd
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
from app.domain.models import ForecastRequest, ForecastResponse, ForecastModel
from app.adapters.parsers import DataParser
from app.services.model_selector import ModelSelector

class ForecastingService:
    @staticmethod
    def generate_forecast(request: ForecastRequest) -> ForecastResponse:
        # 1. Parse Data
        df = DataParser.parse(request.data, request.date_column, request.value_column)
        
        # 2. Sélection du modèle
        model_to_use = request.model.value
        
        if model_to_use == "auto":
            # Mode AUTO : Sélection automatique
            model_to_use = ModelSelector.select_best_model(df, request.horizon, request.frequency.value)
        
        # 3. Prédiction selon le modèle choisi
        if model_to_use == "prophet":
            return ForecastingService._forecast_prophet(df, request)
        elif model_to_use == "arima":
            return ForecastingService._forecast_arima(df, request)
        else:
            # Fallback sur Prophet
            return ForecastingService._forecast_prophet(df, request)
    
    @staticmethod
    def _forecast_prophet(df: pd.DataFrame, request: ForecastRequest) -> ForecastResponse:
        """Prédiction avec Prophet."""
        model = Prophet()
        model.fit(df)
        
        future = model.make_future_dataframe(periods=request.horizon, freq=request.frequency.value)
        forecast = model.predict(future)
        result = forecast.tail(request.horizon)
        
        return ForecastResponse(
            dates=result["ds"].dt.strftime("%Y-%m-%d").tolist(),
            forecast=result["yhat"].round(2).tolist(),
            lower_bound=result["yhat_lower"].round(2).tolist(),
            upper_bound=result["yhat_upper"].round(2).tolist()
        )
    
    @staticmethod
    def _forecast_arima(df: pd.DataFrame, request: ForecastRequest) -> ForecastResponse:
        """Prédiction avec SARIMAX."""
        # Déterminer la périodicité saisonnière
        m = 12 if request.frequency.value == 'M' else 7 if request.frequency.value == 'W' else 1
        
        # Configuration SARIMAX
        # order (p,d,q): (autoregressive, différenciation, moving average)
        # seasonal_order (P,D,Q,m): composantes saisonnières
        model = SARIMAX(df['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, m))
        fitted = model.fit(disp=False)
        
        # Prédire
        forecast_result = fitted.get_forecast(steps=request.horizon)
        forecast_values = forecast_result.predicted_mean
        
        # Intervalles de confiance
        conf_int = forecast_result.conf_int()
        
        # Générer les dates futures
        last_date = df['ds'].max()
        freq_map = {'D': 'D', 'W': 'W', 'M': 'MS', 'Y': 'YS'}
        future_dates = pd.date_range(start=last_date, periods=request.horizon + 1, freq=freq_map.get(request.frequency.value, 'D'))[1:]
        
        return ForecastResponse(
            dates=future_dates.strftime("%Y-%m-%d").tolist(),
            forecast=forecast_values.round(2).tolist(),
            lower_bound=conf_int.iloc[:, 0].round(2).tolist(),
            upper_bound=conf_int.iloc[:, 1].round(2).tolist()
        )
