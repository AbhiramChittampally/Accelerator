/*
Problem 17: Multi-Table Transaction Control (Topic 3.9)
Scenario: Marketing wants to roll out a promotional discount scheme across various food menu segments. However, corporate finance 
mandates a safeguard: a product category only qualifies for a promotional discount if it contains 2 or more distinct items. 
If the category does not meet this threshold, the database transaction must roll back completely to protect profit margins.

The Task: Write a stored procedure named sp_apply_bulk_discount that takes a menu category string. It must count the number of food 
options in that category. If the count is greater than or equal to 2, update the prices by applying a 10% discount and commit the transaction. 
If it fails to meet the item threshold, trigger a rollback sequence and throw an error using SIGNAL.

Expected output=
-----------------
+---------+----------------------+--------+-------------+
| food_id | name                 | price  | category    |
+---------+----------------------+--------+-------------+
|       1 | Paneer Butter Masala | 250.00 | Main Course |
|       2 | Chicken Biryani      | 300.00 | Main Course |
+---------+----------------------+--------+-------------+
2 rows in set (0.00 sec)

*/
DELIMITER $$

CREATE PROCEDURE sp_apply_bulk_discount
(
    IN p_category VARCHAR(50)
)
BEGIN

    DECLARE v_count INT;

    START TRANSACTION;

    SELECT COUNT(*)
    INTO v_count
    FROM FoodItems
    WHERE category = p_category;

    IF v_count >= 2 THEN

        UPDATE FoodItems
        SET price = price * 0.90
        WHERE category = p_category;

        COMMIT;

    ELSE

        ROLLBACK;

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Category does not have at least 2 food items';

    END IF;

END $$

DELIMITER ;

CALL sp_apply_bulk_discount('Main Course');

SELECT
    food_id,
    name,
    price,
    category
FROM FoodItems
WHERE category = 'Main Course';