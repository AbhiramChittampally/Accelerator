/*
Problem Description:
The operational marketing team wants to find the IDs of customers who have ordered 'Chicken Biryani' AND have ordered 'Mango Lassi', 
but have completely excluded 'Samosa' from their ordering lifetime history. Structure a combination of INTERSECT and EXCEPT clauses 
driven by internal target-matching subqueries to extract this precise segmentation.



case=1
output=
customer_id
4



*/
use fs;
select 
    customer_id
from Orders
where food_id = 
(
    select food_id 
    from FoodItems
    where  name='Chicken Biryani'
)

INTERSECT

select customer_id
from Orders
where food_id=
(
    select food_id
    from FoodItems 
    where name='Mango Lassi'
)

EXCEPT

select customer_id
from Orders
where food_id=
(
    select food_id
    from FoodItems 
    where name='Samosa'
)