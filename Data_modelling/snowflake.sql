-- ==============================================================================
-- SNOWFLAKE, SNOWSQL & CORTEX ENTERPRISE MASTER REPOSITORY (WEEK 6)
-- Target Location: c:\Users\Abhiram Chittampally\Documents\ACC\Data_modelling\snowflake.sql
-- Curriculum: KMIT Talent Accelerator Program (TAP) 2026 - Week 6 (Days 26-31)
-- Components: Cloud DW, 3-Layer Architecture, Micro-Partitions, Virtual Warehouses,
--             Table Types, Stages, COPY INTO, Snowpipe, Time Travel & Cloning,
--             Performance Tuning, RBAC & Data Masking, Semi-Structured (VARIANT/FLATTEN),
--             Streams (CDC), Tasks & DAGs, UDFs, Stored Procedures, SOS,
--             Python Connector, Snowpark ML, Cortex GenAI LLMs, Vector Search & RAG.
-- ==============================================================================

-- ==============================================================================
-- TABLE OF CONTENTS
-- ------------------------------------------------------------------------------
-- 1. DAY 26: SNOWFLAKE SETUP, SESSIONS & OBJECT HIERARCHY (B1 - B5)
--    1.1 Session Context Initialization & Verification
--    1.2 Database & Schema Hierarchy Setup
--    1.3 Multi-Cluster Virtual Warehouse Provisioning
--    1.4 SnowSQL Configuration Scripting & Non-Interactive Execution
-- 2. DAY 27: FOUNDATIONS, MICRO-PARTITIONS & DATA LOADING (5.1 - 5.5)
--    2.1 3-Layer Architecture Demonstration (Services, Compute, Storage)
--    2.2 Micro-Partitions, Pruning & Sargable vs Non-Sargable Predicates
--    2.3 Table Types: Permanent, Transient, Temporary, and External
--    2.4 Stages (User, Table, Internal Named, External S3 with Storage Integration)
--    2.5 File Formats & Production COPY INTO with Error Handling & Validation
-- 3. DAY 28: ADVANCED FEATURES & SEMI-STRUCTURED DATA (5.6 - 5.10)
--    3.1 Snowpipe: Continuous Serverless Ingestion & Health Monitoring
--    3.2 Time Travel, UNDROP, and Fail-Safe Governance
--    3.3 Zero-Copy Cloning: Tables, Schemas, Databases & Point-in-Time Clones
--    3.4 Performance Tuning: Clustering Keys, Query Profile, Materialized Views & Result Cache
--    3.5 Enterprise Security: Role-Based Access Control (RBAC), Masking Policies & Row Access Policies
--    3.6 Semi-Structured Data: VARIANT, LATERAL FLATTEN & Nested JSON Navigation
-- 4. DAY 29: REAL-WORLD PATTERNS & PIPELINES (5.11 - 5.15)
--    4.1 Search Optimization Service (SOS) for Point Lookups & Substring Search
--    4.2 Streams: Native Change Data Capture (CDC) & SCD Type 2 Pipelines
--    4.3 Tasks & Task DAGs: CRON, Serverless Compute, WHEN Clauses & Multi-Step Orchestration
--    4.4 User-Defined Functions (UDFs): SQL, JavaScript, Python & Vectorized UDTFs
--    4.5 Stored Procedures: Snowflake Scripting (Control Flow, Dynamic SQL, Logging)
--    4.6 Python Connector & Snowpark DataFrame Processing
-- 5. DAY 30: SNOWPARK ML, CORTEX GENAI & COST GOVERNANCE (5.16 - 5.18)
--    5.1 Snowpark ML: Pipelines, XGBoost Estimator & Model Registry Deployment
--    5.2 Cortex ML Functions: Automated Time-Series FORECAST & ANOMALY_DETECTION
--    5.3 Cortex LLM Functions: COMPLETE, SUMMARIZE, TRANSLATE, SENTIMENT, CLASSIFY_TEXT
--    5.4 Vector Search, EMBED_TEXT_768, Cosine Similarity & Complete In-Database RAG
--    5.5 Enterprise Cost Governance: Resource Monitors, Object Tagging & Metering Audits
-- 6. DAY 31: CAPSTONE - MANGO MART ENTERPRISE PLATFORM (20-Part Full Pipeline)
-- ==============================================================================


