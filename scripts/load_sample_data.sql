-- Insert sample customers
INSERT INTO analytics.customer (customer_id, name, email, phone_number, address)
VALUES 
('CUST001', 'John Doe', 'john@example.com', '555-1234', '123 Elm St.'),
('CUST002', 'Jane Smith', 'jane@example.com', '555-5678', '456 Oak St.');

-- Insert sample products
INSERT INTO analytics.product (product_id, name, description, price, category)
VALUES 
('PROD001', 'Laptop', 'A high-performance laptop', 999.99, 'Electronics'),
('PROD002', 'Smartphone', 'Latest model smartphone', 599.99, 'Electronics');

-- Insert sample orders
INSERT INTO analytics.customer_order (order_id, customer_id, order_date, total_amount)
VALUES 
('ORD001', 'CUST001', CURRENT_TIMESTAMP, 999.99),
('ORD002', 'CUST002', CURRENT_TIMESTAMP, 599.99);

-- Insert sample order items
INSERT INTO analytics.order_item (order_item_id, order_id, product_id, quantity, price)
VALUES 
('ITEM001', 'ORD001', 'PROD001', 1, 999.99),
('ITEM002', 'ORD002', 'PROD002', 1, 599.99);

-- Insert sample reviews
INSERT INTO analytics.review (review_id, customer_id, product_id, rating, review_text, review_date)
VALUES 
('REV001', 'CUST001', 'PROD001', 5, 'Great laptop, highly recommend!', CURRENT_TIMESTAMP),
('REV002', 'CUST002', 'PROD002', 4, 'Good phone, but a bit overpriced.', CURRENT_TIMESTAMP);
