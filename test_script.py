import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from app.domain.models import ForecastRequest, Frequency
from app.services.forecasting import ForecastingService
from app.adapters.parsers import DataParser

def test_parser():
    print("Testing Parser...")
    
    # Case 1: Standard format
    data1 = [{"ds": "2023-01-01", "y": 100}, {"ds": "2023-02-01", "y": 110}]
    df1 = DataParser.parse(data1)
    assert "ds" in df1.columns and "y" in df1.columns
    print("  Case 1 OK")

    # Case 2: Flexible format (renaming)
    data2 = [{"date": "2023-01-01", "value": 100}, {"date": "2023-02-01", "value": 110}]
    df2 = DataParser.parse(data2)
    assert "ds" in df2.columns and "y" in df2.columns
    print("  Case 2 OK")
    
    # Case 3: Custom columns
    data3 = [{"my_date": "2023-01-01", "my_val": 100}]
    df3 = DataParser.parse(data3, date_col="my_date", value_col="my_val")
    assert "ds" in df3.columns and "y" in df3.columns
    print("  Case 3 OK")

def test_forecasting():
    print("\nTesting Forecasting Service...")
    
    data = [
        {"ds": "2023-01-01", "y": 100},
        {"ds": "2023-02-01", "y": 110},
        {"ds": "2023-03-01", "y": 120},
        {"ds": "2023-04-01", "y": 130},
        {"ds": "2023-05-01", "y": 140},
    ]
    
    req = ForecastRequest(
        data=data,
        horizon=3,
        frequency=Frequency.MONTHLY
    )
    
    resp = ForecastingService.generate_forecast(req)
    
    print(f"  Forecast generated: {len(resp.forecast)} points")
    print(f"  Dates: {resp.dates}")
    print(f"  Values: {resp.forecast}")
    
    assert len(resp.forecast) == 3
    assert len(resp.dates) == 3

if __name__ == "__main__":
    try:
        test_parser()
        test_forecasting()
        print("\nALL TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
