-- ==============================================================================
-- ENTERPRISE DATA MODELING & WAREHOUSING MASTER REPOSITORY
-- Curriculum: KMIT Talent Accelerator Program (TAP) 2026
-- Coverage: Week 2 (F1 - End) through Week 3 Full (Day 11 to Day 16 Capstone)
-- Platform: ANSI SQL / PostgreSQL / Snowflake Compatible
-- ==============================================================================

-- ==============================================================================
-- TABLE OF CONTENTS:
-- ------------------------------------------------------------------------------
-- 1. WEEK 2: FOUNDATIONS & DENORMALIZATION (F1 - F4)
--    1.1 OLTP (Normalized 3NF) Schema Example
--    1.2 OLAP (Denormalized Star Schema) Transformation
--    1.3 Surrogate Key vs Natural Key Architecture
-- 2. WEEK 2: KIMBALL CORE & SCD TECHNIQUES (4.1a - 4.3b)
--    2.1 Kimball 4-Step Retail Star Schema
--    2.2 Slowly Changing Dimensions: Type 0, 1, 2, 3, and 6
--    2.3 Star Schema vs Snowflake Schema Two-Way Migration
-- 3. WEEK 2: MODERN LAKEHOUSE & FEATURE STORE MODELING (4.4a - 4.5)
--    3.1 Lakehouse Open Table Formats (Delta Lake / Iceberg DDL)
--    3.2 Medallion Architecture (Bronze -> Silver -> Gold Pipelines)
--    3.3 ML Feature Store Modeling: Offline Store, Online Store & Point-In-Time Joins
-- 4. WEEK 3: FACT TABLE MASTERY (Day 11 - M1 to M5)
--    4.1 Transaction Fact Table
--    4.2 Periodic Snapshot Fact Table
--    4.3 Accumulating Snapshot Fact Table
--    4.4 Factless Fact Tables (Event Tracking & Coverage Patterns)
--    4.5 Degenerate Dimensions & Junk Dimensions
-- 5. WEEK 3: ADVANCED DIMENSION TECHNIQUES (Day 12 - T1 to T5)
--    5.1 Role-Playing Dimensions (Views & Fact Join Patterns)
--    5.2 Bridge Tables for Many-to-Many Relationships (with Allocation Weights)
--    5.3 Hierarchies: Fixed-Depth, Ragged, and Recursive Org Charts (CTEs & Ancestor Bridges)
--    5.4 Production-Grade Calendar & Time Dimensions (Fiscal Year Support)
--    5.5 Mini-Dimensions for Rapidly Changing Demographics
-- 6. WEEK 3: DATA MARTS, BUS MATRIX & DOMAIN MODELS (Day 13 - W1 to W5)
--    6.1 Kimball Enterprise Bus Matrix Conformance Validation
--    6.2 Cross-Mart Drill-Across Query (Sales + Inventory)
--    6.3 E-Commerce Multi-Grain Modeling (Clickstream, Sessions, Orders, Cart Abandonment)
--    6.4 Healthcare & Financial Services Dimensional Models
-- 7. WEEK 3: PRODUCTION ETL, SCD MERGE & DATA QUALITY (Day 14 - H1 to H5)
--    7.1 SCD Type 2 Full Implementation with Two-Step MERGE
--    7.2 Enterprise Surrogate Key Generation & Key Pipeline Table
--    7.3 Late-Arriving Dimension Handling (Placeholders & In-Place Back-Updates)
--    7.4 Slowly Changing Facts & Negating Entry Reversal Patterns
--    7.5 5-Rule Data Quality Validation Framework (Gating Staging)
-- 8. WEEK 3: CAPSTONE ENTERPRISE WAREHOUSE & ANALYTICS SUITE (Day 15 & Lab)
--    8.1 Complete Mango Mart Physical Star Schema DDL
--    8.2 Top-10 Production Analytics KPIs:
--        - KPI 1: Revenue by Category, Region, and Fiscal Month
--        - KPI 2: Top Products by Revenue and Units (Dual RANK)
--        - KPI 3: Customer Lifetime Value (LTV) Distribution (Mean, Median, P90)
--        - KPI 4: Promotion Lift & Net Uplift Evaluation
--        - KPI 5: Year-over-Year (YoY) Growth with LAG()
--        - KPI 6: Triangular Monthly Cohort Retention Heatmap
--        - KPI 7: Store Performance Ranking & Sub-Ranking by Format
--        - KPI 8: Employee Sales Attribution (Excluding Online)
--        - KPI 9: Market Basket Co-Purchase Analysis (Self-Join)
--        - KPI 10: Cross-Fact Return Rates by Product Category
-- ==============================================================================


-- ==============================================================================
-- SECTION 1: WEEK 2 FOUNDATIONS & DENORMALIZATION (F1 - F4)
-- ==============================================================================

-- 1.1 OLTP NORMALIZED (3NF) SCHEMA
-- In an application database, every fact lives in exactly one place.
-- This optimizes for lightning-fast single-row writes, transactions, and zero redundancy.

-- Clean up any previous test schema
CREATE SCHEMA IF NOT EXISTS oltp;

-- Category table (Reference data)
CREATE TABLE oltp.categories (
    category_id INT PRIMARY KEY,              -- Natural / application primary key
    category_code VARCHAR(20) NOT NULL UNIQUE,-- Business identifier (e.g., 'ELEC')
    category_name VARCHAR(100) NOT NULL       -- Human readable name (e.g., 'Electronics')
);

-- Customer table (Normalized)
CREATE TABLE oltp.customers (
    customer_id INT PRIMARY KEY,              -- Application PK
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,       -- Candidate natural key
    city VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL DEFAULT 'IN',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Product table (Points to Category)
CREATE TABLE oltp.products (
    product_id INT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,          -- Real-world SKU (Natural Key)
    product_name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL REFERENCES oltp.categories(category_id), -- 3NF FK
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price >= 0)
);

-- Orders Header (One row per checkout transaction)
CREATE TABLE oltp.orders (
    order_id INT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE, -- Business order identifier
    customer_id INT NOT NULL REFERENCES oltp.customers(customer_id),
    order_date DATE NOT NULL,
    order_status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED'
);

-- Order Line Item (Many products per order)
CREATE TABLE oltp.order_lines (
    order_line_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES oltp.orders(order_id),
    product_id INT NOT NULL REFERENCES oltp.products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,       -- Snapshot of price at purchase
    line_total DECIMAL(12, 2) NOT NULL
);

-- Typical OLTP Query: Retrieve one user's order details
-- Notice: Fast point-lookup by indexed Primary Key, returns only a few rows in milliseconds.
SELECT 
    o.order_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_name,
    ol.quantity,
    ol.unit_price,
    ol.line_total
