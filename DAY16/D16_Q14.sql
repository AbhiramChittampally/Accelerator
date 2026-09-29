/*
Problem Description:
The kitchen logistics team wants to identify unusually large transactional orders to optimize packaging and high-volume delivery preparation. 
Write a read-only SQL query to retrieve the order ID, customer ID, order date, food item name, and the recorded total amount for individual transactions. 
Filter the output to return only those orders where the transaction's total_amount is strictly greater than the calculated historical average total amount
spent specifically on that exact food item across the entire platform.

case=1 
output=
order_id	customer_id	order_date	food_item_name	total_amount
11	4	2026-06-17 11:17:55	Chicken Biryani	600.00
14	5	2026-06-17 11:17:55	Masala Dosa	360.00
19	2	2026-06-17 11:17:55	Veg Fried Rice	260.00
12	4	2026-06-17 11:17:55	Gulab Jamun	200.00
18	1	2026-06-17 11:17:55	Chole Bhature	200.00
20	3	2026-06-17 11:17:55	Mango Lassi	180.00
16	5	2026-06-17 11:17:55	Butter Naan	160.00
15	5	2026-06-17 11:17:55	Samosa	150.00

*/
use fs;
select 
    o.order_id,
    o.customer_id,
    o.order_date,
    f.name as food_item_name,
    o.total_amount
from Orders o
join FoodItems f
on o.food_id=f.food_id
where o.total_amount >
(
    select avg(o1.total_amount)
    from Orders o1
    where o1.food_id=o.food_id
    
)
order by o.total_amount desc