/*=========================================================
        SQL 3.10 MASTER BOILERPLATE
        Views & Materialized Views
=========================================================*/

-----------------------------------------------------------
-- SIMPLE VIEW
-----------------------------------------------------------

CREATE OR REPLACE VIEW active_customers AS
SELECT
    customer_id,
    name,
    city,
    tier
FROM customers
WHERE is_active = TRUE;

-----------------------------------------------------------
-- QUERY VIEW
-----------------------------------------------------------

SELECT *
FROM active_customers;

-----------------------------------------------------------
-- UPDATE THROUGH AN UPDATABLE VIEW
-----------------------------------------------------------

UPDATE active_customers
SET city = 'Mumbai'
WHERE customer_id = 101;

-----------------------------------------------------------
-- INSERT THROUGH VIEW
-----------------------------------------------------------

INSERT INTO active_customers
(
    customer_id,
    name,
    city,
    tier,
    is_active
)
VALUES
(
    201,
    'Rahul',
    'Hyderabad',
    'Gold',
    TRUE
);

-----------------------------------------------------------
-- VIEW WITH CHECK OPTION
-----------------------------------------------------------

CREATE OR REPLACE VIEW active_customers_secure AS
SELECT
    customer_id,
    name,
    city,
    tier,
    is_active
FROM customers
WHERE is_active = TRUE
WITH CHECK OPTION;

-----------------------------------------------------------
-- COMPLEX READ-ONLY VIEW
-----------------------------------------------------------

CREATE VIEW customer_order_summary AS
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spend
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name;

-----------------------------------------------------------
-- MATERIALIZED VIEW
-----------------------------------------------------------

CREATE MATERIALIZED VIEW sales_summary AS
SELECT
    customer_id,
    SUM(total_amount) AS total_sales,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;

-----------------------------------------------------------
-- QUERY MATERIALIZED VIEW
-----------------------------------------------------------

SELECT *
FROM sales_summary
WHERE total_sales > 10000
ORDER BY total_sales DESC;

-----------------------------------------------------------
-- REFRESH MATERIALIZED VIEW
-----------------------------------------------------------

REFRESH MATERIALIZED VIEW sales_summary;

-----------------------------------------------------------
-- MODIFY VIEW DEFINITION
-----------------------------------------------------------

CREATE OR REPLACE VIEW employee_public AS
SELECT
    employee_id,
    employee_name,
    department
FROM employees;

-----------------------------------------------------------
-- REMOVE OBJECTS
-----------------------------------------------------------

DROP VIEW employee_public;

DROP MATERIALIZED VIEW sales_summary;