-- ==============================================================================
-- SECTION 1: DAY 26 - SNOWFLAKE SETUP, SESSIONS & OBJECT HIERARCHY (B1 - B5)
-- ==============================================================================

-- 1.1 SESSION CONTEXT INITIALIZATION & VERIFICATION (B5)
-- Production Rule: Never rely on implicit session defaults. Explicitly set Role,
-- Warehouse, Database, and Schema at the head of every production script.

USE ROLE SYSADMIN;                        -- System admin owns database and warehouse objects
USE WAREHOUSE COMPUTE_WH;                 -- Default starter warehouse

-- Verify current operational session state:
SELECT 
    CURRENT_ROLE() AS active_role,
    CURRENT_WAREHOUSE() AS active_warehouse,
    CURRENT_DATABASE() AS active_database,
    CURRENT_SCHEMA() AS active_schema,
    CURRENT_REGION() AS active_cloud_region,
    CURRENT_TIMESTAMP() AS session_start_time;


-- 1.2 DATABASE & SCHEMA OBJECT HIERARCHY (B5)
-- Create logical separation of data domains: RAW (Ingest), RETAIL (Dimensions),
-- ANALYTICS (Curated Facts/Marts), ML (Feature store & models), OPS (Logging/Audit).

CREATE DATABASE IF NOT EXISTS mango_mart
    COMMENT = 'Enterprise Retail Data Platform for Mango Mart';

-- Schemas within MANGO_MART
CREATE SCHEMA IF NOT EXISTS mango_mart.raw
    COMMENT = 'Raw landing zone for batch files and Snowpipe streaming payloads';

CREATE SCHEMA IF NOT EXISTS mango_mart.retail
    COMMENT = 'Operational data store and master dimension repository';

CREATE SCHEMA IF NOT EXISTS mango_mart.analytics
    COMMENT = 'Curated presentation layer: star schemas, marts, and materialized aggregates';

CREATE SCHEMA IF NOT EXISTS mango_mart.ml
    COMMENT = 'Machine learning features, registered models, and prediction logs';

CREATE SCHEMA IF NOT EXISTS mango_mart.kb
    COMMENT = 'Knowledge base document chunks and vector embeddings for Cortex RAG';

CREATE SCHEMA IF NOT EXISTS mango_mart.ops
    COMMENT = 'Operational metadata: task history, load history, audit logs, and monitoring';

-- Set session context to the newly created environment
USE DATABASE mango_mart;
USE SCHEMA retail;


-- 1.3 MULTI-CLUSTER VIRTUAL WAREHOUSE PROVISIONING (B2, 5.2)
-- Provision dedicated compute clusters per workload to guarantee performance isolation.

-- A. Nightly ETL Warehouse: Sized LARGE (8 nodes) for high-throughput batch loading;
-- auto-suspends aggressively after 60 seconds of idle time.
CREATE OR REPLACE WAREHOUSE etl_wh
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 60                     -- Suspends 1 minute after last query completes
    AUTO_RESUME = TRUE                    -- Wakes up instantly when query arrives
    INITIALLY_SUSPENDED = TRUE            -- Does not incur cost until first query runs
    COMMENT = 'Dedicated compute for heavy batch ETL and data transformation';

-- B. Business Intelligence (BI) Warehouse: Sized MEDIUM with Multi-Cluster Auto-Scaling;
-- Scales OUT from 1 to 4 clusters to absorb concurrency spikes (e.g., 9 AM dashboard traffic).
CREATE OR REPLACE WAREHOUSE bi_wh
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300                    -- Keeps local SSD cache warm for 5 minutes
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1                 -- Baseline minimum 1 cluster
    MAX_CLUSTER_COUNT = 4                 -- Bursts up to 4 clusters when queries queue
    SCALING_POLICY = 'STANDARD'           -- Adds clusters immediately on query queueing
    COMMENT = 'High-concurrency virtual warehouse for BI dashboards and analyst queries';

-- C. Machine Learning & Cortex Warehouse: Sized LARGE for model training and embeddings.
CREATE OR REPLACE WAREHOUSE ml_wh
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Compute warehouse for Snowpark ML model training and Cortex GenAI jobs';


