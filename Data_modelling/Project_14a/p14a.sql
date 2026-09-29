-- Task 1: Create database and schema

CREATE DATABASE IF NOT EXISTS RETAIL14A_DW;

CREATE SCHEMA IF NOT EXISTS RETAIL14A_DW.SCHEMA_14A;

USE DATABASE RETAIL14A_DW;

USE SCHEMA SCHEMA_14A;


-- Create file format

CREATE OR REPLACE FILE FORMAT RETAIL14A_JSON_FORMAT
TYPE = 'JSON'
STRIP_OUTER_ARRAY = FALSE;


-- Create raw text file format

CREATE OR REPLACE FILE FORMAT RETAIL14A_TEXT_FORMAT
TYPE = 'CSV'
FIELD_DELIMITER = NONE
RECORD_DELIMITER = '\n'
SKIP_HEADER = 0;


-- Create stage

CREATE OR REPLACE STAGE RETAIL14A_STAGE
FILE_FORMAT = RETAIL14A_TEXT_FORMAT;


-- Task 1: Create raw landing table

CREATE OR REPLACE TABLE RETAIL14A_RAW_LINES (
    RAW_RECORD_TEXT VARCHAR
);


-- Load all JSON lines from the input files

COPY INTO RETAIL14A_RAW_LINES
FROM @RETAIL14A_STAGE
FILE_FORMAT = RETAIL14A_TEXT_FORMAT
ON_ERROR = 'CONTINUE';


-- Task 1: Create Data Lake table

CREATE OR REPLACE TABLE LAKE_RAW_EVENTS (
    RAW_EVENT VARIANT
);


-- Load only valid JSON records into the Data Lake

INSERT INTO LAKE_RAW_EVENTS (RAW_EVENT)
SELECT TRY_PARSE_JSON(RAW_RECORD_TEXT)
FROM RETAIL14A_RAW_LINES
WHERE TRY_PARSE_JSON(RAW_RECORD_TEXT) IS NOT NULL;


-- Task 1: Validate Data Lake records

SELECT COUNT(*) AS TOTAL_RAW_RECORD_CT
FROM LAKE_RAW_EVENTS;


-- Task 2: Extract semi-structured JSON attributes

SELECT
    RAW_EVENT:event_id::VARCHAR AS EVENT_ID,
    TO_TIMESTAMP_NTZ(RAW_EVENT:timestamp::VARCHAR) AS EVENT_TIME,
    RAW_EVENT:user_id::INTEGER AS USER_ID,
    RAW_EVENT:action::VARCHAR AS ACTION,
    RAW_EVENT:order:total::NUMBER(12,2) AS ORDER_TOTAL,
    RAW_EVENT:promo_code::VARCHAR AS PROMO_CODE
FROM LAKE_RAW_EVENTS
ORDER BY EVENT_ID;


-- Task 3: Calculate Schema-on-Read financial metrics

SELECT
    RAW_EVENT:event_id::VARCHAR AS EVENT_ID,
    RAW_EVENT:order:total::NUMBER(12,2) AS ORDER_TOTAL,
    RAW_EVENT:order:shipping_cost::NUMBER(12,2) AS SHIPPING_COST,
    RAW_EVENT:order:tax::NUMBER(12,2) AS TAX,
    COALESCE(RAW_EVENT:discount_amount::NUMBER(12,2), 0) AS DISCOUNT_AMOUNT,
    (
        RAW_EVENT:order:total::NUMBER(12,2)
        - RAW_EVENT:order:shipping_cost::NUMBER(12,2)
        - RAW_EVENT:order:tax::NUMBER(12,2)
        - COALESCE(RAW_EVENT:discount_amount::NUMBER(12,2), 0)
    ) AS NET_REVENUE
FROM LAKE_RAW_EVENTS
WHERE RAW_EVENT:order:total::NUMBER(12,2) > 0
ORDER BY EVENT_ID;


-- Task 4: Calculate funnel and conversion metrics

