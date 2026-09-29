/*
Problem Description:
The kitchen manager needs to review details for all orders containing items priced strictly above the calculated average price of all available food items on the menu.
Write an SQL query to retrieve the unique order IDs, customer IDs, and total amounts from the Orders table for these high-value items. 
Use an uncorrelated subquery in the WHERE clause to compute the baseline average price.

case=1
output=
order_id	customer_id	total_amount
7	3	250.00
17	5	250.00
1	1	300.00
11	4	600.00
8	3	300.00
9	3	130.00
19	2	260.00



*/
USE fs;

SELECT
    o.order_id,
    o.customer_id,
    o.total_amount
FROM Orders o
JOIN FoodItems f
ON o.food_id = f.food_id
WHERE f.price >
(
    SELECT AVG(price)
    FROM FoodItems
);