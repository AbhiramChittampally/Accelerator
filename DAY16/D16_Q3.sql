/*
Problem Description:
The restaurant marketing team wants to send a promotional thank-you email to customers who have placed individual high-value orders.
Write an SQL query to retrieve the customer's full name (first name and last name combined), their email address, the order ID,
and the specific order's total amount. Use an uncorrelated subquery in the filtering clause to restrict the output to orders whose total_amount 
is strictly greater than the overall average total amount computed across all orders in the system.

case=1
output=
customer_name	email	order_id	total_amount
Neha Patel	neha.patel@yahoo.com	11	600.00
Arjun Gupta	arjun.gupta@gmail.com	14	360.00
Amit Sharma	amit.sharma@gmail.com	1	300.00
Rahul Verma	rahul.verma@gmail.com	8	300.00
Priya Singh	priya.singh@yahoo.com	19	260.00
Rahul Verma	rahul.verma@gmail.com	7	250.00
Arjun Gupta	arjun.gupta@gmail.com	17	250.00
Priya Singh	priya.singh@yahoo.com	4	240.00

*/
use fs;

USE fs;

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    o.order_id,
    o.total_amount
FROM Customers c
JOIN Orders o
ON c.customer_id = o.customer_id
WHERE o.total_amount >
(
    SELECT AVG(total_amount)
    FROM Orders
)
ORDER BY o.total_amount DESC;