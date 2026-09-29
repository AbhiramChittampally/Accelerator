/*
Problem : 
The delivery logistics team wants to evaluate customer ordering patterns by ranking 
the longest delays between consecutive orders per customer. Calculate the days 
elapsed between each customer's consecutive orders using LAG() and rank these gap 
durations to surface each customer's single longest idle period between orders.


case=1
output=
customer_id	order_id	days_since_prev_order
1	3	0
1	1	0
1	18	0
2	5	0
2	6	0
2	19	0
3	9	0
3	8	0
3	7	0
4	11	0
4	12	0
4	13	0
5	15	0
5	16	0
5	17	0
*/
USE fs;

WITH CustomerGaps AS
(
    SELECT
        customer_id,
        order_id,

        DATEDIFF
        (
            order_date,
            LAG(order_date) OVER
            (
                PARTITION BY customer_id
                
            )
        ) AS days_since_prev_order

    FROM Orders
)

SELECT
    customer_id,
    order_id,
    days_since_prev_order
FROM CustomerGaps
WHERE days_since_prev_order IS NOT NULL;