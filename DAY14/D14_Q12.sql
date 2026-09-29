/*
Problem Description:
The kitchen chef wants to see which food categories are demanding the most volume during active shifts. 
Write an SQL query to calculate the total quantity of items ordered for each food category. 
The query should look at all items, but filter the aggregated results to only show categories where the total ordered quantity across all transactions is greater than 5. 
Sort the categories in descending order of total quantity.


case=1
output=
category	total_quantity_ordered
Main Course	10
Snacks	9
Breakfast	8
Desserts	7
Breads	6
Beverages	6


*/
use fs;
select
    f.category,
    sum(o.quantity) as total_quantity_ordered
from FoodItems f
join Orders o
    on o.food_id=f.food_id
group by f.category
having sum(o.quantity)>5
order by total_quantity_ordered desc