import pandas as pd
import os

def extract_raw_data(file_path: str) -> pd.DataFrame:
    """Loads the raw Kaggle D2C Skincare CSV file into a Pandas DataFrame."""
    print(f" [Extract] Loading raw data from: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing dataset! Please place your CSV file at: {file_path}")
    return pd.read_csv(file_path)
