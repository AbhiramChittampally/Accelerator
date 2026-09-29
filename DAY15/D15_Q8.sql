
/*
Problem Description:
The point-of-sale terminal supervisor wants to analyze processing batches to check for high-ticket individual item sales transactions.
Write an SQL query to list the order date, the count of unique orders placed on that date, and the maximum total amount recorded on a single order. 
Filter the groups to show only dates where the maximum individual order amount exceeds 300.


case=1
output=
explicit_date	total_orders	max_order_amount
2026-06-17	20	600.00


*/
USE fs;
select
    DATE(order_date) as explicit_date,
    count(order_id) as total_orders,
    max(total_amount) as max_order_amount
from Orders 
group by order_date
having MAX(total_amount)>300