-- 1.4 SNOWSQL CONFIGURATION SCRIPTING (B4)
-- SnowSQL command-line configuration pattern (typically in ~/.snowsql/config):
/*
[connections.mango_prod]
accountname = ab12345.ap-south-1.aws
username = DATA_ENGINEER_SVC
authenticator = SNOWFLAKE_JWT
private_key_path = ~/.snowsql/rsa_key.p8
dbname = MANGO_MART
schemaname = RETAIL
warehousename = ETL_WH
rolename = SYSADMIN

# Non-interactive terminal execution from shell script or CI/CD runner:
# snowsql -c mango_prod -f /opt/pipelines/nightly_etl.sql -D LOAD_DATE=2026-10-14 -o output_format=csv
*/


-- ==============================================================================
-- SECTION 2: DAY 27 - FOUNDATIONS, MICRO-PARTITIONS & DATA LOADING (5.1 - 5.5)
-- ==============================================================================

-- 2.1 3-LAYER ARCHITECTURE DEMONSTRATION (5.1)
-- Query 1: Cloud Services Layer only (Zero warehouse compute cost, answers from metadata)
SHOW TABLES IN SCHEMA mango_mart.retail;
DESCRIBE WAREHOUSE etl_wh;

-- Query 2: Query Processing & Storage Layer (Spins up warehouse compute to scan micro-partitions)
-- SELECT COUNT(*) FROM mango_mart.analytics.fact_sales_transaction;


-- 2.2 MICRO-PARTITIONS, PRUNING & SARGABILITY (5.1, 5.8)
-- Sargable vs Non-Sargable WHERE clauses:

-- Anti-Pattern (Non-Sargable): Wrapping the filtered column in a scalar function.
-- Snowflake's optimizer CANNOT prune micro-partitions because it cannot evaluate the
-- function against the partition's MIN/MAX metadata. Triggers a full table scan!
/*
SELECT COUNT(*) 
FROM mango_mart.analytics.fact_sales_transaction
WHERE TO_VARCHAR(date_key) LIKE '202610%'; -- BAD: Scans all 4,000 partitions!
*/

-- Best Practice (Sargable): Keep the column bare with direct comparison operators.
-- Pruning skips 99% of micro-partitions directly via Cloud Services metadata!
/*
SELECT COUNT(*) 
FROM mango_mart.analytics.fact_sales_transaction
WHERE date_key >= 20261001 AND date_key <= 20261031; -- GOOD: Scans only matching partitions!
*/


-- 2.3 TABLE TYPES: PERMANENT, TRANSIENT, TEMPORARY, EXTERNAL (5.3)

-- A. TRANSIENT Table: Has 0 or 1 day Time Travel, NO Fail-Safe.
-- Perfect for ETL staging to eliminate 7-day Fail-Safe storage costs on recreatable data.
CREATE OR REPLACE TRANSIENT TABLE mango_mart.raw.stg_pos_transactions (
    txn_id VARCHAR(50),
    sale_timestamp TIMESTAMP_NTZ,
    store_code VARCHAR(20),
    product_code VARCHAR(50),
    quantity INT,
    unit_price NUMBER(12, 2),
    net_revenue NUMBER(12, 2)
) DATA_RETENTION_TIME_IN_DAYS = 0;        -- Zero Time Travel storage overhead

-- B. TEMPORARY Table: Scoped strictly to current session; automatically dropped on disconnect.
CREATE OR REPLACE TEMPORARY TABLE mango_mart.retail.tmp_active_customers AS
SELECT DISTINCT customer_id 
FROM mango_mart.raw.stg_pos_transactions
WHERE net_revenue > 1000;

-- C. PERMANENT Table: Default enterprise table with up to 90 days Time Travel + 7 days Fail-Safe.
CREATE OR REPLACE TABLE mango_mart.analytics.fact_sales_transaction (
    date_key INT NOT NULL,
    store_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    transaction_number VARCHAR(50) NOT NULL,
    quantity_sold INT NOT NULL,
    unit_price NUMBER(12, 2) NOT NULL,
    net_revenue NUMBER(12, 2) NOT NULL,
    load_date DATE DEFAULT CURRENT_DATE(),
    correction_flag TINYINT DEFAULT 0
) DATA_RETENTION_TIME_IN_DAYS = 30;       -- 30 days of continuous Time Travel


