/*
Problem 18: Tracking VIP Customer Milestones (Topic 3.9)
Scenario: CRM applications require a database routine to dynamically 
evaluate a user's loyalty tier based on their total transaction 
frequency. The system architecture prefers keeping data manipulation 
logic within the data layer, returning the evaluation state via an 
environment variable.

The Task: Build a stored procedure named sp_evaluate_customer_vip 
that accepts an input parameter customer_id and provides a character 
string OUT parameter named p_vip_tier. If the customer has placed 3 
or more orders, set the output variable value to 'VIP Platinum'. 
If they have exactly 2 orders, set it to 'VIP Gold'. Otherwise, 
evaluate it as 'Standard Customer'.

Expected output=
-----------------
+-----------------+
| customer_status |
+-----------------+
| VIP Platinum    |
+-----------------+
1 row in set (0.00 sec)

*/
DELIMITER $$

CREATE PROCEDURE sp_evaluate_customer_vip
(
    IN p_customer_id INT,
    OUT p_vip_tier VARCHAR(30)
)

BEGIN

    DECLARE v_order_count INT;

    SELECT COUNT(*)
    INTO v_order_count
    FROM Orders
    WHERE customer_id = p_customer_id;

    IF v_order_count >= 3 THEN

        SET p_vip_tier = 'VIP Platinum';

    ELSEIF v_order_count = 2 THEN

        SET p_vip_tier = 'VIP Gold';

    ELSE

        SET p_vip_tier = 'Standard Customer';

    END IF;

END $$

DELIMITER ;

CALL sp_evaluate_customer_vip(1, @customer_status);

SELECT @customer_status AS customer_status;