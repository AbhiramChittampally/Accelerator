/*
Problem Description:
The executive board wants to identify standard transaction sizes to evaluate point-of-sale pricing tiers.
Write an SQL query to calculate the total number of orders and the average total amount spent per order for each unique customer ID.
Filter out any individual orders with a total_amount less than 100 before computing metrics, and only show customers who have placed at least 2 such orders.


case=1
output=
customer_id	qualified_orders_count	average_order_value
1	3	216.666667
2	3	206.666667
3	4	215.000000
4	4	255.000000
5	4	230.000000



*/
use fs;
select
    c.customer_id,
    COUNT(o.order_id) AS qualified_orders_count,
    AVG(o.total_amount) AS average_order_value
from Customers c
join Orders o
on c.customer_id=o.customer_id
where o.total_amount>=100
group by c.customer_id
having count(o.customer_id)>=2