-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS RETAIL_DW_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Create database
CREATE DATABASE IF NOT EXISTS RETAIL_DW_DB;

-- Create schema
CREATE SCHEMA IF NOT EXISTS RETAIL_DW_DB.SALES_SCHEMA;

-- Select warehouse
USE WAREHOUSE RETAIL_DW_WH;

-- Select database
USE DATABASE RETAIL_DW_DB;

-- Select schema
USE SCHEMA SALES_SCHEMA;

-- Check current environment
SELECT
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();

-- Create CSV file format
CREATE FILE FORMAT IF NOT EXISTS RETAIL_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ',';

-- Create internal stage
CREATE STAGE IF NOT EXISTS RETAIL_STAGE
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Check uploaded files
LIST @RETAIL_STAGE;

-- Create source customers table
CREATE TABLE IF NOT EXISTS CUSTOMERS_SOURCE (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    membership VARCHAR(30)
);

-- Create source products table
CREATE TABLE IF NOT EXISTS PRODUCTS_SOURCE (
    product_id INTEGER,
    product_name VARCHAR(100),
    category VARCHAR(100),
    brand VARCHAR(100),
    price NUMBER(12,2)
);

-- Create source branches table
CREATE TABLE IF NOT EXISTS BRANCHES_SOURCE (
    branch_id INTEGER,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(50),
    manager_name VARCHAR(100)
);

-- Create source calendar table
CREATE TABLE IF NOT EXISTS CALENDAR_SOURCE (
    date_id INTEGER,
    date DATE,
    day INTEGER,
    day_name VARCHAR(20),
    week_no INTEGER,
    month VARCHAR(20),
    quarter VARCHAR(10),
    year INTEGER,
    is_weekend VARCHAR(10)
);

-- Create source sales table
CREATE TABLE IF NOT EXISTS SALES_SOURCE (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(12,2)
);

-- Load customers
COPY INTO CUSTOMERS_SOURCE
FROM @RETAIL_STAGE/customers.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load products
COPY INTO PRODUCTS_SOURCE
FROM @RETAIL_STAGE/products.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load branches
COPY INTO BRANCHES_SOURCE
FROM @RETAIL_STAGE/branches.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load calendar
COPY INTO CALENDAR_SOURCE
FROM @RETAIL_STAGE/calendar.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load sales
COPY INTO SALES_SOURCE
FROM @RETAIL_STAGE/sales.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Verify source customers
SELECT * FROM CUSTOMERS_SOURCE;

-- Verify source products
SELECT * FROM PRODUCTS_SOURCE;

-- Verify source branches
SELECT * FROM BRANCHES_SOURCE;

-- Verify source calendar
SELECT * FROM CALENDAR_SOURCE;

-- Verify source sales
SELECT * FROM SALES_SOURCE;

-- Create customer dimension
CREATE OR REPLACE TABLE DIM_CUSTOMER (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    membership VARCHAR(30)
);

-- Create product dimension
CREATE OR REPLACE TABLE DIM_PRODUCT (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    brand VARCHAR(100),
    price NUMBER(12,2)
);

-- Create branch dimension
CREATE OR REPLACE TABLE DIM_BRANCH (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(50),
    manager_name VARCHAR(100)
);

-- Create date dimension
CREATE OR REPLACE TABLE DIM_DATE (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    day INTEGER,
    day_name VARCHAR(20),
    week_no INTEGER,
    month VARCHAR(20),
    quarter VARCHAR(10),
    year INTEGER,
    is_weekend VARCHAR(10)
);

-- Create sales fact table
CREATE OR REPLACE TABLE FACT_SALES (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(12,2)
);

-- Load customer dimension
INSERT INTO DIM_CUSTOMER
SELECT
    customer_id,
    customer_name,
    city,
    state,
    membership
FROM CUSTOMERS_SOURCE;

-- Load product dimension
INSERT INTO DIM_PRODUCT
SELECT
    product_id,
    product_name,
    category,
    brand,
    price
FROM PRODUCTS_SOURCE;

-- Load branch dimension
INSERT INTO DIM_BRANCH
SELECT
    branch_id,
    branch_name,
    city,
    state,
    region,
    manager_name
FROM BRANCHES_SOURCE;

-- Load date dimension
INSERT INTO DIM_DATE
SELECT
    date_id,
    date,
    day,
    day_name,
    week_no,
    month,
    quarter,
    year,
    is_weekend
FROM CALENDAR_SOURCE;

-- Load sales fact table
INSERT INTO FACT_SALES
SELECT
    sale_id,
    customer_id,
    product_id,
    branch_id,
    date_id,
    quantity,
    total_amount
FROM SALES_SOURCE;

-- Verify customer dimension
SELECT * FROM DIM_CUSTOMER;

-- Verify product dimension
SELECT * FROM DIM_PRODUCT;

-- Verify branch dimension
SELECT * FROM DIM_BRANCH;

-- Verify date dimension
SELECT * FROM DIM_DATE;

-- Verify fact table
SELECT * FROM FACT_SALES;

-- Check number of customers
SELECT COUNT(*) AS customer_count
FROM DIM_CUSTOMER;

-- Check number of products
SELECT COUNT(*) AS product_count
FROM DIM_PRODUCT;

-- Check number of branches
SELECT COUNT(*) AS branch_count
FROM DIM_BRANCH;

-- Check number of dates
SELECT COUNT(*) AS date_count
FROM DIM_DATE;

-- Check number of sales
SELECT COUNT(*) AS sales_count
FROM FACT_SALES;

-- Customer-wise sales report
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.total_amount) AS total_sales
FROM DIM_CUSTOMER c
JOIN FACT_SALES f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_sales DESC;

