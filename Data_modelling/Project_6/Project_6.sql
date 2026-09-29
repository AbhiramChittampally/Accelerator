-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS RETAIL6_WH
WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;


-- Create database
CREATE DATABASE IF NOT EXISTS RETAIL6_DB;


-- Create schema
CREATE SCHEMA IF NOT EXISTS RETAIL6_DB.SALES_SCHEMA;


-- Select warehouse
USE WAREHOUSE RETAIL6_WH;


-- Select database
USE DATABASE RETAIL6_DB;


-- Select schema
USE SCHEMA SALES_SCHEMA;


-- Check current environment
SELECT
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();


-- Create CSV file format
CREATE FILE FORMAT IF NOT EXISTS RETAIL6_CSV_FORMAT
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_DELIMITER = ','
FIELD_OPTIONALLY_ENCLOSED_BY = '"';


-- Create internal stage
CREATE STAGE IF NOT EXISTS RETAIL6_STAGE
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Check stage
LIST @RETAIL6_STAGE;


-- Create raw customers table
CREATE OR REPLACE TABLE RAW_CUSTOMERS (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    membership VARCHAR(50)
);


-- Create raw products table
CREATE OR REPLACE TABLE RAW_PRODUCTS (
    product_id INTEGER,
    product_name VARCHAR(100),
    category VARCHAR(100),
    brand VARCHAR(100),
    price NUMBER(12,2)
);


-- Create raw branches table
CREATE OR REPLACE TABLE RAW_BRANCHES (
    branch_id INTEGER,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(100),
    manager_name VARCHAR(100)
);


