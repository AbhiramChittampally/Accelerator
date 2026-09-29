/*
Problem: Repeat Customer Order Interval Frequency
The customer retention division wants to measure repeat user engagement speed on 
the platform. For every order placed by a customer, determine the previous order 
date from that same user and calculate the exact elapsed time (in hours) between 
consecutive transactions. This metric helps measure user purchase frequency.

case=1
output=
customer_id	order_id	order_date	prev_order_date	hours_since_last_order
1	2	2026-06-17 11:17:55	NULL	NULL
1	3	2026-06-17 11:17:55	2026-06-17 11:17:55	0
1	1	2026-06-17 11:17:55	2026-06-17 11:17:55	0
1	18	2026-06-17 11:17:55	2026-06-17 11:17:55	0
2	4	2026-06-17 11:17:55	NULL	NULL
2	5	2026-06-17 11:17:55	2026-06-17 11:17:55	0
2	6	2026-06-17 11:17:55	2026-06-17 11:17:55	0
2	19	2026-06-17 11:17:55	2026-06-17 11:17:55	0
3	20	2026-06-17 11:17:55	NULL	NULL
3	9	2026-06-17 11:17:55	2026-06-17 11:17:55	0
3	8	2026-06-17 11:17:55	2026-06-17 11:17:55	0
3	7	2026-06-17 11:17:55	2026-06-17 11:17:55	0
4	10	2026-06-17 11:17:55	NULL	NULL
4	11	2026-06-17 11:17:55	2026-06-17 11:17:55	0
4	12	2026-06-17 11:17:55	2026-06-17 11:17:55	0
4	13	2026-06-17 11:17:55	2026-06-17 11:17:55	0
5	14	2026-06-17 11:17:55	NULL	NULL
5	15	2026-06-17 11:17:55	2026-06-17 11:17:55	0
5	16	2026-06-17 11:17:55	2026-06-17 11:17:55	0
5	17	2026-06-17 11:17:55	2026-06-17 11:17:55	0
*/
USE fs;

SELECT
    customer_id,
    order_id,
    order_date,

    LAG(order_date,1) OVER
    (
        PARTITION BY customer_id
        order by customer_id
    ) AS prev_order_date,

    TIMESTAMPDIFF
    (
        HOUR,
        LAG(order_date,1) OVER
        (
            PARTITION BY customer_id
            order by customer_id
            
        ),
        order_date
    ) AS hours_since_last_order

FROM Orders
