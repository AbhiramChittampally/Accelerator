/*
Problem Description:
The sales auditing coordinator wants to review bulk transaction records to monitor high-value orders. Write an SQL query to retrieve the order ID,
the customer's first name, the food item name, the quantity ordered, and the recorded total amount from the database. Filter the records to only 
display orders where the customer purchased more than 1 quantity of that item in a single transaction, and the order's total_amount is strictly greater than 200. 
Sort the output in descending order of the total amount.

case=1
output=
order_id	first_name	food_item_name	quantity	total_amount
11	Neha	Chicken Biryani	2	600.00
14	Arjun	Masala Dosa	3	360.00
8	Rahul	Dal Tadka	2	300.00
19	Priya	Veg Fried Rice	2	260.00
4	Priya	Masala Dosa	2	240.00




*/
use fs;
select
    o.order_id,
    c.first_name,
    f.name as food_item_name,
    o.quantity,
    o.total_amount
from Orders o
join Customers c
on o.customer_id=c.customer_id
join FoodItems f
on o.food_id=f.food_id
where o.quantity>1
and o.total_amount>200
order by o.total_amount desc;
