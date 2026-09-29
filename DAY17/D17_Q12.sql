/*
A fraud detection analyst wants to discover highly localized transaction spikes where a consumer places an order that deviates significantly 
from their personal buying choices. Write a read-only SQL query to retrieve the order ID, customer ID, food ID, and total amount from the Orders table.
The query must filter records using an optimized correlated subquery to return only those orders whose individual total_amount is strictly
greater than twice the historical average order amount calculated for that specific customer's profile.

case=1
output=
order_id	customer_id	food_id	total_amount
11	4	2	600.00



*/
use fs;

select 
    o.order_id,
    o.customer_id,
    o.food_id,
    o.total_amount
from Orders o
where o.total_amount>
(
    2*
    (
        select avg(o2.total_amount)
        from Orders o2
        where o2.customer_id=o.customer_id
    )
)