-- Create raw calendar table
CREATE OR REPLACE TABLE RAW_CALENDAR (
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
CREATE OR REPLACE TABLE RAW_SALES (
    sale_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(14,2)
);


-- Load customers
COPY INTO RAW_CUSTOMERS
FROM @RETAIL6_STAGE/customers.csv
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Load products
COPY INTO RAW_PRODUCTS
FROM @RETAIL6_STAGE/products.csv
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Load branches
COPY INTO RAW_BRANCHES
FROM @RETAIL6_STAGE/branches.csv
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Load calendar
COPY INTO RAW_CALENDAR
FROM @RETAIL6_STAGE/calendar.csv
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Load sales
COPY INTO RAW_SALES
FROM @RETAIL6_STAGE/sales.csv
FILE_FORMAT = RETAIL6_CSV_FORMAT;


-- Verify raw data
SELECT COUNT(*) AS CUSTOMER_COUNT
FROM RAW_CUSTOMERS;

SELECT COUNT(*) AS PRODUCT_COUNT
FROM RAW_PRODUCTS;

SELECT COUNT(*) AS BRANCH_COUNT
FROM RAW_BRANCHES;

SELECT COUNT(*) AS CALENDAR_COUNT
FROM RAW_CALENDAR;

SELECT COUNT(*) AS SALES_COUNT
FROM RAW_SALES;


-- Create region dimension
CREATE OR REPLACE TABLE DIM_REGION (
    region_id INTEGER PRIMARY KEY,
    region_name VARCHAR(100) UNIQUE
);


-- Create state dimension
CREATE OR REPLACE TABLE DIM_STATE (
    state_id INTEGER PRIMARY KEY,
    state_name VARCHAR(100) UNIQUE,
    region_id INTEGER,
    FOREIGN KEY (region_id)
        REFERENCES DIM_REGION(region_id)
);


-- Create city dimension
CREATE OR REPLACE TABLE DIM_CITY (
    city_id INTEGER PRIMARY KEY,
    city_name VARCHAR(100),
    state_id INTEGER,
    FOREIGN KEY (state_id)
        REFERENCES DIM_STATE(state_id)
);


-- Create category dimension
CREATE OR REPLACE TABLE DIM_CATEGORY (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE
);


-- Create brand dimension
CREATE OR REPLACE TABLE DIM_BRAND (
    brand_id INTEGER PRIMARY KEY,
    brand_name VARCHAR(100),
    category_id INTEGER,
    FOREIGN KEY (category_id)
        REFERENCES DIM_CATEGORY(category_id)
);


-- Create year dimension
CREATE OR REPLACE TABLE DIM_YEAR (
    year_id INTEGER PRIMARY KEY,
    year_value INTEGER UNIQUE
);


-- Create quarter dimension
CREATE OR REPLACE TABLE DIM_QUARTER (
    quarter_id INTEGER PRIMARY KEY,
    quarter_name VARCHAR(20),
    year_id INTEGER,
    FOREIGN KEY (year_id)
        REFERENCES DIM_YEAR(year_id)
);


-- Create month dimension
CREATE OR REPLACE TABLE DIM_MONTH (
    month_id INTEGER PRIMARY KEY,
    month_name VARCHAR(20),
    quarter_id INTEGER,
    FOREIGN KEY (quarter_id)
        REFERENCES DIM_QUARTER(quarter_id)
);


-- Create customer dimension
CREATE OR REPLACE TABLE DIM_CUSTOMER (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city_id INTEGER,
    membership VARCHAR(50),
    FOREIGN KEY (city_id)
        REFERENCES DIM_CITY(city_id)
);


-- Create product dimension
CREATE OR REPLACE TABLE DIM_PRODUCT (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    brand_id INTEGER,
    price NUMBER(12,2),
    FOREIGN KEY (brand_id)
        REFERENCES DIM_BRAND(brand_id)
);


-- Create branch dimension
CREATE OR REPLACE TABLE DIM_BRANCH (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR(100),
    city_id INTEGER,
    manager_name VARCHAR(100),
    FOREIGN KEY (city_id)
        REFERENCES DIM_CITY(city_id)
);


-- Create date dimension
CREATE OR REPLACE TABLE DIM_DATE (
    date_id INTEGER PRIMARY KEY,
    date_value DATE,
    day INTEGER,
    day_name VARCHAR(20),
    week_no INTEGER,
    month_id INTEGER,
    is_weekend VARCHAR(10),
    FOREIGN KEY (month_id)
        REFERENCES DIM_MONTH(month_id)
);


-- Insert regions
INSERT INTO DIM_REGION
SELECT
    ROW_NUMBER() OVER (ORDER BY region),
    region
FROM (
    SELECT DISTINCT region
    FROM RAW_BRANCHES
);


-- Insert states
INSERT INTO DIM_STATE
SELECT
    ROW_NUMBER() OVER (ORDER BY state),
    state,
    r.region_id
FROM (
    SELECT DISTINCT state, region
    FROM RAW_BRANCHES
) b
JOIN DIM_REGION r
    ON b.region = r.region_name;


-- Insert cities
INSERT INTO DIM_CITY
SELECT
    ROW_NUMBER() OVER (ORDER BY city, state),
    city,
    s.state_id
FROM (
    SELECT DISTINCT city, state
    FROM (
        SELECT city, state
        FROM RAW_CUSTOMERS

        UNION

        SELECT city, state
        FROM RAW_BRANCHES
    )
) c
JOIN DIM_STATE s
    ON c.state = s.state_name;


-- Insert categories
INSERT INTO DIM_CATEGORY
SELECT
    ROW_NUMBER() OVER (ORDER BY category),
    category
FROM (
    SELECT DISTINCT category
    FROM RAW_PRODUCTS
);


-- Insert brands
INSERT INTO DIM_BRAND
SELECT
    ROW_NUMBER() OVER (ORDER BY brand, category),
    brand,
    c.category_id
FROM (
    SELECT DISTINCT brand, category
    FROM RAW_PRODUCTS
) p
JOIN DIM_CATEGORY c
    ON p.category = c.category_name;


-- Insert years
INSERT INTO DIM_YEAR
SELECT
    ROW_NUMBER() OVER (ORDER BY year),
    year
FROM (
    SELECT DISTINCT year
    FROM RAW_CALENDAR
);


-- Insert quarters
INSERT INTO DIM_QUARTER
SELECT
    ROW_NUMBER() OVER (ORDER BY year, quarter),
    quarter,
    y.year_id
FROM (
    SELECT DISTINCT year, quarter
    FROM RAW_CALENDAR
) c
JOIN DIM_YEAR y
    ON c.year = y.year_value;


-- Insert months
INSERT INTO DIM_MONTH
SELECT
    ROW_NUMBER() OVER (ORDER BY year, quarter, month),
    month,
    q.quarter_id
FROM (
    SELECT DISTINCT year, quarter, month
    FROM RAW_CALENDAR
) c
JOIN DIM_YEAR y
    ON c.year = y.year_value
JOIN DIM_QUARTER q
    ON q.year_id = y.year_id
    AND q.quarter_name = c.quarter;


-- Insert customers
INSERT INTO DIM_CUSTOMER
SELECT
    c.customer_id,
    c.customer_name,
    city.city_id,
    c.membership
FROM RAW_CUSTOMERS c
JOIN DIM_CITY city
    ON c.city = city.city_name
JOIN DIM_STATE state
    ON city.state_id = state.state_id
    AND c.state = state.state_name;


-- Insert products
INSERT INTO DIM_PRODUCT
SELECT
    p.product_id,
    p.product_name,
    b.brand_id,
    p.price
FROM RAW_PRODUCTS p
JOIN DIM_BRAND b
    ON p.brand = b.brand_name
JOIN DIM_CATEGORY c
    ON p.category = c.category_name
    AND b.category_id = c.category_id;


-- Insert branches
INSERT INTO DIM_BRANCH
SELECT
    b.branch_id,
    b.branch_name,
    city.city_id,
    b.manager_name
FROM RAW_BRANCHES b
JOIN DIM_CITY city
    ON b.city = city.city_name
JOIN DIM_STATE state
    ON city.state_id = state.state_id
    AND b.state = state.state_name;


-- Insert dates
INSERT INTO DIM_DATE
SELECT
    c.date_id,
    c.date,
    c.day,
    c.day_name,
    c.week_no,
    m.month_id,
    c.is_weekend
FROM RAW_CALENDAR c
JOIN DIM_YEAR y
    ON c.year = y.year_value
JOIN DIM_QUARTER q
    ON q.year_id = y.year_id
    AND q.quarter_name = c.quarter
JOIN DIM_MONTH m
    ON m.quarter_id = q.quarter_id
    AND m.month_name = c.month;


-- Create fact table
CREATE OR REPLACE TABLE FACT_SALES (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    branch_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount NUMBER(14,2),

    FOREIGN KEY (customer_id)
        REFERENCES DIM_CUSTOMER(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES DIM_PRODUCT(product_id),

    FOREIGN KEY (branch_id)
        REFERENCES DIM_BRANCH(branch_id),

    FOREIGN KEY (date_id)
        REFERENCES DIM_DATE(date_id)
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
FROM RAW_SALES;


-- Verify fact table
SELECT COUNT(*) AS FACT_SALES_COUNT
FROM FACT_SALES;


-- Customer-wise revenue
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC;


-- Product-wise revenue
SELECT
    p.product_id,
    p.product_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_revenue DESC;


-- Brand-wise revenue
SELECT
    br.brand_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
JOIN DIM_BRAND br
    ON p.brand_id = br.brand_id
GROUP BY br.brand_name
ORDER BY total_revenue DESC;


-- Category-wise revenue
SELECT
    c.category_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
JOIN DIM_BRAND br
    ON p.brand_id = br.brand_id
JOIN DIM_CATEGORY c
    ON br.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_revenue DESC;


-- City-wise sales
SELECT
    city.city_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
JOIN DIM_CITY city
    ON b.city_id = city.city_id
GROUP BY city.city_name
ORDER BY total_revenue DESC;


-- State-wise revenue
SELECT
    state.state_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
JOIN DIM_CITY city
    ON b.city_id = city.city_id
JOIN DIM_STATE state
    ON city.state_id = state.state_id
GROUP BY state.state_name
ORDER BY total_revenue DESC;


-- Region-wise revenue
SELECT
    region.region_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
JOIN DIM_CITY city
    ON b.city_id = city.city_id
JOIN DIM_STATE state
    ON city.state_id = state.state_id
JOIN DIM_REGION region
    ON state.region_id = region.region_id
GROUP BY region.region_name
ORDER BY total_revenue DESC;


-- Monthly revenue
SELECT
    y.year_value,
    m.month_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_DATE d
    ON f.date_id = d.date_id
JOIN DIM_MONTH m
    ON d.month_id = m.month_id
JOIN DIM_QUARTER q
    ON m.quarter_id = q.quarter_id
JOIN DIM_YEAR y
    ON q.year_id = y.year_id
GROUP BY
    y.year_value,
    m.month_name
ORDER BY
    y.year_value,
    m.month_name;


-- Quarterly revenue
SELECT
    y.year_value,
    q.quarter_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_DATE d
    ON f.date_id = d.date_id
JOIN DIM_MONTH m
    ON d.month_id = m.month_id
JOIN DIM_QUARTER q
    ON m.quarter_id = q.quarter_id
JOIN DIM_YEAR y
    ON q.year_id = y.year_id
GROUP BY
    y.year_value,
    q.quarter_name
ORDER BY
    y.year_value,
    q.quarter_name;


-- Top 10 customers
SELECT
    c.customer_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Top 10 products
SELECT
    p.product_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Top 10 branches
SELECT
    b.branch_name,
    SUM(f.total_amount) AS total_revenue
FROM FACT_SALES f
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Customer purchase trend
SELECT
    c.customer_name,
    d.date_value,
    SUM(f.quantity) AS quantity_purchased,
    SUM(f.total_amount) AS revenue
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id
JOIN DIM_DATE d
    ON f.date_id = d.date_id
GROUP BY
    c.customer_name,
    d.date_value
ORDER BY
    c.customer_name,
    d.date_value;


-- Product performance dashboard
SELECT
    p.product_name,
    br.brand_name,
    cat.category_name,
    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id
JOIN DIM_BRAND br
    ON p.brand_id = br.brand_id
JOIN DIM_CATEGORY cat
    ON br.category_id = cat.category_id
GROUP BY
    p.product_name,
    br.brand_name,
    cat.category_name
ORDER BY revenue DESC;


-- Regional sales dashboard
SELECT
    region.region_name,
    state.state_name,
    city.city_name,
    SUM(f.total_amount) AS revenue
FROM FACT_SALES f
JOIN DIM_BRANCH b
    ON f.branch_id = b.branch_id
JOIN DIM_CITY city
    ON b.city_id = city.city_id
JOIN DIM_STATE state
    ON city.state_id = state.state_id
JOIN DIM_REGION region
    ON state.region_id = region.region_id
GROUP BY
    region.region_name,
    state.state_name,
    city.city_name
ORDER BY
    region.region_name,
    revenue DESC;


-- Display the complete normalized sales model
SELECT
    f.sale_id,

    c.customer_name,
    customer_city.city_name AS customer_city,
    customer_state.state_name AS customer_state,

    p.product_name,
    brand.brand_name,
    category.category_name,

    branch.branch_name,
    branch_city.city_name AS branch_city,
    branch_state.state_name AS branch_state,
    region.region_name,

    d.date_value,
    month.month_name,
    quarter.quarter_name,
    year.year_value,

    f.quantity,
    f.total_amount

FROM FACT_SALES f

JOIN DIM_CUSTOMER c
    ON f.customer_id = c.customer_id

JOIN DIM_CITY customer_city
    ON c.city_id = customer_city.city_id

JOIN DIM_STATE customer_state
    ON customer_city.state_id = customer_state.state_id

JOIN DIM_PRODUCT p
    ON f.product_id = p.product_id

JOIN DIM_BRAND brand
    ON p.brand_id = brand.brand_id

JOIN DIM_CATEGORY category
    ON brand.category_id = category.category_id

JOIN DIM_BRANCH branch
    ON f.branch_id = branch.branch_id

JOIN DIM_CITY branch_city
    ON branch.city_id = branch_city.city_id

JOIN DIM_STATE branch_state
    ON branch_city.state_id = branch_state.state_id

JOIN DIM_REGION region
    ON branch_state.region_id = region.region_id

JOIN DIM_DATE d
    ON f.date_id = d.date_id

JOIN DIM_MONTH month
    ON d.month_id = month.month_id

JOIN DIM_QUARTER quarter
    ON month.quarter_id = quarter.quarter_id

JOIN DIM_YEAR year
    ON quarter.year_id = year.year_id

ORDER BY f.sale_id;


-- Show primary keys
SHOW PRIMARY KEYS IN SCHEMA RETAIL6_DB.SALES_SCHEMA;


-- Show foreign keys
SHOW IMPORTED KEYS IN SCHEMA RETAIL6_DB.SALES_SCHEMA;