SELECT
    COUNT(*) AS TOTAL_EVENTS,
    COUNT_IF(
        RAW_EVENT:action::VARCHAR = 'purchase'
    ) AS TOTAL_PURCHASES,
    ROUND(
        COUNT_IF(
            RAW_EVENT:action::VARCHAR = 'purchase'
        ) * 100.0 / COUNT(*),
        2
    ) AS CONVERSION_RATE_PCT,
    SUM(
        COALESCE(
            RAW_EVENT:order:total::NUMBER(12,2),
            0
        )
    ) AS TOTAL_GROSS_REVENUE,
    ROUND(
        SUM(
            CASE
                WHEN RAW_EVENT:action::VARCHAR = 'purchase'
                 AND RAW_EVENT:order:total::NUMBER(12,2) > 0
                THEN RAW_EVENT:order:total::NUMBER(12,2)
                ELSE 0
            END
        )
        /
        NULLIF(
            COUNT_IF(
                RAW_EVENT:action::VARCHAR = 'purchase'
                AND RAW_EVENT:order:total::NUMBER(12,2) > 0
            ),
            0
        ),
        2
    ) AS AVERAGE_ORDER_VALUE
FROM LAKE_RAW_EVENTS;


-- Task 5: Create structured Data Warehouse table

CREATE OR REPLACE TABLE DW_STRUCTURED_EVENTS (
    EVENT_ID VARCHAR(50),
    EVENT_TIME TIMESTAMP_NTZ,
    USER_ID NUMBER,
    PAGE VARCHAR(100),
    ACTION VARCHAR(50),
    ORDER_TOTAL NUMBER(12,2),
    SHIPPING_COST NUMBER(12,2),
    TAX NUMBER(12,2),
    ITEMS NUMBER,
    PROMO_CODE VARCHAR(50),
    DISCOUNT_AMOUNT NUMBER(12,2),
    NET_REVENUE NUMBER(12,2)
);


-- Task 5: Backfill structured warehouse table

INSERT INTO DW_STRUCTURED_EVENTS (
    EVENT_ID,
    EVENT_TIME,
    USER_ID,
    PAGE,
    ACTION,
    ORDER_TOTAL,
    SHIPPING_COST,
    TAX,
    ITEMS,
    PROMO_CODE,
    DISCOUNT_AMOUNT,
    NET_REVENUE
)
SELECT
    RAW_EVENT:event_id::VARCHAR,
    TO_TIMESTAMP_NTZ(RAW_EVENT:timestamp::VARCHAR),
    RAW_EVENT:user_id::NUMBER,
    RAW_EVENT:page::VARCHAR,
    RAW_EVENT:action::VARCHAR,
    RAW_EVENT:order:total::NUMBER(12,2),
    RAW_EVENT:order:shipping_cost::NUMBER(12,2),
    RAW_EVENT:order:tax::NUMBER(12,2),
    RAW_EVENT:order:items::NUMBER,
    RAW_EVENT:promo_code::VARCHAR,
    COALESCE(
        RAW_EVENT:discount_amount::NUMBER(12,2),
        0
    ),
    CASE
        WHEN RAW_EVENT:order:total::NUMBER(12,2) IS NOT NULL
        THEN
            RAW_EVENT:order:total::NUMBER(12,2)
            - COALESCE(
                RAW_EVENT:order:shipping_cost::NUMBER(12,2),
                0
            )
            - COALESCE(
                RAW_EVENT:order:tax::NUMBER(12,2),
                0
            )
            - COALESCE(
                RAW_EVENT:discount_amount::NUMBER(12,2),
                0
            )
        ELSE 0
    END
FROM LAKE_RAW_EVENTS;


-- Task 5: Validate structured warehouse records

SELECT
    COUNT(*) AS STORED_RECORDS_QTY,
    SUM(NET_REVENUE) AS TOTAL_NET_REVENUE
FROM DW_STRUCTURED_EVENTS;


-- Task 6: Create quarantine table

CREATE OR REPLACE TABLE QUARANTINE_RAW_EVENTS (
    QUARANTINE_ID NUMBER AUTOINCREMENT,
    RAW_RECORD_TEXT VARCHAR,
    REASON VARCHAR(100)
);


-- Task 6: Move malformed records to quarantine

INSERT INTO QUARANTINE_RAW_EVENTS (
    RAW_RECORD_TEXT,
    REASON
)
SELECT
    RAW_RECORD_TEXT,
    'MALFORMED_JSON_BODY'
FROM RETAIL14A_RAW_LINES
WHERE TRY_PARSE_JSON(RAW_RECORD_TEXT) IS NULL;


-- Task 6: Display quarantined records

SELECT
    QUARANTINE_ID,
    RAW_RECORD_TEXT,
    REASON
FROM QUARANTINE_RAW_EVENTS
ORDER BY QUARANTINE_ID;