/*Problem 1: Partially Masking Customer Contacts 
------------------------------------------------
Scenario: Customer support representatives need to 
verify order deliveries but should not see the customers' full, 
sensitive email addresses or phone numbers.

The Task: Create a secure view named v_customer_masked_directory 
that displays customer_id, the customer's full name as a single 
column (customer_name), a masked email (displaying only the first 
3 characters, followed by ***@domain.com), and a masked phone number 
(displaying only the last 4 digits, prefixed with ******)..



Expected Output:
+-------------+---------------+-------------------+--------------+-------------------+
| customer_id | customer_name | masked_email      | masked_phone | address           |
+-------------+---------------+-------------------+--------------+-------------------+
|           1 | Amit Sharma   | ami***@gmail.com  | ******3210   | Delhi, India      |
|           2 | Priya Singh   | pri***@yahoo.com  | ******1009   | Mumbai, India     |
|           3 | Rahul Verma   | rah***@gmail.com  | ******0998   | Bengaluru, India  |
|           4 | Neha Patel    | neh***@yahoo.com  | ******0987   | Ahmedabad, India  |
|           5 | Arjun Gupta   | arj***@gmail.com  | ******1234   | Hyderabad, India  |
+-------------+---------------+-------------------+--------------+-------------------+

*/

use fs;
create view v_customer_masked_directory as
select 
    customer_id,
    CONCAT(first_name,' ',last_name) AS customer_name,
    CONCAT(
        LEFT(email,3),
        '***@',
        SUBSTRING_INDEX(email,'@',-1)
    ) AS masked_email,
    CONCAT(
        '******',
        RIGHT(phone,4)
    ) AS masked_phone,
    address
from Customers;

select * from v_customer_masked_directory;