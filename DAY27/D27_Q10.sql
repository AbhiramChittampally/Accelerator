/*
Problem : 
The platform operations center wants to monitor running sales targets. 
They require a query that computes the cumulative running total of all order 
amounts sorted by order date, and flags the exact order record where the overall 
cumulative company revenue first crosses the milestone threshold of ₹2,000.

case=1
output=

order_id	order_date	total_amount	running_total	milestone_status
1	2026-06-17 11:17:55	300.00	300.00	PRE MILESTONE
2	2026-06-17 11:17:55	150.00	450.00	PRE MILESTONE
3	2026-06-17 11:17:55	80.00	530.00	PRE MILESTONE
4	2026-06-17 11:17:55	240.00	770.00	PRE MILESTONE
5	2026-06-17 11:17:55	60.00	830.00	PRE MILESTONE
6	2026-06-17 11:17:55	120.00	950.00	PRE MILESTONE
7	2026-06-17 11:17:55	250.00	1200.00	PRE MILESTONE
8	2026-06-17 11:17:55	300.00	1500.00	PRE MILESTONE
9	2026-06-17 11:17:55	130.00	1630.00	PRE MILESTONE
10	2026-06-17 11:17:55	100.00	1730.00	PRE MILESTONE
11	2026-06-17 11:17:55	600.00	2330.00	MILESTONE REACHED
12	2026-06-17 11:17:55	200.00	2530.00	POST MILESTONE
13	2026-06-17 11:17:55	120.00	2650.00	POST MILESTONE
14	2026-06-17 11:17:55	360.00	3010.00	POST MILESTONE
15	2026-06-17 11:17:55	150.00	3160.00	POST MILESTONE
16	2026-06-17 11:17:55	160.00	3320.00	POST MILESTONE
17	2026-06-17 11:17:55	250.00	3570.00	POST MILESTONE
18	2026-06-17 11:17:55	200.00	3770.00	POST MILESTONE
19	2026-06-17 11:17:55	260.00	4030.00	POST MILESTONE
20	2026-06-17 11:17:55	180.00	4210.00	POST MILESTONE
*/
USE fs;

WITH RunningRevenue AS
(
    SELECT
        order_id,
        order_date,
        total_amount,

        SUM(total_amount) OVER
        (
            ORDER BY order_id
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS running_total

    FROM Orders
)

SELECT
    order_id,
    order_date,
    total_amount,
    running_total,

    CASE
        WHEN running_total < 2000 THEN 'PRE MILESTONE'
        WHEN running_total - total_amount < 2000 THEN 'MILESTONE REACHED'
        ELSE 'POST MILESTONE'
    END AS milestone_status

FROM RunningRevenue;