import os
import pandas as pd

def extract_raw_data(data_dir: str) -> pd.DataFrame:
    """
    Reads the core master Skincare D2C dataset from the local data folder.
    """
    print(f" [ETL - Extract] Checking for raw source files in: {data_dir}")
    
    # Kaggle default file name or handle a fallback renamed version
    possible_names = ["Skincare_D2C_Ecommerce_Analytics.csv", "skincare_data.csv", "data.csv"]
    file_path = None
    
    for name in possible_names:
        test_path = os.path.join(data_dir, name)
        if os.path.exists(test_path):
            file_path = test_path
            break
            
    if not file_path:
        # Check if the folder contains any CSV file at all to be flexible
        all_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if all_files:
            file_path = os.path.join(data_dir, all_files[0])
        else:
            raise FileNotFoundError(f"No source CSV dataset found inside {data_dir}!")

    print(f" [ETL - Extract] Loading dataset from target file path: {file_path}")
    df = pd.read_csv(file_path)
    
    # Standardize column strings immediately to prevent index issues
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    return df
