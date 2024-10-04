-- Drop tables in the analytics schema
DROP TABLE IF EXISTS analytics.order_item;
DROP TABLE IF EXISTS analytics.customer_order;
DROP TABLE IF EXISTS analytics.review;
DROP TABLE IF EXISTS analytics.product;
DROP TABLE IF EXISTS analytics.customer;

-- Drop the analytics schema if needed
DROP SCHEMA IF EXISTS analytics;
