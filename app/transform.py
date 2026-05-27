import pandas as pd

def transform_data(df: pd.DataFrame):
    """Cleans raw data, handles missing attributes, and normalizes into star schema DataFrames."""
    print("⚙️ [Transform] Cleaning and normalizing data layout...")
    
    # 1. Standardize Data Types and Handle Missing Numeric Values
    df['age'] = df['age'].fillna(df['age'].median()).astype(int)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['signup_date'] = pd.to_datetime(df['signup_date']).dt.date
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce').fillna(0.0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
    
    # 2. Fill Missing Categorical Fields Safely
    categorical_cols = ['gender', 'location', 'product_name', 'category', 'skin_type_target', 'traffic_source']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip()

    # 3. Extract and Deduplicate dim_customers
    customers_df = df[['customer_id', 'gender', 'age', 'location', 'signup_date']].drop_duplicates(subset=['customer_id'])
    
    # 4. Extract and Deduplicate dim_products
    products_df = df[['product_id', 'product_name', 'category', 'price', 'skin_type_target']].drop_duplicates(subset=['product_id'])
    
    # 5. Extract and Deduplicate fact_orders
    orders_df = df[['order_id', 'customer_id', 'product_id', 'order_date', 'quantity', 'total_amount', 'traffic_source']].drop_duplicates(subset=['order_id'])
    
    print(f"✔️ Normalization complete: {len(customers_df)} unique customers, {len(products_df)} unique products, {len(orders_df)} unique orders.")
    return customers_df, products_df, orders_df
