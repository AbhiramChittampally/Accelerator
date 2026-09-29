/*
Problem Description:
The restaurant sales audit team wants to flag orders that have recorded an exceptionally high quantity of items 
relative to typical customer selections.Write a read-only SQL query to retrieve the order ID, customer ID, food ID, and quantity.
Filter the results using an uncorrelated subquery in the WHERE clause to display only those orders where the quantity ordered is strictly greater 
than the overall average quantity calculated across all orders in the database.

case=1
output=
order_id	customer_id	food_id	quantity
15	5	4	5
6	2	4	4
12	4	5	4
16	5	6	4
2	1	5	3
14	5	3	3
20	3	10	3



*/
use fs;

select 
    order_id,
    customer_id,
    food_id,
    quantity
from Orders 
where quantity >
(
    select avg(quantity)
    from Orders
)
order by quantity desc,order_id asc

