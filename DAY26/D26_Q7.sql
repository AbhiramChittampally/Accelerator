/*
Problem: Cumulative Platform Revenue Stream
The finance department needs a real-time ledger tracking cumulative revenue 
performance over time. They want to inspect every transaction in sequential 
order alongside a running aggregate total of overall customer spend. This ledger
provides quick visibility into cash flow growth across the platform.

case=1
output=
order_id	order_date	total_amount	running_revenue_total
11	2026-06-17 11:17:55	600.00	4210.00
20	2026-06-17 11:17:55	180.00	4210.00
19	2026-06-17 11:17:55	260.00	4210.00
18	2026-06-17 11:17:55	200.00	4210.00
17	2026-06-17 11:17:55	250.00	4210.00
16	2026-06-17 11:17:55	160.00	4210.00
15	2026-06-17 11:17:55	150.00	4210.00
14	2026-06-17 11:17:55	360.00	4210.00
13	2026-06-17 11:17:55	120.00	4210.00
12	2026-06-17 11:17:55	200.00	4210.00
1	2026-06-17 11:17:55	300.00	4210.00
10	2026-06-17 11:17:55	100.00	4210.00
9	2026-06-17 11:17:55	130.00	4210.00
8	2026-06-17 11:17:55	300.00	4210.00
7	2026-06-17 11:17:55	250.00	4210.00
6	2026-06-17 11:17:55	120.00	4210.00
5	2026-06-17 11:17:55	60.00	4210.00
4	2026-06-17 11:17:55	240.00	4210.00
3	2026-06-17 11:17:55	80.00	4210.00
2	2026-06-17 11:17:55	150.00	4210.00



*/
use fs;
USE fs;

SELECT
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER
    (
        ORDER BY order_date
    ) AS running_revenue_total
FROM Orders;