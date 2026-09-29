/*
Problem Description:
The operations team wants a diagnostic view of current processing streams that contrasts active transactions right alongside user historic order volumes.
Write a read-only SQL query to output the order ID, customer ID, order date, status, and total amount. Join the main table against an inline derived subquery 
table that pre-calculates the absolute count of historical orders placed by each unique customer ID.

case=1
output=
order_id	customer_id	order_date	status	total_amount	total_customer_orders
1	1	2026-06-17 11:17:55	Delivered	300.00	4
2	1	2026-06-17 11:17:55	Delivered	150.00	4
3	1	2026-06-17 11:17:55	Delivered	80.00	4
4	2	2026-06-17 11:17:55	Preparing	240.00	4
5	2	2026-06-17 11:17:55	Preparing	60.00	4
6	2	2026-06-17 11:17:55	Delivered	120.00	4
7	3	2026-06-17 11:17:55	Cancelled	250.00	4
8	3	2026-06-17 11:17:55	Delivered	300.00	4
9	3	2026-06-17 11:17:55	Delivered	130.00	4
10	4	2026-06-17 11:17:55	Pending	100.00	4
11	4	2026-06-17 11:17:55	Pending	600.00	4
12	4	2026-06-17 11:17:55	Preparing	200.00	4
13	4	2026-06-17 11:17:55	Preparing	120.00	4
14	5	2026-06-17 11:17:55	Delivered	360.00	4
15	5	2026-06-17 11:17:55	Delivered	150.00	4
16	5	2026-06-17 11:17:55	Delivered	160.00	4
17	5	2026-06-17 11:17:55	Preparing	250.00	4
18	1	2026-06-17 11:17:55	Delivered	200.00	4
19	2	2026-06-17 11:17:55	Pending	260.00	4
20	3	2026-06-17 11:17:55	Delivered	180.00	4



*/
use fs;
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount,
    t.total_customer_orders
from Orders o
join 
(
    select customer_id, count(*) as total_customer_orders
    from Orders
    group by customer_id
)as t
on o.customer_id=t.customer_id
order by o.order_id