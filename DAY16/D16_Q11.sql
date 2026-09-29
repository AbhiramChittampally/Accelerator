/*

Problem Description:
The business intelligence developer wants to identify high-value breakfast consumers to target with a new morning loyalty campaign.
Write a read-only SQL query to retrieve the customer's full name, email address, and their total lifetime spending across all menu categories.
Filter the output to return only those customers whose cumulative spending specifically on items in the 'Breakfast' category is 
strictly greater than the average breakfast expenditure calculated across all customers who have ordered breakfast.

case=1
output=
customer_name	email	total_lifetime_spending
Priya Singh	priya.singh@yahoo.com	680.00
Arjun Gupta	arjun.gupta@gmail.com	920.00



*/
use fs;

select 
    concat(c.first_name, ' ', c.last_name) as customer_name,
    c.email,
    sum(o.total_amount) as total_lifetime_spending
from Customers c
join Orders o
on c.customer_id=o.customer_id
group by
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email
having
(
    select sum(o1.total_amount)
    from Orders o1
    join FoodItems f
    on o1.food_id=f.food_id
    where o1.customer_id=c.customer_id
    and f.category='Breakfast'
)    
>
(
    select avg(breakfast_total)
    from
    (
        select sum(o2.total_amount) as breakfast_total
        from Orders o2
        join FoodItems f1
        on o2.food_id=f1.food_id
        where f1.category='Breakfast'
        group by o2.customer_id
        
    )as t
)
