-- Task 1: Create the warehouse
CREATE WAREHOUSE IF NOT EXISTS ENTERPRISE_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Task 2: Create the database
CREATE DATABASE IF NOT EXISTS ENTERPRISE_DB;

-- Task 3: Create the schema
CREATE SCHEMA IF NOT EXISTS ENTERPRISE_DB.SALES_SCHEMA;

-- Select the warehouse, database and schema
USE WAREHOUSE ENTERPRISE_WH;
USE DATABASE ENTERPRISE_DB;
USE SCHEMA SALES_SCHEMA;

-- Verify the current environment
SELECT
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();

-- Task 4: Create the CSV file format
CREATE FILE FORMAT IF NOT EXISTS ENTERPRISE_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ',';

-- Verify the file format
SHOW FILE FORMATS;

-- Task 5: Create the internal stage
CREATE STAGE IF NOT EXISTS ENTERPRISE_STAGE
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Verify the stage
SHOW STAGES;

-- Task 6: Upload customers.csv, products.csv, branches.csv, sales_history.csv and new_sales.csv using the Snowflake UI

-- Verify uploaded files
LIST @ENTERPRISE_STAGE;

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
    price NUMBER(12,2)
);

-- Create the BRANCHES table
CREATE TABLE IF NOT EXISTS BRANCHES (
    branch_id INTEGER,
    branch_name VARCHAR(100),
    state VARCHAR(50)
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

-- Create the incremental staging table
CREATE TABLE IF NOT EXISTS SALES_INCREMENTAL_STAGE (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    quantity INTEGER,
    sale_date DATE,
    total_amount NUMBER(12,2)
);

-- Task 8: Load customers.csv
COPY INTO CUSTOMERS
FROM @ENTERPRISE_STAGE/customers.csv
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Load products.csv
COPY INTO PRODUCTS
FROM @ENTERPRISE_STAGE/products.csv
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Load branches.csv
COPY INTO BRANCHES
FROM @ENTERPRISE_STAGE/branches.csv
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Load historical sales
COPY INTO SALES
FROM @ENTERPRISE_STAGE/sales_history.csv
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Task 9: Verify customers
SELECT *
FROM CUSTOMERS
ORDER BY customer_id;

-- Verify products
SELECT *
FROM PRODUCTS
ORDER BY product_id;

-- Verify branches
SELECT *
FROM BRANCHES
ORDER BY branch_id;

-- Verify historical sales
SELECT *
FROM SALES
ORDER BY sale_id;

-- Task 10: Create a stream on the incremental staging table
CREATE OR REPLACE STREAM SALES_INCREMENTAL_STREAM
ON TABLE SALES_INCREMENTAL_STAGE;

-- Verify the stream
SHOW STREAMS;

-- Task 11: Load new sales into the incremental staging table
COPY INTO SALES_INCREMENTAL_STAGE
FROM @ENTERPRISE_STAGE/new_sales.csv
FILE_FORMAT = ENTERPRISE_CSV_FORMAT;

-- Task 12: Display newly inserted records captured by the stream
SELECT
    sale_id,
    customer_id,
    product_id,
    branch_id,
    quantity,
    sale_date,
    total_amount,
    METADATA$ACTION AS action,
    METADATA$ISUPDATE AS is_update
FROM SALES_INCREMENTAL_STREAM
WHERE METADATA$ACTION = 'INSERT';

-- Task 13: Merge new records into SALES
MERGE INTO SALES AS target
USING (
    SELECT
        sale_id,
        customer_id,
        product_id,
        branch_id,
        quantity,
        sale_date,
        total_amount
    FROM SALES_INCREMENTAL_STREAM
    WHERE METADATA$ACTION = 'INSERT'
) AS source
ON target.sale_id = source.sale_id
WHEN NOT MATCHED THEN
    INSERT (
        sale_id,
        customer_id,
        product_id,
        branch_id,
        quantity,
        sale_date,
        total_amount
    )
    VALUES (
        source.sale_id,
        source.customer_id,
        source.product_id,
        source.branch_id,
        source.quantity,
        source.sale_date,
        source.total_amount
    );

-- Verify the incremental load
SELECT *
FROM SALES
ORDER BY sale_id;

-- Task 14: Identify duplicate sale IDs
SELECT
    sale_id,
    COUNT(*) AS duplicate_count
FROM SALES
GROUP BY sale_id
HAVING COUNT(*) > 1;

-- Task 15: Identify missing customer IDs
SELECT
    s.sale_id,
    s.customer_id
FROM SALES s
LEFT JOIN CUSTOMERS c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Task 16: Display invalid product IDs
SELECT
    s.sale_id,
    s.product_id
FROM SALES s
LEFT JOIN PRODUCTS p
    ON s.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Task 17: Count newly inserted records
SELECT
    COUNT(*) AS new_sales_count
FROM SALES
WHERE sale_id BETWEEN 6 AND 10;

-- Task 18: Delete one sales record
DELETE FROM SALES
WHERE sale_id = 10;

-- Save the query ID of the DELETE statement
SET DELETE_QUERY_ID = LAST_QUERY_ID();

-- Verify that sale 10 was deleted
SELECT *
FROM SALES
WHERE sale_id = 10;

-- Task 19: Recover the deleted record using Time Travel
SELECT *
FROM SALES
BEFORE (STATEMENT => $DELETE_QUERY_ID)
WHERE sale_id = 10;

-- Task 20: Insert the deleted record back into SALES
INSERT INTO SALES (
    sale_id,
    customer_id,
    product_id,
    branch_id,
    quantity,
    sale_date,
    total_amount
)
SELECT
    sale_id,
    customer_id,
    product_id,
    branch_id,
    quantity,
    sale_date,
    total_amount
FROM SALES
BEFORE (STATEMENT => $DELETE_QUERY_ID)
WHERE sale_id = 10;

-- Verify the recovered record
SELECT *
FROM SALES
WHERE sale_id = 10;

-- Task 21: Create a zero-copy clone
CREATE OR REPLACE TABLE SALES_TEST
CLONE SALES;

-- Task 22: Display cloned records
SELECT *
FROM SALES_TEST
ORDER BY sale_id;

-- Task 23: Insert a test record into the clone
INSERT INTO SALES_TEST (
    sale_id,
    customer_id,
    product_id,
    branch_id,
    quantity,
    sale_date,
    total_amount
)
VALUES (
    999,
    1,
    101,
    1,
    1,
    '2026-07-20',
    60000
);

-- Verify the new record exists in the clone
SELECT *
FROM SALES_TEST
WHERE sale_id = 999;

-- Task 24: Verify the original table is unchanged
SELECT *
FROM SALES
WHERE sale_id = 999;

-- Task 25: Create the daily incremental loading task
CREATE OR REPLACE TASK DAILY_INCREMENTAL_SALES_LOAD
    WAREHOUSE = ENTERPRISE_WH
    SCHEDULE = 'USING CRON 0 0 * * * Asia/Kolkata'
    WHEN SYSTEM$STREAM_HAS_DATA('SALES_INCREMENTAL_STREAM')
AS
    MERGE INTO SALES AS target
    USING (
        SELECT
            sale_id,
            customer_id,
            product_id,
            branch_id,
            quantity,
            sale_date,
            total_amount
        FROM SALES_INCREMENTAL_STREAM
        WHERE METADATA$ACTION = 'INSERT'
    ) AS source
    ON target.sale_id = source.sale_id
    WHEN NOT MATCHED THEN
        INSERT (
            sale_id,
            customer_id,
            product_id,
            branch_id,
            quantity,
            sale_date,
            total_amount
        )
        VALUES (
            source.sale_id,
            source.customer_id,
            source.product_id,
            source.branch_id,
            source.quantity,
            source.sale_date,
            source.total_amount
        );

-- Task 26: Resume the task
ALTER TASK DAILY_INCREMENTAL_SALES_LOAD RESUME;

-- Verify the task
SHOW TASKS;

-- Task 27: Check task execution history
SELECT
    NAME,
    STATE,
    QUERY_ID,
    SCHEDULED_TIME,
    COMPLETED_TIME,
    ERROR_MESSAGE
FROM TABLE(
    INFORMATION_SCHEMA.TASK_HISTORY(
        TASK_NAME => 'DAILY_INCREMENTAL_SALES_LOAD'
    )
)
ORDER BY SCHEDULED_TIME DESC;

-- Task 28: Customer revenue report
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_revenue
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC;

-- Task 29: Branch revenue report
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_revenue
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY total_revenue DESC;

-- Task 30: Product revenue report
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
ORDER BY total_revenue DESC;

-- Task 31: Monthly revenue report
SELECT
    DATE_TRUNC('MONTH', sale_date) AS sales_month,
    SUM(total_amount) AS monthly_revenue
FROM SALES
GROUP BY
    DATE_TRUNC('MONTH', sale_date)
ORDER BY sales_month;

-- Task 32: Highest revenue customer
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_revenue
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC
LIMIT 1;

-- Task 33: Highest revenue branch
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_revenue
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name
ORDER BY total_revenue DESC
LIMIT 1;

-- Task 34: Top five products
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
ORDER BY total_revenue DESC
LIMIT 5;

-- Task 35: Customer purchase frequency
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(s.sale_id) AS purchase_count
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY purchase_count DESC;

-- Task 36: Running revenue
SELECT
    sale_id,
    sale_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY sale_date, sale_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM SALES
ORDER BY
    sale_date,
    sale_id;

-- Task 37: Customer ranking
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(s.total_amount) DESC
    ) AS customer_rank
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY customer_rank;

