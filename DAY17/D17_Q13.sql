
/*
Problem Description:
The marketing division wants to identify dominant menu items that hold a high market share within their menu sections to create focused combos. 
Write a read-only SQL query to calculate the food item name, category, and total revenue pool for successfully processed rows. Use an advanced 
correlated subquery inside the HAVING clause to filter the final dataset to show only those individual food items whose cumulative sales account 
for more than 35% of the entire revenue generated within that product's parent menu category.


case=1
output=
food_item_name	category	item_total_revenue
Chicken Biryani	Main Course	900.00
Masala Dosa	Breakfast	600.00
Mango Lassi	Beverages	360.00
Gulab Jamun	Desserts	350.00
Samosa	Snacks	270.00
Butter Naan	Breads	240.00



*/
use fs;
select 
    f.name as food_item_name,
    f.category,
    sum(o.total_amount) as item_total_revenue
from FoodItems f
join Orders o
on f.food_id = o.food_id
group by 
    f.food_id,
    f.name,
    f.category
having sum(o.total_amount)>
(
    0.35*
    (
        select sum(o2.total_amount)
        from FoodItems f2
        join Orders o2
        on f2.food_id=o2.food_id
        where f2.category=f.category
    )
)ORDER BY item_total_revenue desc
