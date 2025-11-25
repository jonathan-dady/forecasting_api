import pandas as pd
from typing import List, Dict, Any, Optional

class DataParser:
    @staticmethod
    def parse(data: List[Dict[str, Any]], date_col: Optional[str] = None, value_col: Optional[str] = None) -> pd.DataFrame:
        """
        Parses input data into a Prophet-compatible DataFrame (ds, y).
        """
        if not data:
            raise ValueError("Input data is empty")

        df = pd.DataFrame(data)

        # Auto-detect columns if not provided
        if not date_col:
            # Try common names
            for col in ["ds", "date", "datetime", "timestamp", "time"]:
                if col in df.columns:
                    date_col = col
                    break
        
        if not value_col:
            # Try common names
            for col in ["y", "value", "val", "amount", "quantity"]:
                if col in df.columns:
                    value_col = col
                    break
        
        # If still not found, try to infer by type (heuristic)
        if not date_col or not value_col:
             # Simple heuristic: first datetime-like column is date, first numeric is value
             # This is risky but fulfills "flexible input" requirement
             # For now, let's stick to explicit or common names to avoid bad magic
             pass

        if not date_col:
            raise ValueError("Could not detect date column. Please specify 'date_column'.")
        if not value_col:
            raise ValueError("Could not detect value column. Please specify 'value_column'.")

        # Rename and cast
        df = df.rename(columns={date_col: "ds", value_col: "y"})
        
        try:
            df["ds"] = pd.to_datetime(df["ds"])
            # Remove timezone info (Prophet doesn't support it)
            if df["ds"].dt.tz is not None:
                df["ds"] = df["ds"].dt.tz_localize(None)
        except Exception as e:
            raise ValueError(f"Could not parse date column '{date_col}': {str(e)}")

        try:
            df["y"] = pd.to_numeric(df["y"])
        except Exception as e:
            raise ValueError(f"Could not parse value column '{value_col}': {str(e)}")
            
        return df[["ds", "y"]].sort_values("ds")
