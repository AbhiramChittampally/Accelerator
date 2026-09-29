/*
Problem: Moving Average Order Value Smoother
To smooth out short-term fluctuations in order volume, the business intelligence team 
requires a 3-order centered moving average calculation. For each order in 
chronological sequence, compute the average purchase amount across a sliding frame 
consisting of the immediate prior order, current order, and immediate subsequent order.

case=1
output=
order_id	order_date	total_amount	moving_avg_3_orders
11	2026-06-17 11:17:55	600.00	390.000000
20	2026-06-17 11:17:55	180.00	346.666667
19	2026-06-17 11:17:55	260.00	213.333333
18	2026-06-17 11:17:55	200.00	236.666667
17	2026-06-17 11:17:55	250.00	203.333333
16	2026-06-17 11:17:55	160.00	186.666667
15	2026-06-17 11:17:55	150.00	223.333333
14	2026-06-17 11:17:55	360.00	210.000000
13	2026-06-17 11:17:55	120.00	226.666667
12	2026-06-17 11:17:55	200.00	206.666667
1	2026-06-17 11:17:55	300.00	200.000000
10	2026-06-17 11:17:55	100.00	176.666667
9	2026-06-17 11:17:55	130.00	176.666667
8	2026-06-17 11:17:55	300.00	226.666667
7	2026-06-17 11:17:55	250.00	223.333333
6	2026-06-17 11:17:55	120.00	143.333333
5	2026-06-17 11:17:55	60.00	140.000000
4	2026-06-17 11:17:55	240.00	126.666667
3	2026-06-17 11:17:55	80.00	156.666667
2	2026-06-17 11:17:55	150.00	115.000000



*/
use fs;
USE fs;

SELECT
    order_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER
    (
        ORDER BY order_date
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS moving_avg_3_orders
FROM Orders;