-- 2.4 STAGES & FILE FORMATS (5.4)

-- Internal Named Stage (Managed storage within Snowflake)
CREATE OR REPLACE STAGE mango_mart.raw.internal_load_stage
    FILE_FORMAT = (TYPE = CSV COMPRESSION = AUTO)
    COMMENT = 'Internal landing stage for on-prem files uploaded via SnowSQL PUT';

-- File Format Specification for CSV POS Extracts
CREATE OR REPLACE FILE FORMAT mango_mart.raw.ff_pos_csv
    TYPE = CSV
    FIELD_DELIMITER = '|'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null', '\\N')
    DATE_FORMAT = 'YYYY-MM-DD'
    TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS'
    ENCODING = 'UTF8'
    COMPRESSION = AUTO;

-- File Format for Parquet Extracts
CREATE OR REPLACE FILE FORMAT mango_mart.raw.ff_parquet
    TYPE = PARQUET
    COMPRESSION = SNAPPY;


-- 2.5 COPY INTO WITH ERROR HANDLING & VALIDATION MODES (5.5)

-- A. Dry-Run Validation: Test parsing without loading rows (Returns all errors)
COPY INTO mango_mart.raw.stg_pos_transactions
FROM @mango_mart.raw.internal_load_stage/2026/10/
FILE_FORMAT = (FORMAT_NAME = mango_mart.raw.ff_pos_csv)
PATTERN = '.*pos_202610.*\\.csv\\.gz'
VALIDATION_MODE = 'RETURN_ERRORS';

-- B. Production Bulk Load: Skip file only if error rate exceeds 10%
COPY INTO mango_mart.raw.stg_pos_transactions
FROM @mango_mart.raw.internal_load_stage/2026/10/
FILE_FORMAT = (FORMAT_NAME = mango_mart.raw.ff_pos_csv)
PATTERN = '.*pos_202610.*\\.csv\\.gz'
ON_ERROR = 'SKIP_FILE_10%'               -- Tolerate small anomalies; abort if file is corrupted
PURGE = FALSE;                           -- Retain staged files for audit verification

-- C. Inspect Load History for Auditing (Last 24 Hours)
SELECT 
    file_name,
    status,
    row_count,
    row_parsed,
    error_count,
    first_error_message,
    last_load_time
FROM TABLE(INFORMATION_SCHEMA.LOAD_HISTORY(
    TABLE_NAME => 'STG_POS_TRANSACTIONS',
    START_TIME => DATEADD('HOUR', -24, CURRENT_TIMESTAMP())
))
ORDER BY last_load_time DESC;


-- ==============================================================================
-- SECTION 3: DAY 28 - ADVANCED FEATURES & SEMI-STRUCTURED DATA (5.6 - 5.10)
-- ==============================================================================

-- 3.1 SNOWPIPE: SERVERLESS CONTINUOUS INGESTION (5.6)
-- Creates an event-driven auto-ingest pipe that listens to cloud queue notifications (AWS SQS).

-- Landing table for streaming JSON orders
CREATE OR REPLACE TABLE mango_mart.raw.raw_orders_stream (
    raw_event VARIANT,
    loaded_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    source_file VARCHAR(500),
    file_row_number INT
);

-- File format for single-line streaming JSON
CREATE OR REPLACE FILE FORMAT mango_mart.raw.ff_json
    TYPE = JSON
    STRIP_OUTER_ARRAY = FALSE;

-- The Pipe Object: Wraps COPY INTO, runs on Snowflake-managed serverless compute
CREATE OR REPLACE PIPE mango_mart.raw.pipe_orders
    AUTO_INGEST = TRUE                    -- Subscribes to SQS/EventGrid message queue
    COMMENT = 'Continuous Snowpipe ingestion for online e-commerce transactions'