-- Task 38: Create the customer revenue view
CREATE OR REPLACE VIEW CUSTOMER_REVENUE AS
SELECT
    c.customer_id,
    c.customer_name,
    SUM(s.total_amount) AS total_revenue
FROM CUSTOMERS c
INNER JOIN SALES s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name;

-- Display customer revenue
SELECT *
FROM CUSTOMER_REVENUE
ORDER BY total_revenue DESC;

-- Task 39: Create the branch revenue materialized view
-- This requires Snowflake Enterprise Edition
-- CREATE OR REPLACE MATERIALIZED VIEW BRANCH_REVENUE AS
-- SELECT
--     branch_id,
--     SUM(total_amount) AS total_revenue
-- FROM SALES
-- GROUP BY branch_id;

-- Task 39 fallback: Create a normal view because your account does not support materialized views
CREATE OR REPLACE VIEW BRANCH_REVENUE AS
SELECT
    b.branch_id,
    b.branch_name,
    SUM(s.total_amount) AS total_revenue
FROM BRANCHES b
INNER JOIN SALES s
    ON b.branch_id = s.branch_id
GROUP BY
    b.branch_id,
    b.branch_name;

-- Task 40: Display branch revenue
SELECT *
FROM BRANCH_REVENUE
ORDER BY total_revenue DESC;