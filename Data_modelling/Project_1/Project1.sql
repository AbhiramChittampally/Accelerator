-- Task 1: Create the virtual warehouse
CREATE WAREHOUSE IF NOT EXISTS SALES_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Task 2: Create the database
CREATE DATABASE IF NOT EXISTS CUSTOMER_SALES_DB;

-- Task 3: Create the schema
CREATE SCHEMA IF NOT EXISTS CUSTOMER_SALES_DB.SALES_SCHEMA;

-- Task 4: Select the warehouse, database and schema
USE WAREHOUSE SALES_WH;
USE DATABASE CUSTOMER_SALES_DB;
USE SCHEMA CUSTOMER_SALES_DB.SALES_SCHEMA;

-- Verify the current Snowflake environment
SELECT
    CURRENT_WAREHOUSE() AS CURRENT_WAREHOUSE,
    CURRENT_DATABASE() AS CURRENT_DATABASE,
    CURRENT_SCHEMA() AS CURRENT_SCHEMA;

-- Task 5: Create the CSV file format
CREATE FILE FORMAT IF NOT EXISTS SALES_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ',';

-- Verify the file format
SHOW FILE FORMATS;

-- Task 6: Create the internal stage
CREATE STAGE IF NOT EXISTS SALES_STAGE
FILE_FORMAT = SALES_CSV_FORMAT;

-- Verify the stage
SHOW STAGES;

-- Task 7: Upload customers.csv, fooditems.csv and orders.csv to SALES_STAGE using the Snowflake UI

-- Verify the uploaded files
LIST @SALES_STAGE;

-- Task 8: Create the CUSTOMERS table
CREATE TABLE IF NOT EXISTS CUSTOMERS (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(100)
);

-- Create the FOODITEMS table
CREATE TABLE IF NOT EXISTS FOODITEMS (
    food_id INTEGER,
    name VARCHAR(100),
    price NUMBER(10,2),
    category VARCHAR(50),
    availability VARCHAR(20)
);

-- Create the ORDERS table
CREATE TABLE IF NOT EXISTS ORDERS (
    order_id INTEGER,
    customer_id INTEGER,
    food_id INTEGER,
    quantity INTEGER,
    order_date TIMESTAMP_NTZ,
    status VARCHAR(30),
    total_amount NUMBER(10,2)
);

-- Verify the tables
SHOW TABLES;

-- Task 9: Load customers.csv into CUSTOMERS
COPY INTO CUSTOMERS
FROM @SALES_STAGE/customers.csv
FILE_FORMAT = SALES_CSV_FORMAT;

-- Load fooditems.csv into FOODITEMS
COPY INTO FOODITEMS
FROM @SALES_STAGE/fooditems.csv
FILE_FORMAT = SALES_CSV_FORMAT;

-- Load orders.csv into ORDERS
COPY INTO ORDERS
FROM @SALES_STAGE/orders.csv
FILE_FORMAT = SALES_CSV_FORMAT;

-- Task 10: Verify the loaded customer data
SELECT *
FROM CUSTOMERS;

-- Verify the loaded food item data
SELECT *
FROM FOODITEMS;

-- Verify the loaded order data
SELECT *
FROM ORDERS;

-- Task 11: Display all customer details
SELECT *
FROM CUSTOMERS;

-- Task 12: Display all food item details
SELECT *
FROM FOODITEMS;

-- Task 13: Display all order details
SELECT *
FROM ORDERS;

-- Task 14: Generate the customer-wise sales report
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(o.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN ORDERS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name;

-- Task 15: Find the highest spending customer
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(o.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN ORDERS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_spent DESC
LIMIT 1;

-- Task 16: Calculate total business revenue
SELECT
    SUM(total_amount) AS total_revenue
FROM ORDERS;

-- Task 17: Generate the category-wise revenue report
SELECT
    f.category,
    SUM(o.total_amount) AS revenue
FROM ORDERS o
INNER JOIN FOODITEMS f
    ON o.food_id = f.food_id
GROUP BY
    f.category
ORDER BY revenue DESC;

-- Task 18: Generate the order status-wise revenue report
SELECT
    status AS order_status,
    SUM(total_amount) AS revenue
FROM ORDERS
GROUP BY status
ORDER BY revenue DESC;

-- Task 19: Display the top three customers
SELECT
    ROW_NUMBER() OVER (ORDER BY total_spent DESC) AS rank,
    customer_name,
    total_spent
FROM (
    SELECT
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        SUM(o.total_amount) AS total_spent
    FROM CUSTOMERS c
    INNER JOIN ORDERS o
        ON c.customer_id = o.customer_id
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name
)
ORDER BY rank
LIMIT 3;

-- Task 20: Generate the customer purchase frequency report
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(o.order_id) AS orders_placed
FROM CUSTOMERS c
INNER JOIN ORDERS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY c.customer_id;

-- Task 21: Display delivered orders only
SELECT
    order_id,
    customer_id,
    food_id,
    status,
    total_amount
FROM ORDERS
WHERE status = 'Delivered'
ORDER BY order_id;

-- Task 22: Display orders placed after 12 July 2026
SELECT
    o.order_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM ORDERS o
INNER JOIN CUSTOMERS c
    ON o.customer_id = c.customer_id
WHERE o.order_date > '2026-07-12 23:59:59'
ORDER BY o.order_id;

-- Task 23: Create the customer sales report view
CREATE OR REPLACE VIEW CUSTOMER_SALES_REPORT AS
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(o.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN ORDERS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name;

-- Verify the created view
SHOW VIEWS;

-- Task 24: Retrieve all records from the view
SELECT *
FROM CUSTOMER_SALES_REPORT;

-- Task 25: Sort the view by total spending
SELECT *
FROM CUSTOMER_SALES_REPORT
ORDER BY total_spent DESC;