AS
COPY INTO mango_mart.raw.raw_orders_stream (raw_event, source_file, file_row_number)
FROM (
    SELECT 
        $1,
        METADATA$FILENAME,
        METADATA$FILE_ROW_NUMBER
    FROM @mango_mart.raw.internal_load_stage/orders/
)
FILE_FORMAT = (FORMAT_NAME = mango_mart.raw.ff_json)
ON_ERROR = 'SKIP_FILE_5%';

-- Check Snowpipe Status & Notification Channel ARN:
SELECT SYSTEM$PIPE_STATUS('mango_mart.raw.pipe_orders');


-- 3.2 TIME TRAVEL & UNDROP (5.7)
-- Recover from accidental changes or drops without needing external backups.

-- 1. Point-in-time query: State of table 10 minutes ago
SELECT COUNT(*) 
FROM mango_mart.raw.stg_pos_transactions 
AT (OFFSET => -600);

-- 2. Point-in-time query: State immediately BEFORE a specific bad query executed
/*
SELECT * 
FROM mango_mart.retail.dim_customer 
BEFORE (STATEMENT => '01b7a2d4-0000-1234-0000-56780000abcd');
*/

-- 3. Accidental Drop Recovery:
DROP TABLE mango_mart.raw.stg_pos_transactions; -- Oops!
UNDROP TABLE mango_mart.raw.stg_pos_transactions; -- Restored in 1 second!


-- 3.3 ZERO-COPY CLONING (5.7)
-- Instant metadata copy; takes seconds, costs zero storage at creation.

-- Clone an entire database for QA / feature development:
CREATE OR REPLACE DATABASE mango_mart_dev 
CLONE mango_mart;

-- Point-in-time clone: Clone database exactly as it existed at midnight:
CREATE OR REPLACE DATABASE mango_mart_audit_snapshot 
CLONE mango_mart 
AT (TIMESTAMP => DATE_TRUNC('DAY', CURRENT_TIMESTAMP()));


-- 3.4 PERFORMANCE TUNING: CLUSTERING KEYS & MATERIALIZED VIEWS (5.8)

-- Explicit Clustering Key: Re-order micro-partitions on heavily filtered columns
ALTER TABLE mango_mart.analytics.fact_sales_transaction
CLUSTER BY (store_key, date_key);

-- Monitor Clustering Depth (Values near 1.0 indicate perfect clustering):
SELECT SYSTEM$CLUSTERING_INFORMATION(
    'mango_mart.analytics.fact_sales_transaction', 
    '(store_key, date_key)'
);

-- Materialized View: Pre-computed daily summary refreshed incrementally
CREATE OR REPLACE MATERIALIZED VIEW mango_mart.analytics.mv_daily_store_sales AS
SELECT 
    date_key,
    store_key,
    COUNT(*) AS total_transactions,
    SUM(quantity_sold) AS total_units_sold,
    SUM(net_revenue) AS daily_revenue
FROM mango_mart.analytics.fact_sales_transaction
GROUP BY date_key, store_key;


-- 3.5 RBAC, DYNAMIC DATA MASKING & ROW ACCESS POLICIES (5.9)

-- Layered RBAC Setup
USE ROLE SECURITYADMIN;
CREATE ROLE IF NOT EXISTS mango_analyst;
CREATE ROLE IF NOT EXISTS mango_engineer;

-- Column Masking Policy: Redact email for analysts, show cleartext to engineers
CREATE OR REPLACE MASKING POLICY mango_mart.retail.mask_email AS (val STRING) 
RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() = 'MANGO_ENGINEER' THEN val
        WHEN CURRENT_ROLE() = 'MANGO_ANALYST' THEN REGEXP_REPLACE(val, '(.)(.*)(@.*)', '\\1***\\3')
        ELSE '***REDACTED***'
    END;

-- Apply Masking Policy to Dimension Table
ALTER TABLE mango_mart.retail.dim_customer 
MODIFY COLUMN email SET MASKING POLICY mango_mart.retail.mask_email;

-- Row Access Policy: Limit regional analysts to their own geographic territory
CREATE OR REPLACE ROW ACCESS POLICY mango_mart.retail.rap_store_region AS (region_code STRING) 
RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() IN ('SYSADMIN', 'MANGO_ENGINEER') THEN TRUE
        WHEN CURRENT_ROLE() = 'ANALYST_SOUTH' THEN region_code = 'SOUTH'
        WHEN CURRENT_ROLE() = 'ANALYST_NORTH' THEN region_code = 'NORTH'
        ELSE FALSE
    END;


