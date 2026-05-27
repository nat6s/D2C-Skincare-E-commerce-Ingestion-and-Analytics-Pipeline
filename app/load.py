import os
from sqlalchemy import create_engine, text

def load_to_db(customers_df, products_df, orders_df):
    """
    Connects directly to our newly created MySQL Docker service container.
    """
    print(" [ETL - Load] Connecting to the MySQL Docker Container...")
    
    db_user = "root"
    db_pass = "root" 
    db_name = "skincare_analytics"
    host = "mysql" 
    port = "3306"
    
    connection_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{host}:{port}/{db_name}"
    engine = create_engine(connection_url)
    
    try:
        with engine.begin() as conn:
            print("  -> Temporarily disabling foreign key checks for clean load...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            
            # Since the container is fresh or re-running, let's clear old data if it exists
            print("  -> Dropping old destination data rows...")
            for table in ['fact_orders', 'dim_customers', 'dim_products']:
                try:
                    conn.execute(text(f"TRUNCATE TABLE {table};"))
                except Exception:
                    pass 
            
            print("  -> Uploading DataFrames into the live MySQL Docker tables...")
            customers_df.to_sql('dim_customers', con=conn, if_exists='append', index=False)
            products_df.to_sql('dim_products', con=conn, if_exists='append', index=False)
            orders_df.to_sql('fact_orders', con=conn, if_exists='append', index=False)
            
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            print(" 🎉 [ETL - Load] Success! All tables populated cleanly inside Docker!")
            
    except Exception as e:
        print(f" [CRITICAL ERROR] Database insertion failed: {str(e)}")
        raise e
