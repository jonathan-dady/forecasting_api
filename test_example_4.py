import sys
import os
sys.path.append(os.getcwd())

from app.domain.models import ForecastRequest
from app.services.forecasting import ForecastingService

# Test de l'exemple 4
data = {
    "data": [
        {"timestamp": "2023-01-01T00:00:00Z", "qty": 10},
        {"timestamp": "2023-02-01T00:00:00Z", "qty": 15},
        {"timestamp": "2023-03-01T00:00:00Z", "qty": 20},
        {"timestamp": "2023-04-01T00:00:00Z", "qty": 25}
    ],
    "horizon": 6,
    "frequency": "M",
    "value_column": "qty"
}

try:
    req = ForecastRequest(**data)
    print("Request créée avec succès:")
    print(f"  - date_column: {req.date_column}")
    print(f"  - value_column: {req.value_column}")
    
    result = ForecastingService.generate_forecast(req)
    print("\nRésultat:")
    print(f"  Dates: {result.dates}")
    print(f"  Forecast: {result.forecast}")
    print(f"  Lower: {result.lower_bound}")
    print(f"  Upper: {result.upper_bound}")
except Exception as e:
    print(f"ERREUR: {e}")
    import traceback
    traceback.print_exc()
