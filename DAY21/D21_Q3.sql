/*
Scenario: A digital food ordering platform needs to process incoming 
customer checkouts securely. If a customer attempts to order a product
that is marked as unavailable in the kitchen registry, the application
layer should catch this issue and halt the entire transaction before
writing data, ensuring invalid entries do not pollute corporate 
metrics.

The Task: Develop a stored procedure named sp_process_secure_order 
that accepts customer_id, food_id, and quantity. 
It must dynamically pull the live unit price and the availability
flag from FoodItems. If the item is marked as out of stock 
(availability = 0), throw a custom database exception via 
SIGNAL SQLSTATE '45000'. 
If it is active, dynamically compute the total order pricing
(price * quantity) and safely record the order history.


Expected output=
-----------------
+----------+-------------+---------+----------+--------------+
| order_id | customer_id | food_id | quantity | total_amount |
+----------+-------------+---------+----------+--------------+
|       12 |           2 |       3 |        1 |       120.00 |
+----------+-------------+---------+----------+--------------+
1 row in set (0.01 sec)
*/
DELIMITER $$

CREATE PROCEDURE sp_process_secure_order
(
    IN p_customer_id INT,
    IN p_food_id INT,
    IN p_quantity INT
)

BEGIN

    DECLARE v_price DECIMAL(10,2);

    DECLARE v_availability INT;

    DECLARE v_total DECIMAL(10,2);

    SELECT
        price,
        availability
    INTO
        v_price,
        v_availability
    FROM FoodItems
    WHERE food_id = p_food_id;

    IF v_availability = 0 THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Food Item is Out of Stock';

    ELSE

        SET v_total = v_price * p_quantity;

        INSERT INTO Orders
        (
            customer_id,
            food_id,
            quantity,
            total_amount
        )
        VALUES
        (
            p_customer_id,
            p_food_id,
            p_quantity,
            v_total
        );

    END IF;

END $$

DELIMITER ;