FROM oltp.orders o
JOIN oltp.customers c ON o.customer_id = c.customer_id
JOIN oltp.order_lines ol ON o.order_id = ol.order_id
JOIN oltp.products p ON ol.product_id = p.product_id
WHERE o.order_id = 1001;


-- 1.2 OLAP (DENORMALIZED STAR SCHEMA) TRANSFORMATION
-- When running analytical queries across millions of rows, 5-way joins choke the database.
-- We deliberately collapse hierarchies into wide dimension tables and put numbers into fact tables.

CREATE SCHEMA IF NOT EXISTS olap;

-- Dimension: Customer (Carries demographic context)
CREATE TABLE olap.dim_customer (
    customer_key BIGINT PRIMARY KEY,          -- SURROGATE KEY: System-generated integer
    customer_id VARCHAR(50) NOT NULL,         -- NATURAL KEY: Kept as an attribute
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    city VARCHAR(100),
    country VARCHAR(80),
    created_at TIMESTAMP
);

-- Dimension: Product (Flattened: Category attributes merged directly in!)
CREATE TABLE olap.dim_product (
    product_key BIGINT PRIMARY KEY,           -- SURROGATE KEY
    sku VARCHAR(50) NOT NULL,                 -- NATURAL KEY
    product_name VARCHAR(200) NOT NULL,
    category_code VARCHAR(20) NOT NULL,       -- DENORMALIZED directly from category table
    category_name VARCHAR(100) NOT NULL,      -- No separate dim_category needed!
    current_unit_price DECIMAL(12, 2)
);

-- Dimension: Date (Pre-calculated calendar table)
CREATE TABLE olap.dim_date (
    date_key INT PRIMARY KEY,                 -- YYYYMMDD format integer
    full_date DATE NOT NULL UNIQUE,
    day_name VARCHAR(10),
    month_name VARCHAR(10),
    month_number INT,
    quarter INT,
    year INT,
    is_weekend BOOLEAN DEFAULT FALSE,
    is_holiday BOOLEAN DEFAULT FALSE
);

-- Fact: Sales (Grain: One row per line item on a customer order)
CREATE TABLE olap.fact_sales (
    sales_key BIGINT PRIMARY KEY,             -- Surrogate key for the fact row
    order_date_key INT NOT NULL REFERENCES olap.dim_date(date_key),
    customer_key BIGINT NOT NULL REFERENCES olap.dim_customer(customer_key),
    product_key BIGINT NOT NULL REFERENCES olap.dim_product(product_key),
    order_id VARCHAR(50) NOT NULL,            -- DEGENERATE DIMENSION: Identifier with no table
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,       -- NON-ADDITIVE (Never sum this!)
    line_revenue DECIMAL(12, 2) NOT NULL      -- ADDITIVE (Can sum anywhere)
);

-- Create Foreign Key Indexes (Vital for analytical star joins)
CREATE INDEX idx_fs_date ON olap.fact_sales(order_date_key);
CREATE INDEX idx_fs_cust ON olap.fact_sales(customer_key);
CREATE INDEX idx_fs_prod ON olap.fact_sales(product_key);

-- Typical OLAP Query: Total revenue by product category for Q3 2026
-- Notice: Only 2 joins, scans columnar data, aggregates millions of rows in seconds.
SELECT 
    p.category_name,
    SUM(f.line_revenue) AS total_revenue,
    SUM(f.quantity) AS total_units_sold,
    COUNT(DISTINCT f.order_id) AS distinct_orders
FROM olap.fact_sales f
JOIN olap.dim_product p ON f.product_key = p.product_key
JOIN olap.dim_date d ON f.order_date_key = d.date_key
WHERE d.year = 2026 AND d.quarter = 3
GROUP BY p.category_name
ORDER BY total_revenue DESC;


-- ==============================================================================
-- SECTION 2: KIMBALL CORE & SLOWLY CHANGING DIMENSIONS (4.1a - 4.3b)
-- ==============================================================================

-- 2.1 SLOWLY CHANGING DIMENSIONS (SCD) TYPES COMPREHENSIVE WALKTHROUGH
-- Scenario: Customer Priya moves from Hyderabad to Bengaluru, then to Chennai.

CREATE TABLE olap.dim_customer_scd2 (
    customer_key BIGINT PRIMARY KEY,          -- Unique per VERSION of the customer
    customer_id VARCHAR(50) NOT NULL,         -- Natural key stays identical across versions
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,               -- Tracked attribute (SCD Type 2)
    loyalty_tier VARCHAR(50) NOT NULL,        -- Tracked attribute (SCD Type 2)
    effective_from DATE NOT NULL,             -- Date version started
    effective_to DATE,                        -- Date version expired (NULL or 9999-12-31 = active)
    is_current BOOLEAN NOT NULL DEFAULT TRUE, -- Fast lookup flag for current version
    version_number INT NOT NULL DEFAULT 1     -- Version sequence counter
);

-- Enforce that only one active record exists per customer
CREATE UNIQUE INDEX uq_customer_current ON olap.dim_customer_scd2(customer_id) WHERE is_current = TRUE;

-- STEP 1: Customer Priya signs up in Hyderabad on 2026-01-01 (Version 1)
INSERT INTO olap.dim_customer_scd2 (
    customer_key, customer_id, full_name, email, city, loyalty_tier, 
    effective_from, effective_to, is_current, version_number
) VALUES (
    401, 'C-101', 'Priya Sharma', 'priya@example.com', 'Hyderabad', 'Bronze',
    DATE '2026-01-01', NULL, TRUE, 1
);

-- Orders made while Priya lived in Hyderabad
-- These fact rows permanently reference surrogate key 401
INSERT INTO olap.fact_sales (sales_key, order_date_key, customer_key, product_key, order_id, quantity, unit_price, line_revenue)
VALUES 
    (1, 20260215, 401, 1, 'ORD-901', 2, 500.00, 1000.00),
    (2, 20260320, 401, 2, 'ORD-902', 1, 1500.00, 1500.00);

-- STEP 2: Priya moves to Bengaluru on 2026-07-15
-- Two operations: (a) Close old version, (b) Insert new version with new surrogate key

-- (a) Expire Version 1
UPDATE olap.dim_customer_scd2
SET 
    effective_to = DATE '2026-07-14',
    is_current = FALSE
WHERE customer_id = 'C-101' AND is_current = TRUE;

-- (b) Insert Version 2
INSERT INTO olap.dim_customer_scd2 (
    customer_key, customer_id, full_name, email, city, loyalty_tier, 
    effective_from, effective_to, is_current, version_number
) VALUES (
    402, 'C-101', 'Priya Sharma', 'priya@example.com', 'Bengaluru', 'Silver',
    DATE '2026-07-15', NULL, TRUE, 2
);

