/*
Problem: Food Menu Item Demand Popularity Index

The inventory management team wants to rank menu offerings based on customer 
consumption. They require a breakdown of total item quantities sold across all 
completed orders and want each item ranked by total sales volume. This popularity
 metric will determine which items receive primary placement on the food platform.



case=1
output=
name	category	total_qty	popularity_rank
Samosa	Snacks	9	1
Gulab Jamun	Desserts	7	2
Butter Naan	Breads	6	3
Mango Lassi	Beverages	6	3
Masala Dosa	Breakfast	5	5
Chicken Biryani	Main Course	3	6
Chole Bhature	Breakfast	3	6
Veg Fried Rice	Main Course	3	6
Paneer Butter Masala	Main Course	2	9
Dal Tadka	Main Course	2	9



*/
use fs;
USE fs;

WITH FoodPopularity AS
(
    SELECT
        f.name,
        f.category,
        SUM(o.quantity) AS total_qty
    FROM FoodItems f
    JOIN Orders o
    ON f.food_id = o.food_id
    GROUP BY
        f.food_id,
        f.name,
        f.category
)

SELECT
    name,
    category,
    total_qty,
    RANK() OVER
    (
        ORDER BY total_qty DESC
    ) AS popularity_rank
FROM FoodPopularity;