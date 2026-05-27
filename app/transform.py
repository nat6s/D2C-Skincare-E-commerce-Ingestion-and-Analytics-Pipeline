import pandas as pd
import numpy as np

def transform_data(df: pd.DataFrame):
    """
    Cleans structural column values and dynamically extracts Star Schema fields
    by mapping against actual columns available in the Kaggle dataset.
    """
    print(" [ETL - Transform] Processing dataset fields and mapping target dimensions...")
    
    # Clean the input dataframe copies
    df_clean = df.copy()

    # --- 1. DYNAMICALLY BUILD CUSTOMER DIMENSIONS ---
    dim_customers = pd.DataFrame()
    dim_customers['customer_id'] = df_clean['customer_id'] if 'customer_id' in df_clean.columns else df_clean.get('id', df_clean.index.to_series().map(lambda x: f"CUST_{x}"))
    dim_customers['gender'] = df_clean['gender'] if 'gender' in df_clean.columns else 'Unknown'
    dim_customers['age'] = df_clean['age'].fillna(28).astype(int) if 'age' in df_clean.columns else 28
    dim_customers['location'] = df_clean['location'] if 'location' in df_clean.columns else df_clean.get('city', df_clean.get('country', 'Unknown'))
    
    if 'signup_date' in df_clean.columns:
        dim_customers['signup_date'] = pd.to_datetime(df_clean['signup_date'], dayfirst=True, errors='coerce')
    else:
        dim_customers['signup_date'] = pd.Timestamp('2026-01-01')
        
    dim_customers = dim_customers.drop_duplicates(subset=['customer_id'])

    # --- 2. DYNAMICALLY BUILD PRODUCT DIMENSIONS ---
    dim_products = pd.DataFrame()
    prod_id_col = next((c for c in df_clean.columns if 'product_id' in c or 'prod_id' in c or 'item_id' in c), None)
    if prod_id_col:
        dim_products['product_id'] = df_clean[prod_id_col]
    else:
        dim_products['product_id'] = df_clean.get('product', df_clean.index.to_series().map(lambda x: f"PROD_{x}"))

    dim_products['product_name'] = df_clean.get('product_name', df_clean.get('product', df_clean.get('item_name', 'Generic Product')))
    dim_products['category'] = df_clean.get('category', 'Skincare')
    dim_products['price'] = df_clean.get('price', df_clean.get('mrp', df_clean.get('cost', 10.00)))
    dim_products['skin_type_target'] = df_clean.get('skin_type_target', df_clean.get('skin_type', df_clean.get('concern', 'All Skin Types')))
    dim_products = dim_products.drop_duplicates(subset=['product_id'])

    # --- 3. DYNAMICALLY BUILD FACT ORDERS ---
    fact_orders = pd.DataFrame()
    fact_orders['order_id'] = df_clean['order_id'] if 'order_id' in df_clean.columns else df_clean.index.to_series().map(lambda x: f"ORD_{x}")
    fact_orders['customer_id'] = df_clean['customer_id'] if 'customer_id' in df_clean.columns else dim_customers['customer_id']
    fact_orders['product_id'] = df_clean[prod_id_col] if prod_id_col else dim_products['product_id']
    
    if 'order_date' in df_clean.columns:
        fact_orders['order_date'] = pd.to_datetime(df_clean['order_date'], dayfirst=True, errors='coerce')
    else:
        fact_orders['order_date'] = pd.Timestamp.now()
        
    fact_orders['quantity'] = df_clean.get('quantity', df_clean.get('qty', 1))
    fact_orders['total_amount'] = df_clean.get('total_amount', df_clean.get('final_amount', df_clean.get('gross_amount', 25.00)))
    fact_orders['traffic_source'] = df_clean.get('traffic_source', df_clean.get('sales_channel', 'Direct'))
    fact_orders = fact_orders.drop_duplicates(subset=['order_id'])

    print(f" [ETL - Transform] Complete! Customers: {len(dim_customers)}, Products: {len(dim_products)}, Orders: {len(fact_orders)}")
    return dim_customers, dim_products, fact_orders
