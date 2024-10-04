-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create CUSTOMER table
CREATE TABLE IF NOT EXISTS analytics.customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create PRODUCT table
CREATE TABLE IF NOT EXISTS analytics.product (
    product_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ORDER table
CREATE TABLE IF NOT EXISTS analytics.customer_order (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES analytics.customer(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2)
);

-- Create ORDER_ITEM table
CREATE TABLE IF NOT EXISTS analytics.order_item (
    order_item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES analytics.customer_order(order_id),
    product_id VARCHAR(50) REFERENCES analytics.product(product_id),
    quantity INT,
    price DECIMAL(10, 2)
);

-- Create REVIEW table
CREATE TABLE IF NOT EXISTS analytics.review (
    review_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES analytics.customer(customer_id),
    product_id VARCHAR(50) REFERENCES analytics.product(product_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
