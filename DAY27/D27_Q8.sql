/*
Problem : 
The finance team needs a breakdown showing how much revenue each food item 
contributes relative to its entire menu category. Use windowed aggregation SUM() 
OVER(PARTITION BY category) inside a CTE to compute the total category sales and 
calculate each food item's exact percentage contribution to its category revenue.

case=1
output=
category	food_name	item_revenue	category_total_revenue	revenue_pct
Beverages	Mango Lassi	360.00	360.00	100.00
Breads	Butter Naan	240.00	240.00	100.00
Breakfast	Masala Dosa	600.00	900.00	66.67
Breakfast	Chole Bhature	300.00	900.00	33.33
Desserts	Gulab Jamun	350.00	350.00	100.00
Main Course	Chicken Biryani	900.00	2090.00	43.06
Main Course	Paneer Butter Masala	500.00	2090.00	23.92
Main Course	Veg Fried Rice	390.00	2090.00	18.66
Main Course	Dal Tadka	300.00	2090.00	14.35
Snacks	Samosa	270.00	270.00	100.00
*/
use fs;

with cte as(
select 
    f.category, 
    f.name as food_name, 
    sum(o.total_amount) as item_revenue
from Orders o join FoodItems f
on o.food_id=f.food_id
group by 
    f.food_id, 
    f.category, 
    f.name
),
cte2 as(
select
    *,
    sum(item_revenue) over
    (
        partition by category
    ) as category_total_revenue
from cte
)
select  
    *, 
    round(item_revenue*100/category_total_revenue,2) as revenue_pct from cte2
order by category, item_revenue desc;