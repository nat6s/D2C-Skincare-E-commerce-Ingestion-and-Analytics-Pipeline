import os
import sys

# Ensure local directory lookup contexts match across Airflow containers
dag_dir = os.path.dirname(os.path.abspath(__file__))
if dag_dir not in sys.path:
    sys.path.insert(0, dag_dir)

from extract import extract_raw_data
from transform import transform_data
from load import load_to_db

def run_etl_pipeline():
    print("\n=======================================================")
    print("  PRODUCTION DATA PIPELINE RUNTIME LOG: RUNNING ETL")
    print("=======================================================\n")
    
    # Point directly to your local nested data folder path context
    data_directory = os.path.join(dag_dir, "data")
    
    # Task 1: Extraction Execution Layer
    raw_flat_dataframe = extract_raw_data(data_directory)
    
    # Task 2: Structural Split Data Transformation Layer
    clean_cust, clean_prod, clean_ord = transform_data(raw_flat_dataframe)
    
    # Task 3: Load Engine Layer
    load_to_db(clean_cust, clean_prod, clean_ord)
    
    print("\n=======================================================")
    print("  PIPELINE PROCESSING COMPLETE: READY FOR ANALYTICS")
    print("=======================================================\n")

if __name__ == "__main__":
    run_etl_pipeline()
