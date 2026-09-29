/*
Problem Description:
The financial closing analyst wants to finalize the revenue figures generated exclusively from fulfilled dining transactions.
Write an SQL query to calculate the item name, its category, and the total combined amount collected across all orders. 
Restrict your dataset calculation to orders that are marked with a status of 'Delivered'.
Sort the resulting dataset matrix by the total revenue metric in descending order.


case=1
output=
food_item_name	category	revenue_collected
Masala Dosa	Breakfast	360.00
Chicken Biryani	Main Course	300.00
Dal Tadka	Main Course	300.00
Samosa	Snacks	270.00
Butter Naan	Breads	240.00
Chole Bhature	Breakfast	200.00
Mango Lassi	Beverages	180.00
Gulab Jamun	Desserts	150.00
Veg Fried Rice	Main Course	130.00



*/
use fs;
SELECT 
    f.name AS food_item_name,
    f.category,
    SUM(o.total_amount) AS revenue_collected
FROM 
    FoodItems f
INNER JOIN 
    Orders o ON f.food_id = o.food_id
WHERE 
    o.status = 'Delivered'
GROUP BY 
    f.food_id, f.name, f.category
ORDER BY 
    revenue_collected DESC;