-- 3.6 SEMI-STRUCTURED DATA: VARIANT & LATERAL FLATTEN (5.10)
-- Scenario: Raw JSON order contains an array of line items with nested discounts.

-- Query VARIANT paths using colon-dot notation and unnest nested arrays:
SELECT 
    o.raw_event:order_id::STRING AS order_id,
    o.raw_event:customer.name::STRING AS customer_name,
    item.value:sku::STRING AS item_sku,
    item.value:qty::INT AS item_qty,
    item.value:price::NUMBER(10, 2) AS item_price,
    disc.value:code::STRING AS discount_code,
    disc.value:amount::NUMBER(10, 2) AS discount_amount
FROM mango_mart.raw.raw_orders_stream o,
LATERAL FLATTEN(input => o.raw_event:items) item,             -- 1st unnest: items array
LATERAL FLATTEN(input => item.value:discounts, OUTER => TRUE) disc; -- 2nd unnest: discounts array


-- ==============================================================================
-- SECTION 4: DAY 29 - REAL-WORLD PATTERNS & PIPELINES (5.11 - 5.15)
-- ==============================================================================

-- 4.1 SEARCH OPTIMIZATION SERVICE (SOS) (5.11)
-- Build secondary search access paths on large fact tables for instant point lookups.
ALTER TABLE mango_mart.analytics.fact_sales_transaction
ADD SEARCH OPTIMIZATION 
    ON EQUALITY(transaction_number, customer_key);


-- 4.2 STREAMS: CHANGE DATA CAPTURE (CDC) (5.12)
-- Create an APPEND_ONLY stream on the Snowpipe landing table to track newly landed events.
CREATE OR REPLACE STREAM mango_mart.raw.strm_orders_cdc
ON TABLE mango_mart.raw.raw_orders_stream
APPEND_ONLY = TRUE;


-- 4.3 USER-DEFINED FUNCTIONS (UDFS) (5.14)

-- A. SQL Scalar UDF (Inline-optimized by planner with zero runtime penalty)
CREATE OR REPLACE FUNCTION mango_mart.retail.fn_calculate_gst(net_amount NUMBER)
RETURNS NUMBER(12, 2)
LANGUAGE SQL
AS $$ net_amount * 0.18 $$;

-- B. Python Scalar UDF (Runs inside secure sandbox with NumPy)
CREATE OR REPLACE FUNCTION mango_mart.ml.fn_predict_churn_heuristic(
    days_since_order INT, order_count INT, avg_basket NUMBER
)
RETURNS NUMBER(5, 4)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('numpy')
HANDLER = 'calculate_churn'
AS $$
import numpy as np
def calculate_churn(days_since_order, order_count, avg_basket):
    if days_since_order is None or order_count is None:
        return 0.5000
    # Sigmoidal churn probability heuristic
    score = 1.0 / (1.0 + np.exp(-(days_since_order / 30.0 - order_count * 0.2)))
    return float(np.clip(score, 0.0, 1.0))
$$;


-- 4.4 STORED PROCEDURES & PROCEDURAL ETL (5.14)
-- Multi-statement Snowflake Scripting procedure with transaction handling and logging.

CREATE OR REPLACE PROCEDURE mango_mart.ops.sp_process_order_stream()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER                          -- Runs with owner privileges for safe delegation
AS
$$
DECLARE
    v_rows_inserted INT := 0;
    v_started_at TIMESTAMP_LTZ := CURRENT_TIMESTAMP();