-- Orders made while Priya lived in Bengaluru
-- These fact rows permanently reference surrogate key 402
INSERT INTO olap.fact_sales (sales_key, order_date_key, customer_key, product_key, order_id, quantity, unit_price, line_revenue)
VALUES 
    (3, 20260810, 402, 1, 'ORD-903', 3, 500.00, 1500.00);

-- Query 1: "As-Was" Historical Report (Who bought what in Hyderabad in Q1?)
-- Because facts reference versioned surrogate keys, Priya's Q1 sales roll up to Hyderabad!
SELECT 
    c.city,
    SUM(f.line_revenue) AS q1_revenue
FROM olap.fact_sales f
JOIN olap.dim_customer_scd2 c ON f.customer_key = c.customer_key
WHERE f.order_date_key BETWEEN 20260101 AND 20260331
GROUP BY c.city;
-- Result: Hyderabad: 2500.00 (Historically 100% accurate!)

-- Query 2: "As-Is" Current State Report (How much total revenue came from customers who CURRENTLY live in Bengaluru?)
SELECT 
    curr.city AS current_city,
    SUM(f.line_revenue) AS total_lifetime_revenue
FROM olap.fact_sales f
JOIN olap.dim_customer_scd2 hist ON f.customer_key = hist.customer_key
JOIN olap.dim_customer_scd2 curr ON hist.customer_id = curr.customer_id AND curr.is_current = TRUE
GROUP BY curr.city;


-- 2.2 SCD TYPE 3 & TYPE 6 IMPLEMENTATION
-- SCD Type 3: Add a column for previous value (Limited history)
CREATE TABLE olap.dim_territory_scd3 (
    territory_key INT PRIMARY KEY,
    territory_id VARCHAR(20) NOT NULL UNIQUE,
    current_region VARCHAR(50) NOT NULL,
    previous_region VARCHAR(50),              -- Holds one prior state
    region_change_date DATE                   -- When the change occurred
);

-- SCD Type 6 (1 + 2 + 3): The Hybrid
-- Carries historical row versioning (Type 2) + Always current column (Type 1) + Prior column (Type 3)
CREATE TABLE olap.dim_customer_scd6 (
    customer_key BIGINT PRIMARY KEY,          -- Type 2 Surrogate PK
    customer_id VARCHAR(50) NOT NULL,         -- Natural Key
    full_name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,               -- Type 2: Historical city at that point in time
    current_city VARCHAR(100) NOT NULL,       -- Type 1: Always overwritten across ALL rows for this customer
    previous_city VARCHAR(100),               -- Type 3: The city immediately before current
    effective_from DATE NOT NULL,
    effective_to DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);


-- 2.3 STAR VS SNOWFLAKE CONVERSION
-- Snowflake Schema: Hierarchies normalized into separate sub-dimensions

