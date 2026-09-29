
/*
Problem Description:
The marketing team wants a list of customers who have registered a user profile on the platform but have never placed any food orders.
Write an SQL query to select the customer ID, first name, last name, and email from the Customers table. 
Implement an uncorrelated subquery tracking all unique customer IDs present in the Orders table to filter them out using a NOT IN constraint.


case=1
output=
customer_id	first_name	last_name	email



*/
use fs;
SELECT 
    customer_id, 
    first_name, 
    last_name, 
    email
FROM 
    Customers
WHERE 
    customer_id NOT IN (
        SELECT DISTINCT customer_id 
        FROM Orders 
        WHERE customer_id IS NOT NULL
    );