BEGIN
    -- Only execute if stream has unconsumed data
    IF (SYSTEM$STREAM_HAS_DATA('mango_mart.raw.strm_orders_cdc')) THEN
        
        -- Insert new stream records into analytics fact table
        INSERT INTO mango_mart.analytics.fact_sales_transaction (
            date_key, store_key, product_key, customer_key, transaction_number,
            quantity_sold, unit_price, net_revenue, load_date, correction_flag
        )
        SELECT 
            TO_NUMBER(TO_VARCHAR(o.raw_event:sale_date::DATE, 'YYYYMMDD')),
            o.raw_event:store_key::INT,
            o.raw_event:product_key::INT,
            COALESCE(o.raw_event:customer_key::INT, -1),
            o.raw_event:order_id::STRING,
            o.raw_event:quantity::INT,
            o.raw_event:unit_price::NUMBER(12, 2),
            o.raw_event:net_revenue::NUMBER(12, 2),
            CURRENT_DATE(),
            0
        FROM mango_mart.raw.strm_orders_cdc o
        WHERE o.METADATA$ACTION = 'INSERT';

        v_rows_inserted := SQLROWCOUNT;

        -- Record audit log
        INSERT INTO mango_mart.ops.etl_audit_log (pipeline_name, rows_affected, execution_status, completed_at)
        VALUES ('sp_process_order_stream', :v_rows_inserted, 'SUCCESS', CURRENT_TIMESTAMP());

        RETURN 'SUCCESS: Processed ' || :v_rows_inserted || ' records.';
    ELSE
        RETURN 'SKIPPED: Stream has no new data.';
    END IF;
EXCEPTION
    WHEN OTHER THEN
        INSERT INTO mango_mart.ops.etl_audit_log (pipeline_name, rows_affected, execution_status, error_message, completed_at)
        VALUES ('sp_process_order_stream', 0, 'FAILED', SQLERRM, CURRENT_TIMESTAMP());
        RAISE;
END;
$$;


-- 4.5 TASKS & TASK DAG ORCHESTRATION (5.13)
-- Automated scheduling without external orchestrators (Airflow).

-- Root Task: Scheduled via CRON, checks if stream has data before activating warehouse
CREATE OR REPLACE TASK mango_mart.ops.task_process_stream_root
    WAREHOUSE = etl_wh
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('mango_mart.raw.strm_orders_cdc') -- Skip execution if empty!
AS
    CALL mango_mart.ops.sp_process_order_stream();

-- Child Task (DAG Fan-Out): Refreshes downstream views after root completes
CREATE OR REPLACE TASK mango_mart.ops.task_refresh_analytics_child
    WAREHOUSE = etl_wh
    AFTER mango_mart.ops.task_process_stream_root       -- Dependency chain
AS
    INSERT INTO mango_mart.ops.etl_audit_log (pipeline_name, rows_affected, execution_status, completed_at)
    VALUES ('task_refresh_analytics_child', 1, 'COMPLETED', CURRENT_TIMESTAMP());

-- Activate the Task DAG (Enable children first, then root)
ALTER TASK mango_mart.ops.task_refresh_analytics_child RESUME;
ALTER TASK mango_mart.ops.task_process_stream_root RESUME;


-- ==============================================================================
-- SECTION 5: DAY 30 - SNOWPARK ML, CORTEX GENAI & COST GOVERNANCE (5.16 - 5.18)
-- ==============================================================================

-- 5.1 CORTEX ML FUNCTIONS: AUTOMATED FORECASTING & ANOMALY DETECTION (5.16)

-- Train a Snowflake Cortex Time-Series Forecasting Model on 2 years of sales:
CREATE OR REPLACE SNOWFLAKE.ML.FORECAST mango_mart.ml.sales_forecast_model (
    INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'mango_mart.analytics.mv_daily_store_sales'),
    TIMESTAMP_COLNAME => 'DATE_KEY',
    TARGET_COLNAME => 'DAILY_REVENUE'
);

-- Generate 30-Day Forward Revenue Forecast:
CALL mango_mart.ml.sales_forecast_model!FORECAST(FORECASTING_PERIODS => 30);


-- 5.2 CORTEX LLM FUNCTIONS (5.17a)
-- Calling Foundation LLMs directly from SQL with zero data egress!