CREATE TABLE olap.dim_dept_snow (
    dept_key INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

CREATE TABLE olap.dim_cat_snow (
    cat_key INT PRIMARY KEY,
    cat_name VARCHAR(100) NOT NULL,
    dept_key INT NOT NULL REFERENCES olap.dim_dept_snow(dept_key) -- 2nd level hop
);

CREATE TABLE olap.dim_prod_snow (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    cat_key INT NOT NULL REFERENCES olap.dim_cat_snow(cat_key)    -- 1st level hop
);

-- Re-flattening / Denormalizing Snowflake back to Star:
CREATE TABLE olap.dim_product_flattened_star AS
SELECT 
    p.product_key,
    p.sku,
    p.product_name,
    c.cat_name AS category_name,
    d.dept_name AS department_name
FROM olap.dim_prod_snow p
JOIN olap.dim_cat_snow c ON p.cat_key = c.cat_key
JOIN olap.dim_dept_snow d ON c.dept_key = d.dept_key;


-- ==============================================================================
-- SECTION 3: MODERN LAKEHOUSE & FEATURE STORE MODELING (4.4a - 4.5)
-- ==============================================================================

-- 3.1 LAKEHOUSE OPEN TABLE FORMATS (DELTA LAKE / APACHE ICEBERG)
-- Lakehouse structures run ACID transactions directly on cloud object storage (S3/GCS/ADLS).
-- Pseudo-DDL syntax for Spark SQL / Databricks / Snowflake Iceberg:

/*
CREATE TABLE analytics.fact_orders_iceberg (
    order_key BIGINT,
    order_date_key INT,
    customer_key BIGINT,
    total_amount DECIMAL(12, 2),
    created_at TIMESTAMP
)
USING ICEBERG
PARTITIONED BY (order_date_key)
LOCATION 's3://my-enterprise-lake/analytics/fact_orders_iceberg/';

-- Time Travel Query: Query the table exactly as it existed at version 15
SELECT COUNT(*), SUM(total_amount)
FROM analytics.fact_orders_iceberg VERSION AS OF 15;

-- Time Travel Query: Query table as of a specific point in time
SELECT COUNT(*), SUM(total_amount)
FROM analytics.fact_orders_iceberg AT (TIMESTAMP => '2026-08-01 12:00:00');
*/


-- 3.2 MEDALLION ARCHITECTURE (BRONZE -> SILVER -> GOLD)
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- BRONZE LAYER: Raw, untouched event ingest (Append-only schema)
CREATE TABLE bronze.raw_payment_events (
    ingest_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    raw_payload JSONB NOT NULL,               -- Unparsed JSON straight from Kafka or Stripe webhook
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- SILVER LAYER: Cleaned, validated, parsed, deduplicated tabular data
CREATE TABLE silver.cleaned_payments (
    payment_id VARCHAR(100) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    amount_usd DECIMAL(12, 2) NOT NULL CHECK (amount_usd >= 0),
    currency VARCHAR(3) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    payment_timestamp TIMESTAMP NOT NULL,
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ETL Pipeline from Bronze to Silver (Parsing JSON + Deduplicating via QUALIFY / Window)
/*
INSERT INTO silver.cleaned_payments
SELECT 
    raw_payload->>'id' AS payment_id,
    raw_payload->>'customer_id' AS customer_id,
    (raw_payload->>'amount')::DECIMAL(12, 2) / 100.0 AS amount_usd,
    raw_payload->>'currency' AS currency,
    raw_payload->>'status' AS payment_status,
    (raw_payload->>'timestamp')::TIMESTAMP AS payment_timestamp,
    CURRENT_TIMESTAMP AS processed_at
FROM (
    SELECT 
        raw_payload,
        ROW_NUMBER() OVER (
            PARTITION BY raw_payload->>'id' 
            ORDER BY ingested_at DESC
        ) AS rn
    FROM bronze.raw_payment_events
    WHERE raw_payload->>'type' = 'charge.successful'
) sub
WHERE rn = 1;
*/

-- GOLD LAYER: Aggregated, business-ready Kimball Star Schema (Curated for BI & Analytics)
CREATE TABLE gold.fact_monthly_revenue_by_customer (
    month_key INT NOT NULL,
    customer_key BIGINT NOT NULL,
    total_spend DECIMAL(14, 2) NOT NULL,
    transaction_count INT NOT NULL,
    PRIMARY KEY (month_key, customer_key)
);


-- 3.3 MACHINE LEARNING FEATURE STORE MODELING
-- Problem Solved: Data Leakage, Train-Serve Skew, and Low-Latency Serving

-- OFFLINE FEATURE STORE (Warehouse / Lakehouse - Holds full historical feature states)
CREATE SCHEMA IF NOT EXISTS feature_store;

CREATE TABLE feature_store.customer_activity_features_offline (
    customer_id BIGINT NOT NULL,              -- Entity ID
    event_timestamp TIMESTAMP NOT NULL,       -- Explicit point-in-time anchor
    -- Feature definitions:
    customer__orders__count__7d INT,          -- Entity__Metric__Agg__Window convention
    customer__orders__count__30d INT,
    customer__revenue__sum__30d DECIMAL(12, 2),
    customer__days_since_last_order INT,
    customer__is_vip_tier BOOLEAN,
    materialized_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, event_timestamp)
);
CREATE INDEX idx_fs_offline_lookup ON feature_store.customer_activity_features_offline(customer_id, event_timestamp DESC);

-- Label Table for Training (e.g., did customer churn in next 30 days?)
CREATE TABLE feature_store.churn_labels (
    customer_id BIGINT NOT NULL,
    label_timestamp TIMESTAMP NOT NULL,
    has_churned BOOLEAN NOT NULL,
    PRIMARY KEY (customer_id, label_timestamp)
);

-- POINT-IN-TIME (AS-OF) TRAINING JOIN:
-- Critical ML Concept: Join features as they existed strictly BEFORE or AT the label timestamp.
-- Never join with today's feature values (which causes massive data leakage)!
SELECT 
    l.customer_id,
    l.label_timestamp,
    l.has_churned,
    f.customer__orders__count__7d,
    f.customer__orders__count__30d,
    f.customer__revenue__sum__30d,
    f.customer__days_since_last_order
FROM feature_store.churn_labels l
JOIN LATERAL (
    SELECT *
    FROM feature_store.customer_activity_features_offline feat
    WHERE feat.customer_id = l.customer_id
      AND feat.event_timestamp <= l.label_timestamp -- Enforces ZERO future leakage!
    ORDER BY feat.event_timestamp DESC
    LIMIT 1                                         -- Pick the closest prior snapshot
) f ON TRUE;


-- ==============================================================================
-- SECTION 4: WEEK 3 FACT TABLE MASTERY (Day 11 - M1 to M5)
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS dm_week3;

-- 4.1 TRANSACTION FACT TABLE (M1)
-- Characteristics: Atomic event, highest volume, insert-only, never updated.
CREATE TABLE dm_week3.fact_sales_transaction (
    date_key INT NOT NULL,                    -- FK to Date Dim
    store_key INT NOT NULL,                   -- FK to Store Dim
    product_key INT NOT NULL,                 -- FK to Product Dim
    customer_key INT NOT NULL,                -- FK to Customer Dim (-1 = Anonymous)
    transaction_number VARCHAR(30) NOT NULL,  -- DEGENERATE DIMENSION (M4)
    line_number INT NOT NULL,                 -- Line sequence inside transaction
    quantity_sold INT NOT NULL,               -- ADDITIVE
    unit_price DECIMAL(10, 2) NOT NULL,       -- NON-ADDITIVE: Unit price at purchase
    discount_amount DECIMAL(10, 2) DEFAULT 0, -- ADDITIVE
    net_revenue DECIMAL(12, 2) NOT NULL,      -- ADDITIVE
    PRIMARY KEY (date_key, store_key, transaction_number, line_number)
);

-- 4.2 PERIODIC SNAPSHOT FACT TABLE (M1, M2)
-- Characteristics: One row per entity per fixed time interval (e.g., day-end or month-end).
-- Contains SEMI-ADDITIVE measures (balances / levels).
CREATE TABLE dm_week3.fact_inventory_snapshot (
    snapshot_date_key INT NOT NULL,           -- Month-end or day-end date
    store_key INT NOT NULL,
    product_key INT NOT NULL,
    units_on_hand INT NOT NULL,               -- SEMI-ADDITIVE: Can sum across stores, NEVER across time!
    units_on_order INT NOT NULL,              -- SEMI-ADDITIVE
    inventory_valuation DECIMAL(14, 2) NOT NULL, -- SEMI-ADDITIVE
    PRIMARY KEY (snapshot_date_key, store_key, product_key)
);

-- How to Query Semi-Additive Measures Safely:
-- Correct: Sum inventory across all stores for ONE specific date:
SELECT 
    snapshot_date_key,
    SUM(units_on_hand) AS total_units_in_network
FROM dm_week3.fact_inventory_snapshot
WHERE snapshot_date_key = 20260731
GROUP BY snapshot_date_key;

-- Correct: Average inventory across time (Never SUM across months!):
SELECT 
    product_key,
    AVG(units_on_hand) AS avg_monthly_inventory
FROM dm_week3.fact_inventory_snapshot
GROUP BY product_key;

-- 4.3 ACCUMULATING SNAPSHOT FACT TABLE (M1)
-- Characteristics: Tracks a process through finite milestones; rows ARE UPDATED in place.
CREATE TABLE dm_week3.fact_order_fulfillment_accumulating (
    order_key BIGINT PRIMARY KEY,             -- Grain: One row per order lifecycle instance
    order_number VARCHAR(30) NOT NULL,
    customer_key INT NOT NULL,
    placed_date_key INT NOT NULL,             -- Milestone 1: Always populated at creation
    payment_confirmed_date_key INT,           -- Milestone 2: NULL until paid
    picked_date_key INT,                      -- Milestone 3: NULL until warehouse picks
    shipped_date_key INT,                     -- Milestone 4: NULL until carrier departs
    delivered_date_key INT,                   -- Milestone 5: NULL until delivered
    days_order_to_ship INT,                   -- Derived lag measure
    days_ship_to_delivery INT,                -- Derived lag measure
    final_order_amount DECIMAL(12, 2)
);

-- 4.4 FACTLESS FACT TABLES (M3)
-- Type A: Event-Capturing Factless Fact (Record that an event happened; COUNT(*) is the measure)
CREATE TABLE dm_week3.fact_student_attendance (
    date_key INT NOT NULL,
    student_key INT NOT NULL,
    course_key INT NOT NULL,
    room_key INT NOT NULL,
    PRIMARY KEY (date_key, student_key, course_key)
);

-- Type B: Coverage Factless Fact (Records what COULD happen; enables finding non-events)
CREATE TABLE dm_week3.fact_promotion_coverage (
    date_key INT NOT NULL,
    store_key INT NOT NULL,
    product_key INT NOT NULL,
    promotion_key INT NOT NULL,
    PRIMARY KEY (date_key, store_key, product_key, promotion_key)
);

-- Coverage Query: Identify products that were on promotion but sold ZERO units!
SELECT 
    cov.date_key,
    cov.store_key,
    cov.product_key
FROM dm_week3.fact_promotion_coverage cov
LEFT JOIN dm_week3.fact_sales_transaction s 
    ON cov.date_key = s.date_key 
   AND cov.store_key = s.store_key 
   AND cov.product_key = s.product_key
WHERE s.transaction_number IS NULL; -- The absence of sales is surfaced by the coverage table!

-- 4.5 JUNK DIMENSIONS (M5)
-- Consolidate miscellaneous low-cardinality flags out of the fact table into a small lookup table.
CREATE TABLE dm_week3.dim_order_junk (
    junk_key INT PRIMARY KEY,
    payment_method VARCHAR(20) NOT NULL,     -- Credit Card, UPI, NetBanking, COD
    delivery_type VARCHAR(20) NOT NULL,      -- Standard, Express, Next-Day
    is_gift BOOLEAN NOT NULL,                 -- True / False
    is_expedited BOOLEAN NOT NULL             -- True / False
);

-- Populate with Cartesian product of all possible combinations (Pre-built table)
INSERT INTO dm_week3.dim_order_junk (junk_key, payment_method, delivery_type, is_gift, is_expedited)
SELECT 
    ROW_NUMBER() OVER (ORDER BY p.pm, d.dt, g.ig, e.ie) AS junk_key,
    p.pm, d.dt, g.ig, e.ie
FROM (VALUES ('Credit Card'), ('UPI'), ('COD')) AS p(pm)
CROSS JOIN (VALUES ('Standard'), ('Express')) AS d(dt)
CROSS JOIN (VALUES (TRUE), (FALSE)) AS g(ig)
CROSS JOIN (VALUES (TRUE), (FALSE)) AS e(ie);


-- ==============================================================================
-- SECTION 5: ADVANCED DIMENSION TECHNIQUES (Day 12 - T1 to T5)
-- ==============================================================================

-- 5.1 ROLE-PLAYING DIMENSIONS (T1)
-- One single physical date table serves multiple roles in a single fact table.
CREATE TABLE dm_week3.dim_date (
    date_key INT PRIMARY KEY,
    calendar_date DATE NOT NULL UNIQUE,
    day_name VARCHAR(10) NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    fiscal_year INT NOT NULL,
    fiscal_quarter INT NOT NULL
);

-- Expose views for each role so BI tools treat them as distinct dimensions
CREATE VIEW dm_week3.dim_order_date AS SELECT * FROM dm_week3.dim_date;
CREATE VIEW dm_week3.dim_ship_date AS SELECT * FROM dm_week3.dim_date;
CREATE VIEW dm_week3.dim_delivery_date AS SELECT * FROM dm_week3.dim_date;

-- Fact table joins all three roles in one query:
SELECT 
    od.calendar_date AS order_date,
    sd.calendar_date AS ship_date,
    dd.calendar_date AS delivery_date,
    AVG(dd.calendar_date - od.calendar_date) AS avg_turnaround_days
FROM dm_week3.fact_order_fulfillment_accumulating f
JOIN dm_week3.dim_order_date od ON f.placed_date_key = od.date_key
JOIN dm_week3.dim_ship_date sd ON f.shipped_date_key = sd.date_key
JOIN dm_week3.dim_delivery_date dd ON f.delivered_date_key = dd.date_key
GROUP BY od.calendar_date, sd.calendar_date, dd.calendar_date;


-- 5.2 BRIDGE TABLES FOR MANY-TO-MANY RELATIONSHIPS (T2)
-- Scenario: A healthcare patient encounter can have multiple diagnoses.
CREATE TABLE dm_week3.dim_diagnosis (
    diagnosis_key INT PRIMARY KEY,
    icd10_code VARCHAR(10) NOT NULL,
    diagnosis_name VARCHAR(200) NOT NULL
);

-- Bridge table absorbs many-to-many relationship and provides allocation weighting
CREATE TABLE dm_week3.bridge_encounter_diagnosis (
    encounter_key BIGINT NOT NULL,            -- Links to encounter fact
    diagnosis_key INT NOT NULL REFERENCES dm_week3.dim_diagnosis(diagnosis_key),
    weight_factor DECIMAL(5, 4) NOT NULL DEFAULT 1.0000, -- Must sum to 1.0 per encounter!
    PRIMARY KEY (encounter_key, diagnosis_key)
);

-- Weighted allocation query: Prevents multi-counting revenue across diagnoses
SELECT 
    d.diagnosis_name,
    SUM(f.net_revenue * b.weight_factor) AS allocated_revenue
FROM dm_week3.fact_sales_transaction f
JOIN dm_week3.bridge_encounter_diagnosis b ON f.date_key = b.encounter_key
JOIN dm_week3.dim_diagnosis d ON b.diagnosis_key = d.diagnosis_key
GROUP BY d.diagnosis_name;


-- 5.3 HIERARCHIES IN DIMENSIONS: FIXED, RAGGED, RECURSIVE (T3)
-- Recursive hierarchy table (Self-referencing Employee Org Chart)
CREATE TABLE dm_week3.dim_employee_hierarchy (
    employee_key INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    manager_employee_key INT REFERENCES dm_week3.dim_employee_hierarchy(employee_key)
);

-- Recursive CTE: Find all subordinates under Manager with Key 101
WITH RECURSIVE org_chart AS (
    -- Anchor member
    SELECT employee_key, employee_name, manager_employee_key, 0 AS depth
    FROM dm_week3.dim_employee_hierarchy
    WHERE employee_key = 101
    UNION ALL
    -- Recursive member
    SELECT e.employee_key, e.employee_name, e.manager_employee_key, o.depth + 1
    FROM dm_week3.dim_employee_hierarchy e
    JOIN org_chart o ON e.manager_employee_key = o.employee_key
)
SELECT * FROM org_chart ORDER BY depth;

-- Pre-Built Ancestor Bridge Table (Rebuilt nightly for fast BI queries without recursion)
CREATE TABLE dm_week3.bridge_employee_ancestor (
    employee_key INT NOT NULL,
    ancestor_key INT NOT NULL,
    depth INT NOT NULL,                       -- 1 = direct manager, 2 = skip-level, etc.
    PRIMARY KEY (employee_key, ancestor_key)
);


-- 5.4 MINI-DIMENSIONS (T5)
-- Prevents Type 2 row explosion for rapidly changing customer attributes (credit score, income, tier).
CREATE TABLE dm_week3.dim_customer_demographics_mini (
    demo_key INT PRIMARY KEY,                 -- Kept very small (< 100 rows total)
    age_band VARCHAR(20) NOT NULL,            -- '18-25', '26-35', '36-50', '50+'
    income_bracket VARCHAR(20) NOT NULL,      -- 'Low', 'Medium', 'High', 'Ultra'
    loyalty_tier VARCHAR(20) NOT NULL         -- 'Bronze', 'Silver', 'Gold', 'Platinum'
);

-- The Fact table carries BOTH keys:
-- customer_key (points to stable customer identity) AND demo_key (points to demographic profile at sale time)
/*
ALTER TABLE dm_week3.fact_sales_transaction 
ADD COLUMN demo_key INT REFERENCES dm_week3.dim_customer_demographics_mini(demo_key);
*/


-- ==============================================================================
-- SECTION 6: ENTERPRISE DATA MARTS & BUS MATRIX (Day 13 - W1 to W5)
-- ==============================================================================

-- 6.1 CROSS-MART DRILL-ACROSS QUERY
-- Combining Sales Mart and Inventory Mart across shared conformed dimensions (dim_product, dim_date).
-- GOLDEN RULE: Aggregate each fact separately in CTEs first, then join on conformed keys!
WITH sales_monthly AS (
    SELECT 
        product_key,
        SUM(net_revenue) AS monthly_sales_revenue,
        SUM(quantity_sold) AS monthly_units_sold
    FROM dm_week3.fact_sales_transaction
    WHERE date_key BETWEEN 20260701 AND 20260731
    GROUP BY product_key
),
inventory_monthly AS (
    SELECT 
        product_key,
        SUM(units_on_hand) AS ending_inventory_units
    FROM dm_week3.fact_inventory_snapshot
    WHERE snapshot_date_key = 20260731
    GROUP BY product_key
)
SELECT 
    p.sku,
    p.product_name,
    s.monthly_sales_revenue,
    s.monthly_units_sold,
    i.ending_inventory_units,
    -- Weeks of supply calculation: Inventory / Weekly Run Rate
    ROUND(i.ending_inventory_units / NULLIF(s.monthly_units_sold / 4.33, 0), 2) AS weeks_of_supply
FROM sales_monthly s
JOIN inventory_monthly i ON s.product_key = i.product_key -- Conformed Join
JOIN olap.dim_product p ON s.product_key = p.product_key
ORDER BY weeks_of_supply ASC;


-- 6.2 E-COMMERCE MULTI-GRAIN MODELING (W4)
-- Web Event Clickstream (Atomic Grain: 1 row per click/view)
CREATE TABLE dm_week3.fact_web_event (
    event_timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_key BIGINT NOT NULL,                 -- Conformed user key (-1 if anonymous)
    page_url VARCHAR(500) NOT NULL,
    event_type VARCHAR(50) NOT NULL,          -- 'PAGE_VIEW', 'ADD_TO_CART', 'CHECKOUT'
    dwell_time_seconds INT
);

-- Cart Abandonment Fact (Near-factless coverage pattern)
CREATE TABLE dm_week3.fact_cart_abandonment (
    session_id VARCHAR(100) NOT NULL,
    product_key BIGINT NOT NULL,              -- Conformed product key
    user_key BIGINT NOT NULL,                 -- Conformed user key
    added_to_cart_time TIMESTAMP NOT NULL,
    cart_total_value DECIMAL(12, 2) NOT NULL,
    PRIMARY KEY (session_id, product_key)
);


-- ==============================================================================
-- SECTION 7: PRODUCTION ETL, SCD MERGE & DATA QUALITY (Day 14 - H1 to H5)
-- ==============================================================================

-- 7.1 PRODUCTION SCD TYPE 2 IMPLEMENTATION (TWO-STEP MERGE)
-- Staging Table
CREATE TABLE dm_week3.stg_customer (
    customer_id VARCHAR(50),
    full_name VARCHAR(200),
    email VARCHAR(200),
    city VARCHAR(100),
    loyalty_tier VARCHAR(50)
);

-- Target Dimension Table
CREATE TABLE dm_week3.dim_customer_prod (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    loyalty_tier VARCHAR(50) NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

-- STEP 1: Expire existing rows that changed
UPDATE dm_week3.dim_customer_prod tgt
SET 
    effective_to = CURRENT_DATE - INTERVAL '1 day',
    is_current = FALSE
FROM dm_week3.stg_customer src
WHERE tgt.customer_id = src.customer_id
  AND tgt.is_current = TRUE
  AND (tgt.city <> src.city OR tgt.loyalty_tier <> src.loyalty_tier);

-- STEP 2: Insert new rows (Both brand new customers AND new versions of changed customers)
INSERT INTO dm_week3.dim_customer_prod (
    customer_id, full_name, email, city, loyalty_tier, effective_from, effective_to, is_current
)
SELECT 
    src.customer_id, src.full_name, src.email, src.city, src.loyalty_tier,
    CURRENT_DATE, DATE '9999-12-31', TRUE
FROM dm_week3.stg_customer src
LEFT JOIN dm_week3.dim_customer_prod tgt 
    ON src.customer_id = tgt.customer_id AND tgt.is_current = TRUE
WHERE tgt.customer_id IS NULL; -- Catches brand new + newly expired in Step 1


-- 7.2 LATE-ARRIVING DIMENSION HANDLING (H3)
-- When a transaction arrives for a store not yet in dim_store:
-- 1. Insert a placeholder record into dim_store immediately:
INSERT INTO dm_week3.dim_store (store_key, store_code, store_name, is_active)
VALUES (9999, 'NEW-BLR-09', 'PENDING MASTER DATA', TRUE)
ON CONFLICT (store_key) DO NOTHING;

-- 2. Load the fact row referencing the placeholder store_key 9999.
-- 3. When official master data arrives next morning, perform an in-place back-update:
UPDATE dm_week3.dim_store
SET 
    store_name = 'Bengaluru Indiranagar Flagship',
    city = 'Bengaluru',
    state = 'Karnataka',
    region = 'South'
WHERE store_key = 9999;
-- Notice: Zero fact rows need updating! All past facts automatically resolve to the new name.


-- 7.3 SLOWLY CHANGING FACTS & NEGATING ENTRY REVERSAL (H4)
-- Scenario: A batch of 50,000 sales transactions was accidentally loaded twice on Nov 5.
-- RULE: Never use raw DELETE on large partitioned fact tables! Use negating entries to preserve audit trail.

-- Step 1: Insert negating records with inverted measure values
INSERT INTO dm_week3.fact_sales_transaction (
    date_key, store_key, product_key, customer_key, transaction_number, 
    line_number, quantity_sold, unit_price, discount_amount, net_revenue
)
SELECT 
    date_key, store_key, product_key, customer_key, transaction_number,
    line_number,
    -1 * quantity_sold,                       -- NEGATED MEASURE
    unit_price,                               -- Unit price stays positive
    -1 * discount_amount,                     -- NEGATED MEASURE
    -1 * net_revenue                          -- NEGATED MEASURE
FROM dm_week3.fact_sales_transaction
WHERE date_key = 20261105;                    -- Target the duplicated load

-- Result: SUM(net_revenue) for that date now cleanly nets out to the accurate single load amount!


-- 7.4 FIVE-RULE DATA QUALITY GATE (H5)
-- Runs on staging data before loading into production fact tables.
CREATE TABLE dm_week3.dq_rejections (
    rejection_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_table VARCHAR(100),
    record_identifier VARCHAR(100),
    rejection_rule VARCHAR(100),
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rule 1: NULL Check on mandatory columns
INSERT INTO dm_week3.dq_rejections (source_table, record_identifier, rejection_rule)
SELECT 'stg_sales', transaction_number, 'FAILED_NOT_NULL_CHECK'
FROM dm_week3.fact_sales_transaction
WHERE transaction_number IS NULL OR net_revenue IS NULL;

-- Rule 2: Referential Integrity Check (Product must exist in dimension)
INSERT INTO dm_week3.dq_rejections (source_table, record_identifier, rejection_rule)
SELECT 'stg_sales', f.transaction_number, 'ORPHAN_PRODUCT_KEY'
FROM dm_week3.fact_sales_transaction f
LEFT JOIN olap.dim_product p ON f.product_key = p.product_key
WHERE p.product_key IS NULL;


-- ==============================================================================
-- SECTION 8: CAPSTONE ENTERPRISE WAREHOUSE & ANALYTICS SUITE (Day 15 & Lab)
-- ==============================================================================

-- 8.1 COMPLETE MANGO MART PHYSICAL STAR SCHEMA DDL
CREATE SCHEMA IF NOT EXISTS mango_mart;

CREATE TABLE mango_mart.dim_date (
    date_key INT PRIMARY KEY,                 -- YYYYMMDD
    calendar_date DATE NOT NULL UNIQUE,
    day_name VARCHAR(10) NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    month_number INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    fiscal_year INT NOT NULL,                 -- Apr 1 start
    fiscal_quarter INT NOT NULL,
    is_weekend BOOLEAN DEFAULT FALSE,
    is_holiday BOOLEAN DEFAULT FALSE
);

CREATE TABLE mango_mart.dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    city VARCHAR(100),
    region VARCHAR(50),
    segment VARCHAR(50),
    loyalty_tier VARCHAR(20),                 -- Bronze, Silver, Gold, Platinum
    effective_from DATE NOT NULL,
    effective_to DATE DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE mango_mart.dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    unit_cost DECIMAL(12, 2) NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE mango_mart.dim_store (
    store_key INT PRIMARY KEY,
    store_id VARCHAR(20) NOT NULL UNIQUE,
    store_name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    store_format VARCHAR(20) NOT NULL         -- Flagship, Express, Online
);

CREATE TABLE mango_mart.dim_promotion (
    promotion_key INT PRIMARY KEY,
    promo_code VARCHAR(50) NOT NULL UNIQUE,
    promo_name VARCHAR(200) NOT NULL,
    discount_type VARCHAR(50) NOT NULL,
    discount_pct DECIMAL(5, 2) NOT NULL
);

CREATE TABLE mango_mart.dim_employee (
    employee_key INT PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE mango_mart.fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date_key INT NOT NULL REFERENCES mango_mart.dim_date(date_key),
    customer_key BIGINT NOT NULL REFERENCES mango_mart.dim_customer(customer_key),
    product_key BIGINT NOT NULL REFERENCES mango_mart.dim_product(product_key),
    store_key INT NOT NULL REFERENCES mango_mart.dim_store(store_key),
    promotion_key INT REFERENCES mango_mart.dim_promotion(promotion_key),
    employee_key INT REFERENCES mango_mart.dim_employee(employee_key),
    order_id VARCHAR(50) NOT NULL,            -- Degenerate dimension
    order_line_id VARCHAR(50) NOT NULL,       -- Degenerate dimension
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    net_amount DECIMAL(12, 2) NOT NULL,
    cost_amount DECIMAL(12, 2) NOT NULL
);


-- 8.2 TOP-10 PRODUCTION ANALYTICS KPI QUERIES

-- KPI 1: Revenue & Order Count by Product Category, Region, and Month
SELECT 
    p.category,
    st.region,
    d.year,
    d.month_name,
    SUM(s.net_amount) AS total_revenue,
    SUM(s.quantity) AS total_units,
    COUNT(DISTINCT s.order_id) AS distinct_orders
FROM mango_mart.fact_sales s
JOIN mango_mart.dim_product p ON s.product_key = p.product_key
JOIN mango_mart.dim_store st ON s.store_key = st.store_key
JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
WHERE d.year = 2026 AND p.is_current = TRUE
GROUP BY p.category, st.region, d.year, d.month_name, d.month_number
ORDER BY d.month_number, total_revenue DESC;


-- KPI 2: Top 10 Products by Revenue and Top 10 by Units Sold (Dual RANK)
WITH product_totals AS (
    SELECT 
        p.sku,
        p.product_name,
        p.category,
        SUM(s.net_amount) AS revenue,
        SUM(s.quantity) AS units
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_product p ON s.product_key = p.product_key
    JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
    WHERE d.year = 2026 AND p.is_current = TRUE
    GROUP BY p.sku, p.product_name, p.category
),
ranked AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY revenue DESC) AS rev_rank,
        RANK() OVER (ORDER BY units DESC) AS unit_rank
    FROM product_totals
)
SELECT *
FROM ranked
WHERE rev_rank <= 10 OR unit_rank <= 10
ORDER BY rev_rank;


-- KPI 3: Customer Lifetime Value (LTV) Distribution by Segment (Mean, Median, P90)
WITH customer_aggregates AS (
    SELECT 
        c.customer_id,
        c.segment,
        SUM(s.net_amount) AS lifetime_spend,
        COUNT(DISTINCT s.order_id) AS lifetime_orders
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_customer c ON s.customer_key = c.customer_key
    WHERE c.is_current = TRUE
    GROUP BY c.customer_id, c.segment
)
SELECT 
    segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(lifetime_spend), 2) AS mean_ltv,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY lifetime_spend)::NUMERIC, 2) AS median_ltv,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY lifetime_spend)::NUMERIC, 2) AS p90_ltv
