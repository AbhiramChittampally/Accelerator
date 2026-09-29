/*
Problem Description:
The digital menu management team wants to highlight the single most expensive item within each distinct food category on the menu. 
Write an SQL query to pull the food item ID, name, category, and price. Implement a multi-row correlated subquery that finds items
where the price matches the maximum price computed exclusively for that matching row category.


case=1
output=
food_id	name	category	price
2	Chicken Biryani	Main Course	300.00
3	Masala Dosa	Breakfast	120.00
4	Samosa	Snacks	30.00
5	Gulab Jamun	Desserts	50.00
6	Butter Naan	Breads	40.00
10	Mango Lassi	Beverages	60.00



*/

use fs;
USE fs;

SELECT
    f.food_id,
    f.name,
    f.category,
    f.price
FROM FoodItems f
WHERE f.price =
(
    SELECT MAX(f2.price)
    FROM FoodItems f2
    WHERE f2.category = f.category
);

