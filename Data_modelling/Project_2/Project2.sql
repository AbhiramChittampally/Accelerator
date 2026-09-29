-- Task 1: Create the warehouse
CREATE WAREHOUSE IF NOT EXISTS RETAIL_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Task 2: Create the database
CREATE DATABASE IF NOT EXISTS RETAIL_DB;

-- Task 3: Create the schema
CREATE SCHEMA IF NOT EXISTS RETAIL_DB.SALES_SCHEMA;

-- Select the warehouse, database and schema
USE WAREHOUSE RETAIL_WH;
USE DATABASE RETAIL_DB;
USE SCHEMA SALES_SCHEMA;

-- Verify the current environment
SELECT
    CURRENT_WAREHOUSE() AS CURRENT_WAREHOUSE,
    CURRENT_DATABASE() AS CURRENT_DATABASE,
    CURRENT_SCHEMA() AS CURRENT_SCHEMA;

-- Task 4: Create the CSV file format
CREATE FILE FORMAT IF NOT EXISTS RETAIL_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ',';

-- Verify the file format
SHOW FILE FORMATS;

-- Task 5: Create the internal stage
CREATE STAGE IF NOT EXISTS RETAIL_STAGE
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Verify the stage
SHOW STAGES;

-- Task 6: Upload customers.csv, products.csv, branches.csv and sales.csv using the Snowflake UI

-- Verify the uploaded files
LIST @RETAIL_STAGE;

-- Task 7: Create the CUSTOMERS table
CREATE TABLE IF NOT EXISTS CUSTOMERS (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    membership VARCHAR(20)
);

-- Create the PRODUCTS table
CREATE TABLE IF NOT EXISTS PRODUCTS (
    product_id INTEGER,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMBER(10,2)
);

-- Create the BRANCHES table
CREATE TABLE IF NOT EXISTS BRANCHES (
    branch_id INTEGER,
    branch_name VARCHAR(100),
    city VARCHAR(50)
);

-- Create the SALES table
CREATE TABLE IF NOT EXISTS SALES (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    quantity INTEGER,
    sale_date DATE,
    total_amount NUMBER(12,2)
);

-- Verify the tables
SHOW TABLES;

-- Task 8: Load customers.csv
COPY INTO CUSTOMERS
FROM @RETAIL_STAGE/customers.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load products.csv
COPY INTO PRODUCTS
FROM @RETAIL_STAGE/products.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load branches.csv
COPY INTO BRANCHES
FROM @RETAIL_STAGE/branches.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Load sales.csv
COPY INTO SALES
FROM @RETAIL_STAGE/sales.csv
FILE_FORMAT = RETAIL_CSV_FORMAT;

-- Task 9: Verify customer records
SELECT *
FROM CUSTOMERS;

-- Verify product records
SELECT *
FROM PRODUCTS;

-- Verify branch records
SELECT *
FROM BRANCHES;

-- Verify sales records
SELECT *
FROM SALES;

-- Task 10: Display all customers
SELECT *
FROM CUSTOMERS;

-- Task 11: Display all products
SELECT *
FROM PRODUCTS;

-- Task 12: Display all branches
SELECT *
FROM BRANCHES;

-- Task 13: Display all sales transactions
SELECT *
FROM SALES;

-- Task 14: Calculate total business revenue
SELECT
    SUM(total_amount) AS total_revenue
FROM SALES;

-- Task 15: Generate customer-wise sales
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    total_spent DESC;

-- Task 16: Generate branch-wise sales
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_sales
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY
    total_sales DESC;

-- Task 17: Generate product-wise sales
SELECT
    p.product_id,
    p.product_name,
    SUM(s.total_amount) AS total_revenue
FROM PRODUCTS p
INNER JOIN SALES s
    ON p.product_id = s.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    total_revenue DESC;

-- Task 18: Generate category-wise sales
SELECT
    p.category,
    SUM(s.total_amount) AS total_revenue
FROM PRODUCTS p
INNER JOIN SALES s
    ON p.product_id = s.product_id
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;

-- Task 19: Display the highest revenue branch
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_sales
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY
    total_sales DESC
