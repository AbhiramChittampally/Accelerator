/*
Problem: Sequential Transaction Delta Tracking
The risk management team is analyzing transaction variance across consecutive
platform orders. They need a query displaying each order's total spend alongside
the amount spent in the immediately preceding order. Additionally, calculate the
numeric variance (delta) between current and prior purchases to detect unusual 
shifts.

case=1
output=
order_id	order_date	current_amount	prev_amount	amount_diff
11	2026-06-17 11:17:55	600.00	NULL	NULL
20	2026-06-17 11:17:55	180.00	600.00	-420.00
19	2026-06-17 11:17:55	260.00	180.00	80.00
18	2026-06-17 11:17:55	200.00	260.00	-60.00
17	2026-06-17 11:17:55	250.00	200.00	50.00
16	2026-06-17 11:17:55	160.00	250.00	-90.00
15	2026-06-17 11:17:55	150.00	160.00	-10.00
14	2026-06-17 11:17:55	360.00	150.00	210.00
13	2026-06-17 11:17:55	120.00	360.00	-240.00
12	2026-06-17 11:17:55	200.00	120.00	80.00
1	2026-06-17 11:17:55	300.00	200.00	100.00
10	2026-06-17 11:17:55	100.00	300.00	-200.00
9	2026-06-17 11:17:55	130.00	100.00	30.00
8	2026-06-17 11:17:55	300.00	130.00	170.00
7	2026-06-17 11:17:55	250.00	300.00	-50.00
6	2026-06-17 11:17:55	120.00	250.00	-130.00
5	2026-06-17 11:17:55	60.00	120.00	-60.00
4	2026-06-17 11:17:55	240.00	60.00	180.00
3	2026-06-17 11:17:55	80.00	240.00	-160.00
2	2026-06-17 11:17:55	150.00	80.00	70.00



*/

USE fs;

select
    order_id, 
    order_date, 
    total_amount as current_amount,
    lag(total_amount,1) over
    (   
        order by order_date 
    )as prev_amount,
    total_amount-lag(total_amount,1) over
    (
        order by order_date
    ) as amount_diff
from Orders;