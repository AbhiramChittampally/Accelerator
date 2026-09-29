/*
Problem Description:
The email marketing team is preparing a specific discount campaign targeting users on legacy email platforms.
Write an SQL query to find the customer's full name, email address, physical location, and the total quantity of items they ordered across all transactions.
Limit the base records to customers whose email ends with '@yahoo.com'.
Sort the output based on the total quantity in descending order.

case=1
output=
customer_name	email	address	total_quantity_ordered
Priya Singh	priya.singh@yahoo.com	Mumbai, India	9
Neha Patel	neha.patel@yahoo.com	Ahmedabad, India	9



*/
use fs;
select
    concat(c.first_name,' ',c.last_name) as customer_name,
    c.email,
    c.address,
    sum(o.quantity) as total_quantity_ordered
from Customers c
join Orders o
on c.customer_id=o.customer_id
WHERE c.email LIKE '%@yahoo.com'
group by c.customer_id,customer_name,c.address
order by sum(o.quantity) desc