LIMIT 1;

-- Task 20: Display the highest spending customer
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    total_spent DESC
LIMIT 1;

-- Task 21: Display the top three products by revenue
SELECT
    p.product_id,
    p.product_name,
    SUM(s.total_amount) AS total_revenue
FROM PRODUCTS p
INNER JOIN SALES s
    ON p.product_id = s.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    total_revenue DESC
LIMIT 3;

-- Task 22: Display the top three customers by spending
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_spent
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    total_spent DESC
LIMIT 3;

-- Task 23: Rank customers based on total spending
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_spent,
    RANK() OVER (
        ORDER BY SUM(s.total_amount) DESC
    ) AS customer_rank
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    customer_rank;

-- Task 24: Rank branches based on total sales
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_sales,
    RANK() OVER (
        ORDER BY SUM(s.total_amount) DESC
    ) AS branch_rank
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY
    branch_rank;

-- Task 25: Display the top-selling product in each category
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(s.total_amount) AS total_revenue
    FROM PRODUCTS p
    INNER JOIN SALES s
        ON p.product_id = s.product_id
    GROUP BY
        p.category,
        p.product_id,
        p.product_name
),
ranked_products AS (
    SELECT
        category,
        product_id,
        product_name,
        total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS product_rank
    FROM product_revenue
)
SELECT
    category,
    product_id,
    product_name,
    total_revenue
FROM ranked_products
WHERE product_rank = 1
ORDER BY category;

-- Task 26: Calculate cumulative sales
SELECT
    sale_id,
    sale_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY sale_date, sale_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_sales
FROM SALES
ORDER BY
    sale_date,
    sale_id;

-- Task 27: Calculate average sale amount using a window function
SELECT
    sale_id,
    sale_date,
    total_amount,
    AVG(total_amount) OVER () AS average_sale_amount
FROM SALES
ORDER BY
    sale_id;

-- Task 28: Generate customer-wise revenue using a CTE
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(s.total_amount) AS total_spent
    FROM CUSTOMERS c
    INNER JOIN SALES s
        ON c.customer_id = s.customer_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_spent
FROM customer_revenue
ORDER BY
    total_spent DESC;

-- Task 29: Display customers spending above average
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(s.total_amount) AS total_spent
    FROM CUSTOMERS c
    INNER JOIN SALES s
        ON c.customer_id = s.customer_id
    GROUP BY
        c.customer_id,
        c.customer_name
),
average_revenue AS (
    SELECT
        AVG(total_spent) AS average_spending
    FROM customer_revenue
)
SELECT
    cr.customer_id,
    cr.customer_name,
    cr.total_spent
FROM customer_revenue cr
CROSS JOIN average_revenue ar
WHERE cr.total_spent > ar.average_spending
ORDER BY
    cr.total_spent DESC;

-- Task 30: Create the SALES_REPORT view
CREATE OR REPLACE VIEW SALES_REPORT AS
SELECT
    s.sale_id,
    c.customer_name,
    p.product_name,
    p.category,
    b.branch_name,
    s.quantity,
    s.sale_date,
    s.total_amount
FROM SALES s
INNER JOIN CUSTOMERS c
    ON s.customer_id = c.customer_id
INNER JOIN PRODUCTS p
    ON s.product_id = p.product_id
INNER JOIN BRANCHES b
    ON s.branch_id = b.branch_id;

-- Task 31: Query the SALES_REPORT view
SELECT *
FROM SALES_REPORT;

-- Task 32: Create the TOP_CUSTOMERS materialized view
CREATE OR REPLACE MATERIALIZED VIEW TOP_CUSTOMERS
AS
SELECT
    customer_id,
    SUM(total_amount) AS total_spent
FROM SALES
GROUP BY
    customer_id;

-- Task 33: Query the TOP_CUSTOMERS materialized view
SELECT
    tc.customer_id,
    c.customer_name,
    tc.total_spent
FROM TOP_CUSTOMERS tc
INNER JOIN CUSTOMERS c
    ON tc.customer_id = c.customer_id
ORDER BY
    tc.total_spent DESC
LIMIT 3;