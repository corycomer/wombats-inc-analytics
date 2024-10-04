-- Query total number of customers
SELECT COUNT(*) AS total_customers FROM analytics.customer;

-- Query total revenue from orders
SELECT SUM(total_amount) AS total_revenue FROM analytics.customer_order;

-- Query average rating for products
SELECT product_id, AVG(rating) AS avg_rating 
FROM analytics.review
GROUP BY product_id;

-- Query order details
SELECT o.order_id, c.name, p.name AS product_name, oi.quantity, oi.price
FROM analytics.customer_order o
JOIN analytics.customer c ON o.customer_id = c.customer_id
JOIN analytics.order_item oi ON o.order_id = oi.order_id
JOIN analytics.product p ON oi.product_id = p.product_id;
