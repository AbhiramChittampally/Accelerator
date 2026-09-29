/*
Problem Description:
The operations manager wants to verify the pricing structure of active items on the menu to see if any adjustments are needed for the upcoming holiday season. 
Write an SQL query to extract the category name, the count of active food items in that category, and the average price of those items.
Only evaluate food items that are marked as available (availability = 1) and whose individual price is greater than or equal to 50.

case=1
output=
category	total_available_items	average_price
Main Course	4	207.500000
Breakfast	2	110.000000
Desserts	1	50.000000
Beverages	1	60.000000

*/
use fs;
select
    category,
    count(*) as total_available_items,
    avg(price) as average_price
from FoodItems 
where availability=1 and price>=50
group by category
