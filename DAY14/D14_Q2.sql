/*

Problem Description:
The restaurant management team wants to evaluate customer ordering patterns to optimize their inventory for the current month. 
Write an SQL query to retrieve the customer's first name, last name, and the total number of items they have ordered that are currently in a 'Delivered' status. 
The results should only include customers who have placed more than 2 delivered orders. 
Display the final output sorted in descending order of the total items ordered.

case=1 
output=
first_name	last_name	total_items_ordered
Arjun	Gupta	12
Amit	Sharma	8
Rahul	Verma	6


*/
USE fs;

SELECT
    c.first_name,
    c.last_name,
    SUM(o.quantity) AS total_items_ordered
FROM Customers c
JOIN Orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 2
ORDER BY total_items_ordered DESC;