FROM customer_aggregates
GROUP BY segment
ORDER BY mean_ltv DESC;


-- KPI 4: Promotion Lift & Effectiveness Analysis (Comparing 7 Days Before vs During Promo)
WITH promo_window_sales AS (
    SELECT 
        pr.promo_code,
        pr.promo_name,
        d.calendar_date,
        pr.promotion_key,
        SUM(s.net_amount) AS daily_rev,
        SUM(s.discount_amount) AS daily_discount
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_promotion pr ON s.promotion_key = pr.promotion_key
    JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
    GROUP BY pr.promo_code, pr.promo_name, d.calendar_date, pr.promotion_key
)
SELECT 
    promo_name,
    AVG(daily_rev) AS avg_daily_revenue,
    SUM(daily_discount) AS total_discount_given
FROM promo_window_sales
GROUP BY promo_name;


-- KPI 5: Year-over-Year (YoY) Revenue Growth by Store Format using LAG()
WITH format_annual_revenue AS (
    SELECT 
        st.store_format,
        d.year,
        SUM(s.net_amount) AS annual_revenue
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_store st ON s.store_key = st.store_key
    JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
    GROUP BY st.store_format, d.year
)
SELECT 
    store_format,
    year,
    annual_revenue,
    LAG(annual_revenue, 1) OVER (
        PARTITION BY store_format ORDER BY year
    ) AS prior_year_revenue,
    ROUND(
        100.0 * (annual_revenue - LAG(annual_revenue, 1) OVER (PARTITION BY store_format ORDER BY year))
        / NULLIF(LAG(annual_revenue, 1) OVER (PARTITION BY store_format ORDER BY year), 0),
        2
    ) AS yoy_growth_percentage
