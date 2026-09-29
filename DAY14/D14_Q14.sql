/*
Problem Description:
The shipping coordinators want to find unique transaction entries where a customer bought an unusually high volume of an individual item in a single order line.
Write an SQL query to find the order ID, customer ID, and the maximum quantity ordered in a single transaction. 
Filter the rows down to only showcase orders where the individual quantity is 3 or more and the status is listed as 'Delivered' or 'Preparing'.

case=1
output=
order_id	customer_id	maximum_quantity
15	5	5
6	2	4
12	4	4
16	5	4
2	1	3
14	5	3
20	3	3

*/
use fs;
select
    o.order_id,
    c.customer_id,
    o.quantity as maximum_quantity
from Customers c
join Orders o
on o.customer_id = c.customer_id
where o.quantity >= 3 and o.status IN ('Delivered','Preparing')
order by o.quantity desc