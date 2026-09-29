/*
Problem Statement

An online food delivery company wants to identify its premium customers based on their purchase history. Every customer may place multiple orders throughout the month. 
The finance department first prepares a summary report showing the total amount spent by each customer and then identifies customers whose total spending is greater than ₹1500. 

The management wants this report to be easy to understand and maintain.

Write an SQL query to generate the report.

Tables Used
Customers
Orders

YOur Task:Generate a report containing

Customer ID
Total Amount Spent

Display only those customers whose total spending is greater than ₹1500.


customer_id	TotalSpent
1	730.00
2	680.00
3	860.00
4	1020.00
5	920.00

*/


USE fs;

WITH CustomerSpending AS
(
    SELECT
        customer_id,
        SUM(total_amount) AS TotalSpent
    FROM Orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    TotalSpent
FROM CustomerSpending
WHERE TotalSpent > 500;