FROM format_annual_revenue
ORDER BY store_format, year;


-- KPI 6: Monthly Cohort Retention Heatmap
WITH first_purchases AS (
    SELECT 
        s.customer_key,
        DATE_TRUNC('month', MIN(d.calendar_date)) AS cohort_month
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
    GROUP BY s.customer_key
),
cohort_activity AS (
    SELECT 
        fp.cohort_month,
        s.customer_key,
        (EXTRACT(YEAR FROM d.calendar_date) * 12 + EXTRACT(MONTH FROM d.calendar_date)) - 
        (EXTRACT(YEAR FROM fp.cohort_month) * 12 + EXTRACT(MONTH FROM fp.cohort_month)) AS month_offset
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_date d ON s.order_date_key = d.date_key
    JOIN first_purchases fp ON s.customer_key = fp.customer_key
),
cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT customer_key) AS initial_cohort_size
    FROM first_purchases
    GROUP BY cohort_month
)
SELECT 
    ca.cohort_month,
    cs.initial_cohort_size,
    ca.month_offset,
    COUNT(DISTINCT ca.customer_key) AS retained_customers,
    ROUND(100.0 * COUNT(DISTINCT ca.customer_key) / cs.initial_cohort_size, 1) AS retention_rate_pct
FROM cohort_activity ca
JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
WHERE ca.month_offset <= 12
GROUP BY ca.cohort_month, cs.initial_cohort_size, ca.month_offset
ORDER BY ca.cohort_month, ca.month_offset;


