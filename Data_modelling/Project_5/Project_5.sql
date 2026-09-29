-- Create the warehouse
CREATE WAREHOUSE IF NOT EXISTS RETAIL_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Create the database
CREATE DATABASE IF NOT EXISTS RETAIL_DB;

-- Create the schema
CREATE SCHEMA IF NOT EXISTS RETAIL_DB.SALES_SCHEMA;

-- Select the warehouse
USE WAREHOUSE RETAIL_WH;

-- Select the database
USE DATABASE RETAIL_DB;

-- Select the schema
USE SCHEMA SALES_SCHEMA;

-- Check the current environment
SELECT
    CURRENT_WAREHOUSE() AS WAREHOUSE,
    CURRENT_DATABASE() AS DATABASE,
    CURRENT_SCHEMA() AS SCHEMA;


-- Create CSV file format
CREATE FILE FORMAT IF NOT EXISTS RETAIL_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ',';


-- Create internal stage
CREATE STAGE IF NOT EXISTS RETAIL_STAGE
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Check the files uploaded to the stage
LIST @RETAIL_STAGE;


-- Create raw customers table
CREATE TABLE IF NOT EXISTS CUSTOMERS_RAW (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    membership VARCHAR(20)
);


-- Create raw products table
CREATE TABLE IF NOT EXISTS PRODUCTS_RAW (
    product_id INTEGER,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    price NUMBER(12,2)
);


-- Create raw branches table
CREATE TABLE IF NOT EXISTS BRANCHES_RAW (
    branch_id INTEGER,
    branch_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(50),
    manager_name VARCHAR(100)
);


-- Create raw calendar table
CREATE TABLE IF NOT EXISTS CALENDAR_RAW (
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


-- Create raw sales table
CREATE TABLE IF NOT EXISTS SALES_RAW (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(14,2)
);


-- Load customers
COPY INTO CUSTOMERS_RAW
FROM @RETAIL_STAGE/customers.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Load products
COPY INTO PRODUCTS_RAW
FROM @RETAIL_STAGE/products.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Load branches
COPY INTO BRANCHES_RAW
FROM @RETAIL_STAGE/branches.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Load calendar
COPY INTO CALENDAR_RAW
FROM @RETAIL_STAGE/calendar.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Load sales
COPY INTO SALES_RAW
FROM @RETAIL_STAGE/sales.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;


-- Verify customers
SELECT * FROM CUSTOMERS_RAW;


-- Verify products
SELECT * FROM PRODUCTS_RAW;


-- Verify branches
SELECT * FROM BRANCHES_RAW;


-- Verify calendar
SELECT * FROM CALENDAR_RAW;


-- Verify sales
SELECT * FROM SALES_RAW;


-- Create customer dimension
CREATE OR REPLACE TABLE DIM_CUSTOMER (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    membership VARCHAR(20)
);


-- Load customer dimension
INSERT INTO DIM_CUSTOMER
SELECT
    customer_id,
    customer_name,
    city,
    state,
    membership
FROM CUSTOMERS_RAW;


-- Create product dimension
CREATE OR REPLACE TABLE DIM_PRODUCT (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    price NUMBER(12,2)
);


-- Load product dimension
INSERT INTO DIM_PRODUCT
SELECT
    product_id,
    product_name,
    category,
    brand,
    price
FROM PRODUCTS_RAW;


-- Create branch dimension
CREATE OR REPLACE TABLE DIM_BRANCH (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(50),
    manager_name VARCHAR(100)
);


-- Load branch dimension
INSERT INTO DIM_BRANCH
SELECT
    branch_id,
    branch_name,
    city,
    state,
    region,
    manager_name
FROM BRANCHES_RAW;


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
FROM CALENDAR_RAW;


-- Create fact table
CREATE OR REPLACE TABLE FACT_SALES (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(14,2)
);


-- Load fact table
INSERT INTO FACT_SALES
SELECT
    sale_id,
    customer_id,
    product_id,
    branch_id,
    date_id,
    quantity,
    total_amount
FROM SALES_RAW;


-- Verify fact table
SELECT * FROM FACT_SALES;


-- Check dimension record counts
SELECT 'DIM_CUSTOMER' AS TABLE_NAME, COUNT(*) AS ROW_COUNT
FROM DIM_CUSTOMER
UNION ALL
SELECT 'DIM_PRODUCT', COUNT(*)
FROM DIM_PRODUCT
UNION ALL
SELECT 'DIM_BRANCH', COUNT(*)
FROM DIM_BRANCH
UNION ALL
SELECT 'DIM_DATE', COUNT(*)
FROM DIM_DATE
UNION ALL
SELECT 'FACT_SALES', COUNT(*)
FROM FACT_SALES;


-- Check duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS row_count
FROM DIM_CUSTOMER
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Check duplicate product IDs
SELECT
    product_id,
    COUNT(*) AS row_count
FROM DIM_PRODUCT
GROUP BY product_id
HAVING COUNT(*) > 1;


-- Check duplicate branch IDs
SELECT
    branch_id,
    COUNT(*) AS row_count
FROM DIM_BRANCH
GROUP BY branch_id
HAVING COUNT(*) > 1;


-- Check duplicate date IDs
SELECT
    date_id,
    COUNT(*) AS row_count
FROM DIM_DATE
GROUP BY date_id
HAVING COUNT(*) > 1;


-- Validate customer foreign keys
SELECT COUNT(*) AS invalid_customer_keys
FROM FACT_SALES f
LEFT JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Validate product foreign keys
SELECT COUNT(*) AS invalid_product_keys
FROM FACT_SALES f
LEFT JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
WHERE p.product_id IS NULL;


-- Validate branch foreign keys
SELECT COUNT(*) AS invalid_branch_keys
FROM FACT_SALES f
LEFT JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
WHERE b.branch_id IS NULL;


-- Validate date foreign keys
SELECT COUNT(*) AS invalid_date_keys
FROM FACT_SALES f
LEFT JOIN DIM_DATE d
    ON f.date_id = d.date_id
WHERE d.date_id IS NULL;


-- Display complete star schema sales report
SELECT
    f.sale_id,
    c.customer_name,
    p.product_name,
    p.category,
    p.brand,
    b.branch_name,
    b.city AS branch_city,
    b.state,
    b.region,
    d.date,
    d.month,
    d.quarter,
    d.year,
    f.quantity,
    f.total_amount
FROM FACT_SALES f
INNER JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
INNER JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
INNER JOIN DIM_DATE d
    ON f.date_id = d.date_id
ORDER BY f.sale_id;


-- Customer-wise sales report
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_sales
FROM FACT_SALES f
INNER JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_sales DESC;


-- Product-wise revenue report
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_revenue DESC;


-- Branch-wise revenue report
SELECT
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.city,
    b.state
ORDER BY total_revenue DESC;


-- State-wise revenue report
SELECT
    b.state,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY b.state
ORDER BY total_revenue DESC;


-- Monthly revenue report
SELECT
    d.year,
    d.month,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_DATE d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.month
ORDER BY
    d.year,
    MIN(d.date);


-- Quarterly revenue report
SELECT
    d.year,
    d.quarter,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_DATE d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.quarter
ORDER BY
    d.year,
    d.quarter;


-- Category-wise revenue
SELECT
    p.category,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- Top 10 customers
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.total_amount) AS total_sales
FROM FACT_SALES f
INNER JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
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
FROM FACT_SALES f
INNER JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Top 10 performing branches
SELECT
    b.branch_id,
    b.branch_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Customer purchase trend
