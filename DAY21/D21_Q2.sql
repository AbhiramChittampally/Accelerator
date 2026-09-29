/*
Problem 12: Materialized View Rebuild Engine 
Scenario: The analytics team frequently queries total order spending
grouped by customer. Because running complex multi-table joins and
aggregation functions directly on live transaction tables degrades 
production performance, engineering wants to read from a dedicated
physical summary table that acts like a materialized view.
This summary table must be completely refreshed safely on demand.

The Task: Create a physical summary table named mv_revenue_by_customer.
Then, design a stored procedure named sp_refresh_customer_revenue_mv 
that handles the refresh operation within a single transaction block.
The procedure must clear out historical calculations and recalculate 
every customer's full name, total order count, and total spent amount
using a LEFT JOIN. If an error occurs during processing, 
the operation must immediately rollback.

Expected output=
-----------------
+-------------+---------------+--------------+---------------+
| customer_id | customer_name | total_orders | total_revenue |
+-------------+---------------+--------------+---------------+
|           1 | Amit Sharma   |            3 |       1150.00 |
|           2 | Priya Singh   |            3 |        970.00 |
|           3 | Rahul Verma   |            2 |        460.00 |
|           4 | Neha Patel    |            2 |        390.00 |
|           5 | Arjun Gupta   |            2 |        500.00 |
+-------------+---------------+--------------+---------------+
5 rows in set (0.00 sec)


*/
DROP VIEW IF EXISTS mv_revenue_by_customer;

DELIMITER $$

CREATE PROCEDURE sp_refresh_customer_revenue_mv()

BEGIN

    DECLARE EXIT HANDLER
    FOR SQLEXCEPTION

    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DROP VIEW IF EXISTS mv_revenue_by_customer;

    CREATE VIEW mv_revenue_by_customer AS

    SELECT

        c.customer_id,

        CONCAT(c.first_name,' ',c.last_name) AS customer_name,

        COUNT(o.order_id) AS total_orders,

        IFNULL(SUM(o.total_amount),0) AS total_revenue

    FROM customers c

    LEFT JOIN orders o

    ON c.customer_id = o.customer_id

    GROUP BY

        c.customer_id,
        c.first_name,
        c.last_name;

    COMMIT;

END $$

DELIMITER ;

CALL sp_refresh_customer_revenue_mv();

SELECT *
FROM mv_revenue_by_customer;