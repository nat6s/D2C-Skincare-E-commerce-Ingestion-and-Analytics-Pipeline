import sys
import os

# Appends current directory to system path for clean imports execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract_raw_data
from transform import transform_data
from load import load_to_db

def run_pipeline():
    print("=== STARTING SKINCARE D2C ETL PIPELINE ===")
    
    # Dynamic path routing to look for the CSV within the data folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_path = os.path.join(base_dir, "data", "skincare_dataset.csv")
    
    try:
        raw_df = extract_raw_data(raw_data_path)
        customers, products, orders = transform_data(raw_df)
        load_to_db(customers, products, orders)
        print("=== PIPELINE EXECUTION SUCCESSFUL ===")
    except Exception as e:
        print(f" Pipeline Failed Error Trace: {str(e)}")

if __name__ == "__main__":
    run_pipeline()
