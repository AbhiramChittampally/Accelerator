/*
Problem 1 (Medium): High-Value Customers with Delivered Orders
Topic: CTEs & Aggregation Filtering

Statement: The operations team wants to identify top-spending customers using only completed orders. Write a query with a CTE to aggregate total spending for Delivered status orders, then filter for customers who spent more than ₹500. Display customer_id, first_name, and Delivered_Spent.



case=1
output=
case=1
output=
customer_id	first_name	Delivered_Spent
1	Amit	730.00
3	Rahul	610.00
5	Arjun	670.00

*/
use fs;
USE fs;

WITH CustomerSpending AS
(
    SELECT
        customer_id,
        SUM(total_amount) AS Delivered_Spent
    FROM Orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.first_name,
    cs.Delivered_Spent
FROM Customers c
JOIN CustomerSpending cs
ON c.customer_id = cs.customer_id
WHERE cs.Delivered_Spent > 500;