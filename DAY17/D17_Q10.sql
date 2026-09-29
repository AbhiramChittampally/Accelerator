/*
Problem Description:
The kitchen inventory control office wants to identify menu choices that haven't registered any successful order fulfillments to optimize stocking space. 
Write a read-only SQL query to find the food ID, item name, category, and price of items inside the FoodItems table whose food_id is entirely absent from
transactional records currently flagged with a status of 'Delivered'.  

case=1
output=

food_id	name	category	price
1	Paneer Butter Masala	Main Course	250.00


*/
use fs;
USE fs;

SELECT
    f.food_id,
    f.name,
    f.category,
    f.price
FROM FoodItems f
WHERE NOT EXISTS
(
    SELECT *
    FROM Orders o
    WHERE o.food_id = f.food_id
      AND o.status = 'Delivered'
);