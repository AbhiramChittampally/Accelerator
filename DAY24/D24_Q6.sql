/*
Topic: Modular CTE FormattingStatement: Write a CTE named CustomerOrderDetails that 
retrieves customer full name, food name ordered, and total order amount.
 Select from this CTE all orders with amounts $\ge 300$
 
 
case=1
output=
full_name	food_item	total_amount
Amit Sharma	Chicken Biryani	300.00
Rahul Verma	Dal Tadka	300.00
Neha Patel	Chicken Biryani	600.00
Arjun Gupta	Masala Dosa	360.00



*/
use fs;
USE fs;

WITH CustomerOrderDetails AS
(
    SELECT
        CONCAT(c.first_name,' ',c.last_name) AS full_name,
        f.name AS food_item,
        o.total_amount
    FROM Customers c
    JOIN Orders o
    ON c.customer_id = o.customer_id
    JOIN FoodItems f
    ON o.food_id = f.food_id
)

SELECT
    full_name,
    food_item,
    total_amount
FROM CustomerOrderDetails
WHERE total_amount >= 300;