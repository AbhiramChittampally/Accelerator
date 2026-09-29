/*
Problem Description:
The restaurant finance team wants to audit the total revenue generated from high-value food items.
Write an SQL query to find the food item name, its category, and the total revenue generated from it (calculated as the sum of the total amount across all orders).
Only include items belonging to the 'Main Course' or 'Breakfast' categories where the item has been ordered a total quantity of more than 2 times. 
Sort the results by total revenue in descending order.

case=1
output=
food_item_name	category	total_revenue
Chicken Biryani	Main Course	900.00
Masala Dosa	Breakfast	600.00
Veg Fried Rice	Main Course	390.00
Chole Bhature	Breakfast	300.00

*/
use fs;
select
    f.name as food_item_name,
    f.category,
    sum(o.total_amount) as total_revenue
from FoodItems f
join Orders o
    on o.food_id=f.food_id
where f.category IN ('Main Course','Breakfast')
group by f.food_id,f.name,f.category
having sum(o.quantity)>2
order by total_revenue desc