SELECT
    c.customer_id,
    c.customer_name,
    d.year,
    d.month,
    COUNT(f.sale_id) AS purchase_count,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_spending
FROM FACT_SALES f
INNER JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
INNER JOIN DIM_DATE d
    ON f.date_id = d.date_id
GROUP BY
    c.customer_id,
    c.customer_name,
    d.year,
    d.month
ORDER BY
    c.customer_id,
    d.year,
    MIN(d.date);


-- Product performance dashboard
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue,
    AVG(f.total_amount) AS average_sale_amount
FROM FACT_SALES f
INNER JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand
ORDER BY revenue DESC;


-- Branch performance dashboard
SELECT
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region,
    COUNT(f.sale_id) AS transaction_count,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region
ORDER BY revenue DESC;


-- Regional sales analysis
SELECT
    b.region,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY b.region
ORDER BY total_revenue DESC;


-- Daily sales trend
SELECT
    d.date,
    SUM(f.total_amount) AS daily_revenue
FROM FACT_SALES f
INNER JOIN DIM_DATE d
    ON f.date_id = d.date_id
GROUP BY d.date
ORDER BY d.date;


-- Top customer using ROW_NUMBER
WITH CUSTOMER_TOTALS AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(f.total_amount) AS total_sales
    FROM FACT_SALES f
    INNER JOIN DIM_CUSTOMER c
        ON f.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_sales,
    ROW_NUMBER() OVER (
        ORDER BY total_sales DESC
    ) AS customer_rank
FROM CUSTOMER_TOTALS
ORDER BY customer_rank;


-- Top product using ROW_NUMBER
WITH PRODUCT_TOTALS AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(f.total_amount) AS total_revenue
    FROM FACT_SALES f
    INNER JOIN DIM_PRODUCT p
        ON f.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.product_name
)
SELECT
    product_id,
    product_name,
    total_revenue,
    ROW_NUMBER() OVER (
        ORDER BY total_revenue DESC
    ) AS product_rank
FROM PRODUCT_TOTALS
ORDER BY product_rank;


-- Sales trend with running revenue
WITH DAILY_SALES AS (
    SELECT
        d.date,
        SUM(f.total_amount) AS daily_revenue
    FROM FACT_SALES f
    INNER JOIN DIM_DATE d
        ON f.date_id = d.date_id
    GROUP BY d.date
)
SELECT
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM DAILY_SALES
ORDER BY date;


-- Create customer revenue view
CREATE OR REPLACE VIEW CUSTOMER_REVENUE AS
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.state,
    c.membership,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
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


-- Create branch revenue view
CREATE OR REPLACE VIEW BRANCH_REVENUE AS
SELECT
    b.branch_id,
    b.branch_name,
    b.city,
    b.state,
    b.region,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
INNER JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
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


-- Display the table structure
DESC TABLE FACT_SALES;

DESC TABLE DIM_CUSTOMER;

DESC TABLE DIM_PRODUCT;

DESC TABLE DIM_BRANCH;

DESC TABLE DIM_DATE;