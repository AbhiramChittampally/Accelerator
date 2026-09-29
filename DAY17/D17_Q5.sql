/*
An enterprise data analyst needs to audit high-performing customer accounts to identify regional market leaders.
Write a read-only SQL query to find the customer ID, their full name (first name and last name combined), their city address, 
and their total lifetime expenditure across all orders.

Filter the results using a complex correlated subquery inside the HAVING clause so that you only return customers whose 
cumulative lifetime spending is strictly greater than the historical average of individual transaction amounts placed by all customers living in that exact same city.

case=1
output=
customer_id	customer_name	city_address	total_customer_lifetime_spend
4	Neha Patel	Ahmedabad, India	1020.00
5	Arjun Gupta	Hyderabad, India	920.00
3	Rahul Verma	Bengaluru, India	860.00
1	Amit Sharma	Delhi, India	730.00
2	Priya Singh	Mumbai, India	680.00

*/
use fs;
select
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as customer_name,
    c.address as city_address,
    sum(o.total_amount) as total_customer_lifetime_spend
from Customers c
join Orders o
on c.customer_id=o.customer_id
group by
    c.customer_id,
    c.first_name,
    c.last_name
having sum(o.total_amount)>
(
    select avg(o2.total_amount)
    from Customers c2
    join Orders o2
    ON c2.customer_id = o2.customer_id
    WHERE c2.address = c.address
)
order by total_customer_lifetime_spend desc;