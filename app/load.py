from sqlalchemy import create_engine
import pandas as pd

def load_to_db(customers, products, orders):
    """Establishes a MySQL connection and loads data directly into pre-existing schema tables."""
    print("🚀 [Load] Pushing data into MySQL database...")
    
    # NOTE: Replace 'root' and 'your_password' with your local MySQL configurations
    DATABASE_URL = 'mysql+pymysql://root:your_password@localhost:3306/skincare_db'
    
    engine = create_engine(DATABASE_URL)
    
    # Load into tables using append mode to preserve pre-declared constraints and indexes
    customers.to_sql('dim_customers', engine, if_exists='append', index=False)
    print("  -> Loaded dim_customers successfully.")
    
    products.to_sql('dim_products', engine, if_exists='append', index=False)
    print("  -> Loaded dim_products successfully.")
    
    orders.to_sql('fact_orders', engine, if_exists='append', index=False)
    print("  -> Loaded fact_orders successfully.")
    
    print(" Database fully populated!")