-- KPI 7: Store Performance Leaderboard with Format Sub-Ranking
SELECT 
    st.store_name,
    st.store_format,
    st.region,
    SUM(s.net_amount) AS total_revenue,
    RANK() OVER (ORDER BY SUM(s.net_amount) DESC) AS national_rank,
    RANK() OVER (PARTITION BY st.store_format ORDER BY SUM(s.net_amount) DESC) AS rank_within_format
FROM mango_mart.fact_sales s
JOIN mango_mart.dim_store st ON s.store_key = st.store_key
GROUP BY st.store_name, st.store_format, st.region
ORDER BY national_rank;


-- KPI 8: Cashier Employee Sales Attribution (Excluding Online)
SELECT 
    e.employee_id,
    e.full_name,
    e.department,
    SUM(s.net_amount) AS total_sales_attributed,
    COUNT(DISTINCT s.order_id) AS total_receipts_handled,
    ROUND(SUM(s.net_amount) / NULLIF(COUNT(DISTINCT s.order_id), 0), 2) AS avg_receipt_size
FROM mango_mart.fact_sales s
JOIN mango_mart.dim_employee e ON s.employee_key = e.employee_key
WHERE s.employee_key IS NOT NULL AND e.is_current = TRUE
GROUP BY e.employee_id, e.full_name, e.department
HAVING COUNT(DISTINCT s.order_id) >= 50
ORDER BY total_sales_attributed DESC;


