/*

Problem Description:
The inventory supervisor wants to calculate delivery patterns specifically for accompaniment menu categories like 'Breads' to prepare the kitchen prep list. 
Write an SQL query to retrieve the food item name, its category, and the total number of individual orders placed for that item. 
Filter the system to only look at food items categorized under 'Breads' that have a status of 'Delivered'.

case=1
output=
food_item_name	category	total_successful_orders
Butter Naan	Breads	2



*/
use fs;
select 
    f.name as food_item_name,
    f.category,
    count(o.food_id) as total_successful_orders
from FoodItems f
join Orders o 
on f.food_id=o.food_id
where f.category='Breads' and o.status='Delivered'
group by f.name,f.category