-- Product-wise revenue report
SELECT
    p.product_id,
    p.product_name,
    SUM(f.total_amount) AS total_revenue
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_revenue DESC;

-- Branch-wise sales report
SELECT
    b.branch_id,
    b.branch_name,
    SUM(f.total_amount) AS total_sales
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY total_sales DESC;

-- Monthly revenue report
SELECT
    d.year,
    d.month,
    SUM(f.total_amount) AS monthly_revenue
FROM DIM_DATE d
JOIN FACT_SALES f
    ON d.date_id = f.date_id
GROUP BY
    d.year,
    d.month
ORDER BY
    d.year,
    d.month;

-- State-wise revenue report
SELECT
    b.state,
    SUM(f.total_amount) AS total_revenue
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY b.state
ORDER BY total_revenue DESC;

-- Category-wise revenue report
SELECT
    p.category,
    SUM(f.total_amount) AS total_revenue
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Top 10 customers
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.total_amount) AS total_sales
FROM DIM_CUSTOMER c
JOIN FACT_SALES f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_sales DESC
LIMIT 10;

-- Top 10 products
SELECT
    p.product_id,
    p.product_name,
    SUM(f.total_amount) AS total_revenue
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Top 10 branches
SELECT
    b.branch_id,
    b.branch_name,
    SUM(f.total_amount) AS total_revenue
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Sales trend by date
SELECT
    d.date,
    SUM(f.total_amount) AS daily_revenue
FROM DIM_DATE d
JOIN FACT_SALES f
    ON d.date_id = f.date_id
GROUP BY d.date
ORDER BY d.date;

-- Quarterly revenue
SELECT
    d.year,
    d.quarter,
    SUM(f.total_amount) AS quarterly_revenue
FROM DIM_DATE d
JOIN FACT_SALES f
    ON d.date_id = f.date_id
GROUP BY
    d.year,
    d.quarter
ORDER BY
    d.year,
    d.quarter;

-- Customer purchase analysis
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(f.sale_id) AS purchase_count,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_spending
FROM DIM_CUSTOMER c
JOIN FACT_SALES f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_spending DESC;

-- Product performance
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand
ORDER BY revenue DESC;

-- Branch performance
SELECT
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region
ORDER BY revenue DESC;

-- Customer ranking
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.total_amount) AS total_sales,
    RANK() OVER (
        ORDER BY SUM(f.total_amount) DESC
    ) AS customer_rank
FROM DIM_CUSTOMER c
JOIN FACT_SALES f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY customer_rank;

-- Product ranking
SELECT
    p.product_id,
    p.product_name,
    SUM(f.total_amount) AS revenue,
    RANK() OVER (
        ORDER BY SUM(f.total_amount) DESC
    ) AS product_rank
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY product_rank;

-- Branch ranking
SELECT
    b.branch_id,
    b.branch_name,
    SUM(f.total_amount) AS revenue,
    RANK() OVER (
        ORDER BY SUM(f.total_amount) DESC
    ) AS branch_rank
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY branch_rank;

-- Running revenue
SELECT
    d.date,
    f.sale_id,
    f.total_amount,
    SUM(f.total_amount) OVER (
        ORDER BY d.date, f.sale_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM FACT_SALES f
JOIN DIM_DATE d
    ON f.date_id = d.date_id
ORDER BY
    d.date,
    f.sale_id;

-- Average sale amount
SELECT
    f.sale_id,
    d.date,
    f.total_amount,
    AVG(f.total_amount) OVER () AS average_sale_amount
FROM FACT_SALES f
JOIN DIM_DATE d
    ON f.date_id = d.date_id
ORDER BY
    d.date,
    f.sale_id;

-- Create customer revenue view
CREATE OR REPLACE VIEW CUSTOMER_REVENUE AS
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.state,
    c.membership,
    SUM(f.total_amount) AS total_revenue,
    SUM(f.quantity) AS total_quantity,
    COUNT(f.sale_id) AS purchase_count
FROM DIM_CUSTOMER c
JOIN FACT_SALES f
    ON c.customer_id = f.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city,
    c.state,
    c.membership;

-- Query customer revenue view
SELECT *
FROM CUSTOMER_REVENUE
ORDER BY total_revenue DESC;

-- Create product revenue view
CREATE OR REPLACE VIEW PRODUCT_REVENUE AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS total_revenue
FROM DIM_PRODUCT p
JOIN FACT_SALES f
    ON p.product_id = f.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand;

-- Query product revenue view
SELECT *
FROM PRODUCT_REVENUE
ORDER BY total_revenue DESC;

-- Create branch revenue view
CREATE OR REPLACE VIEW BRANCH_REVENUE AS
SELECT
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region,
    SUM(f.total_amount) AS total_revenue
FROM DIM_BRANCH b
JOIN FACT_SALES f
    ON b.branch_id = f.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region;

-- Query branch revenue view
SELECT *
FROM BRANCH_REVENUE
ORDER BY total_revenue DESC;

-- Create a complete sales reporting view
CREATE OR REPLACE VIEW SALES_REPORT AS
SELECT
    f.sale_id,
    c.customer_name,
    p.product_name,
    p.category,
    p.brand,
    b.branch_name,
    b.city AS branch_city,
    b.state AS branch_state,
    b.region,
    d.date,
    d.month,
    d.quarter,
    d.year,
    f.quantity,
    f.total_amount
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
JOIN DIM_DATE d
    ON f.date_id = d.date_id;

-- Query complete sales report
SELECT *
FROM SALES_REPORT
ORDER BY date, sale_id;