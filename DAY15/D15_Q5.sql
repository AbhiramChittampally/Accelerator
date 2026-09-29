/*
Problem Description:
The food truck operations desk wants to check the historical sales velocities specifically for quick-service categories. 
Write an SQL query to discover the order ID, the food item name, its category, and the quantity ordered.
Limit the rows to items classified under the 'Snacks' or 'Beverages' categories, and ensure only orders with an explicit quantity of 2 or more are returned. 
Sort the list by quantity in descending order.

case=1
output=
order_id	food_item_name	category	quantity
15	Samosa	Snacks	5
6	Samosa	Snacks	4
20	Mango Lassi	Beverages	3
13	Mango Lassi	Beverages	2



*/
use fs;
select
    o.order_id,
    f.name as food_item_name,
    f.category,
    o.quantity
from FoodItems f
join Orders o
on f.food_id=o.food_id
where f.category IN ('Snacks','Beverages')
group by
o.order_id
having o.quantity>=2
order by o.quantity desc