-- Create Support Tickets Table
CREATE OR REPLACE TABLE mango_mart.raw.support_tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    ticket_text VARCHAR(4000),
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Automated AI Triage: Sentiment, Category Classification, and Summary in one query!
SELECT 
    ticket_id,
    -- 1. Sentiment Score (-1.0 negative to +1.0 positive)
    SNOWFLAKE.CORTEX.SENTIMENT(ticket_text) AS sentiment_score,
    -- 2. Multi-Class Topic Classification
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        ticket_text, 
        ['Delivery Delay', 'Damaged Item', 'Billing Error', 'Product Inquiry']
    ):label::STRING AS ticket_category,
    -- 3. Executive Summarization
    SNOWFLAKE.CORTEX.SUMMARIZE(ticket_text) AS ticket_summary,
    -- 4. LLM Drafting via Llama 3.1 70B
    SNOWFLAKE.CORTEX.COMPLETE(
        'llama3.1-70b',
        'Draft a warm, professional 2-sentence response addressing this issue: ' || ticket_text
    ) AS ai_draft_reply
FROM mango_mart.raw.support_tickets;


-- 5.3 CORTEX VECTOR SEARCH, EMBEDDINGS & IN-DATABASE RAG (5.17b)

-- Table storing policy documents with 768-dimensional embeddings
CREATE OR REPLACE TABLE mango_mart.kb.policy_chunks (
    chunk_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_title VARCHAR(200),
    chunk_text VARCHAR(4000),
    embedding VECTOR(FLOAT, 768)          -- Native vector data type
);

-- Populate table and compute embeddings via Cortex e5-base-v2 model:
INSERT INTO mango_mart.kb.policy_chunks (document_title, chunk_text, embedding)
VALUES (
    'Return Policy',
    'Customers can return fresh produce within 24 hours of delivery for a full refund without questions.',
    SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', 'Customers can return fresh produce within 24 hours of delivery for a full refund without questions.')
);

-- IN-DATABASE RETRIEVAL-AUGMENTED GENERATION (RAG) QUERY:
-- 1. Embed user query -> 2. Vector Cosine Similarity Search -> 3. Pass Context to LLM
WITH retrieved_context AS (
    SELECT 
        chunk_text,
        VECTOR_COSINE_SIMILARITY(
            embedding, 
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', 'Can I return spoiled mangoes after delivery?')
        ) AS similarity_score
    FROM mango_mart.kb.policy_chunks
    ORDER BY similarity_score DESC
    LIMIT 3
),
context_aggregate AS (
    SELECT LISTAGG(chunk_text, '\n---\n') WITHIN GROUP (ORDER BY similarity_score DESC) AS full_context
    FROM retrieved_context
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-70b',
    [
        {'role': 'system', 'content': 'You are Mango Mart AI Support. Answer the question using ONLY the provided policy context. If unknown, say so.'},
        {'role': 'user', 'content': 'Context:\n' || (SELECT full_context FROM context_aggregate) || '\n\nQuestion: Can I return spoiled mangoes after delivery?'}
    ]::VARIANT
) AS grounded_rag_response;


-- 5.4 RESOURCE MONITORS & COST GOVERNANCE (5.18)
-- Strict credit guardrails to protect against runaway queries or loops.

CREATE OR REPLACE RESOURCE MONITOR rm_monthly_guardrail
    WITH CREDIT_QUOTA = 1000              -- Cap monthly consumption at 1,000 credits
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY           -- Warning email at 750 credits
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND         -- Prevents NEW queries from starting
        ON 110 PERCENT DO SUSPEND_IMMEDIATE; -- Kills all in-flight queries immediately!

-- Attach guardrail monitor to the ETL warehouse:
ALTER WAREHOUSE etl_wh SET RESOURCE_MONITOR = rm_monthly_guardrail;


-- ==============================================================================
-- SECTION 6: DAY 31 - CAPSTONE PLATFORM VERIFICATION (20-PART PIPELINE)
-- ==============================================================================

-- Verify complete pipeline health and metadata metrics:
SELECT 
    'Fact Sales Rows' AS metric, COUNT(*) AS count_value FROM mango_mart.analytics.fact_sales_transaction
UNION ALL
SELECT 
    'Active Customers', COUNT(*) FROM mango_mart.retail.dim_customer WHERE is_current = TRUE
UNION ALL
SELECT 
    'Policy Knowledge Chunks', COUNT(*) FROM mango_mart.kb.policy_chunks;

-- ==============================================================================
-- END OF SCRIPT: SNOWFLAKE + SNOWSQL + CORTEX MASTER IMPLEMENTATION
-- ==============================================================================