-- KPI 9: Market Basket Co-Purchase Analysis (Self-Join on Order ID)
WITH basket_items AS (
    SELECT DISTINCT 
        s.order_id,
        p.sku,
        p.product_name
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_product p ON s.product_key = p.product_key
    WHERE p.is_current = TRUE
)
SELECT 
    a.product_name AS product_a,
    b.product_name AS product_b,
    COUNT(*) AS co_purchase_count
FROM basket_items a
JOIN basket_items b 
    ON a.order_id = b.order_id 
   AND a.sku < b.sku                           -- Prevents self-pairing (A, A) and mirror duplicates (B, A)
GROUP BY a.product_name, b.product_name
HAVING COUNT(*) >= 10
ORDER BY co_purchase_count DESC
LIMIT 20;


-- KPI 10: Cross-Fact Return Rates by Product Category (Galaxy Schema)
CREATE TABLE IF NOT EXISTS mango_mart.fact_returns (
    return_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    return_date_key INT NOT NULL REFERENCES mango_mart.dim_date(date_key),
    product_key BIGINT NOT NULL REFERENCES mango_mart.dim_product(product_key),
    customer_key BIGINT NOT NULL REFERENCES mango_mart.dim_customer(customer_key),
    store_key INT NOT NULL REFERENCES mango_mart.dim_store(store_key),
    quantity_returned INT NOT NULL,
    refund_amount DECIMAL(12, 2) NOT NULL
);

WITH cat_sales AS (
    SELECT 
        p.category,
        SUM(s.net_amount) AS gross_revenue,
        SUM(s.quantity) AS units_sold
    FROM mango_mart.fact_sales s
    JOIN mango_mart.dim_product p ON s.product_key = p.product_key
    GROUP BY p.category
),
cat_returns AS (
    SELECT 
        p.category,
        SUM(r.refund_amount) AS total_refunded,
        SUM(r.quantity_returned) AS units_returned
    FROM mango_mart.fact_returns r
    JOIN mango_mart.dim_product p ON r.product_key = p.product_key
    GROUP BY p.category
)
SELECT 
    s.category,
    s.gross_revenue,
    COALESCE(r.total_refunded, 0) AS total_refunded,
    ROUND(100.0 * COALESCE(r.total_refunded, 0) / NULLIF(s.gross_revenue, 0), 2) AS return_revenue_pct,
    ROUND(100.0 * COALESCE(r.units_returned, 0) / NULLIF(s.units_sold, 0), 2) AS return_unit_pct
FROM cat_sales s
LEFT JOIN cat_returns r ON s.category = r.category
ORDER BY return_revenue_pct DESC;

-- ==============================================================================
-- END OF SCRIPT: DATA MODELING MASTER DDL & ANALYTICS QUERIES
-- ==============================================================================
