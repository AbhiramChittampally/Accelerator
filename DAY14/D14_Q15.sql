/*
Problem Description:
The customer service helpdesk requires a comprehensive master report to verify line-item details for pending financial reconciliations. 
Write an SQL query to combine data from three tables to extract the customer's email, the order date, the food item name, the individual item price, and the total amount charged. 
Filter the output to show only transactions where the order status is 'Pending'.
Sort the output chronologically by the order date.


case=1
output=
email	order_date	food_item_name	unit_price	total_amount
neha.patel@yahoo.com	2026-06-17 11:17:55	Chole Bhature	100.00	100.00
neha.patel@yahoo.com	2026-06-17 11:17:55	Chicken Biryani	300.00	600.00
priya.singh@yahoo.com	2026-06-17 11:17:55	Veg Fried Rice	130.00	260.00



*/
use fs;
select
    c.email,
    o.order_date,
    f.name as food_item_name,
    f.price as unit_price,
    o.total_amount
from Customers c
join Orders o 
on c.customer_id=o.customer_id
join FoodItems f
on o.food_id=f.food_id
where o.status='Pending'
order by o.order_date asc
