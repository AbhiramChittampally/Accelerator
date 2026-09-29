/*
Problem 3 (Medium): Food Category Revenue Distribution
Topic: CTEs & Multi-table Joins

Statement: Analyze sales by category. Write a CTE that sums total order amounts per category across all delivered orders and shows categories generating over ₹500. Display category and total_revenue.

case=1
output=

category	total_revenue
Main Course	730.00
Breakfast	560.00


*/
use fs;
with categrev as
(
    select 
        f.category,
        sum(o.total_amount) as tr
    from Orders o
    join FoodItems f
    on o.food_id=f.food_id
    where o.status='Delivered'
    group by f.category
)
select
    category,
    tr as total_revenue
from categrev
where tr>500