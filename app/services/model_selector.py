import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error
from app.domain.models import ForecastRequest, ForecastResponse, ForecastModel

class ModelSelector:
    """Sélectionne automatiquement le meilleur modèle basé sur la validation."""
    
    @staticmethod
    def select_best_model(df: pd.DataFrame, horizon: int, freq: str) -> str:
        """
        Compare Prophet et SARIMAX sur les dernières données et retourne le meilleur.
        """
        if len(df) < 20:
            # Pas assez de données pour une validation robuste, utiliser Prophet par défaut
            return "prophet"
        
        # Split train/test (80/20)
        split_point = int(len(df) * 0.8)
        train = df.iloc[:split_point]
        test = df.iloc[split_point:]
        test_size = len(test)
        
        if test_size == 0:
            return "prophet"
        
        scores = {}
        
        # Test Prophet
        try:
            prophet_model = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality='auto')
            prophet_model.fit(train)
            future = prophet_model.make_future_dataframe(periods=test_size, freq=freq)
            forecast = prophet_model.predict(future)
            prophet_pred = forecast.tail(test_size)['yhat'].values
            scores['prophet'] = mean_absolute_error(test['y'].values, prophet_pred)
        except Exception:
            scores['prophet'] = float('inf')
        
        # Test SARIMAX (simple configuration)
        try:
            # Configuration basique SARIMAX
            model = SARIMAX(train['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12 if freq == 'M' else 1))
            fitted = model.fit(disp=False)
            sarimax_pred = fitted.forecast(steps=test_size)
            scores['arima'] = mean_absolute_error(test['y'].values, sarimax_pred)
        except Exception:
            scores['arima'] = float('inf')
        
        # Retourner le meilleur
        best_model = min(scores, key=scores.get)
        return best_model
