/*
Problem : Category Product Launch Pioneer

The food platform operation team is analyzing product launch performance 
across different culinary categories. For each category (e.g., Main Course, Breakfast, Snacks), 
they need to identify the very first item ordered historically on the platform. 
This will help assess initial category traction and order timing patterns.

case=1
output=
order_id	category	food_item	order_date
20	Beverages	Mango Lassi	2026-06-17 11:17:55
3	Breads	Butter Naan	2026-06-17 11:17:55
4	Breakfast	Masala Dosa	2026-06-17 11:17:55
2	Desserts	Gulab Jamun	2026-06-17 11:17:55
11	Main Course	Chicken Biryani	2026-06-17 11:17:55
15	Snacks	Samosa	2026-06-17 11:17:55



*/
use fs;
USE fs;

WITH CategoryOrders AS
(
    SELECT
        o.order_id,
        f.category,
        f.name AS food_item,
        o.order_date,
        ROW_NUMBER() OVER
        (
            PARTITION BY f.category
            
        ) AS rn
    FROM Orders o
    JOIN FoodItems f
    ON o.food_id = f.food_id
)

SELECT
    order_id,
    category,
    food_item,
    order_date
FROM CategoryOrders
WHERE rn = 1;