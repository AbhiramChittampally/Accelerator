/*
Problem : 
The growth marketing division wants to identify customers who are accelerating their 
spending over time. For every order placed by a customer, compare their current order 
amount against the average amount of their previous 2 orders using a window frame. 
Filter and output only orders where the current spending exceeds that 2-order prior 
average.

case=1
output=
order_id	customer_id	order_date	total_amount	prior_2_avg
1	1	2026-06-17 11:17:55	300.00	115.00
18	1	2026-06-17 11:17:55	200.00	190.00
19	2	2026-06-17 11:17:55	260.00	90.00
8	3	2026-06-17 11:17:55	300.00	155.00
7	3	2026-06-17 11:17:55	250.00	215.00
11	4	2026-06-17 11:17:55	600.00	100.00
17	5	2026-06-17 11:17:55	250.00	155.00
*/
USE fs;

WITH CustomerOrders AS
(
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,

        round(AVG(total_amount) OVER
        (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN 2 PRECEDING
            AND 1 PRECEDING),2
        ) AS prior_2_avg

    FROM Orders
)

SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    prior_2_avg
FROM CustomerOrders
WHERE total_amount > prior_2_avg;