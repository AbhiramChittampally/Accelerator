/*
Problem Description:
The analytics desk wants to compile a list of highly engaged customer contacts for a targeted outreach program. 
Write a read-only query that uses the UNION operator to find the unique customer IDs, first names, and emails of customers
who have either placed a single order exceeding a quantity of 3 or have successfully spent more than 300.00 in a single transaction.



case=1
output=
customer_id	first_name	email
2	Priya	priya.singh@yahoo.com
4	Neha	neha.patel@yahoo.com
5	Arjun	arjun.gupta@gmail.com



*/
use fs;
select 
    c.customer_id,
    c.first_name,
    c.email
from Customers c
join Orders o
on c.customer_id=o.customer_id
where o.quantity > 3

UNION

select 
    c.customer_id,
    c.first_name,
    c.email
from Customers c
join Orders o
on c.customer_id=o.customer_id
where o.total_amount > 300