/*
Problem 6: Name Formatting Utility
------------------------------------
Scenario: The marketing automation system needs customer names
formatted uniformly as "Last Name, First Name" for printable 
mailing vouchers.

The Task: Write a stored function fn_format_customer_name that 
accepts a customer_id and returns their formatted full name.

Expected output:
---------------
+-------------+---------------+
| customer_id | mailing_label |
+-------------+---------------+
|           1 | Sharma, Amit  |
|           2 | Singh, Priya  |
|           3 | Verma, Rahul  |
+-------------+---------------+


*/

USE fs;

DELIMITER //

CREATE FUNCTION fn_format_customer_name(p_customer_id INT)
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    DECLARE formatted_name VARCHAR(100);

    SELECT CONCAT(last_name, ', ',first_name)
    INTO formatted_name
    FROM Customers
    WHERE customer_id = p_customer_id;

    RETURN formatted_name;
END //

DELIMITER ;

SELECT
    customer_id,
    fn_format_customer_name(customer_id) AS mailing_label
FROM Customers;