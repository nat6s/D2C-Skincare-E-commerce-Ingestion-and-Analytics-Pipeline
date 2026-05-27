-- Disable foreign key checks temporarily to drop tables smoothly on re-runs
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_products;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Create Customers Dimension Table
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(20),
    age INT,
    location VARCHAR(100),
    signup_date DATE,
    CONSTRAINT chk_age CHECK (age >= 0 AND age < 120)
);

-- 2. Create Products Dimension Table
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    skin_type_target VARCHAR(50)
);

-- 3. Create Fact Orders Table
CREATE TABLE fact_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    order_date DATETIME NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    total_amount DECIMAL(10,2) NOT NULL,
    traffic_source VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);

-- Create explicit index for time-series optimization
CREATE INDEX idx_orders_date ON fact_orders(order_date);
