/*
VIP Customer Signature Purchase Identification
-----------------------------------------------
The marketing team is launching a target campaign to thank high-value customers 
for their largest transactions. For every customer who has placed orders, identify 
their single highest monetary order. If a customer has multiple top-value orders of
equal amount, pick the earliest placed order to feature in their account profile.

case=1
output=
order_id	customer_id	total_amount	order_date
1	1	300.00	2026-06-17 11:17:55
19	2	260.00	2026-06-17 11:17:55
8	3	300.00	2026-06-17 11:17:55
11	4	600.00	2026-06-17 11:17:55
14	5	360.00	2026-06-17 11:17:55
*/
USE fs;

WITH CustomerOrders AS
(
    SELECT
        order_id,
        customer_id,
        total_amount,
        order_date,
        ROW_NUMBER() OVER
        (
            PARTITION BY customer_id
            ORDER BY total_amount DESC, order_date ASC
        ) AS rn
    FROM Orders
)

SELECT
    order_id,
    customer_id,
    total_amount,
    order_date
FROM CustomerOrders
WHERE rn = 1;