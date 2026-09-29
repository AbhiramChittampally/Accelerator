/*
Problem Description:
The marketing team wants to identify which food items are completely unpopular or haven't successfully converted into delivered sales yet. 
Write an SQL query to list the names of all food items, their categories, and the total count of times they have been successfully delivered.
Use a left join to ensure that food items with zero delivered orders are still present in the list with a count of 0. Sort the results alphabetically by the food item name.

case=1
output=
food_item_name	category	total_delivered_orders
Butter Naan	Breads	2
Chicken Biryani	Main Course	1
Chole Bhature	Breakfast	1
Dal Tadka	Main Course	1
Gulab Jamun	Desserts	1
Mango Lassi	Beverages	1
Masala Dosa	Breakfast	1
Paneer Butter Masala	Main Course	0
Samosa	Snacks	2
Veg Fried Rice	Main Course	1

*/
USE fs;
select
    f.name as food_item_name,
    f.category,
    count(o.order_id) as total_delivered_orders
from FoodItems f
left join Orders o 
    on o.food_id = f.food_id
    and o.status='Delivered'
group by f.name,f.food_id,f.category
order by f.name asc