USE fs;

DELIMITER //

CREATE FUNCTION fn_check_food_eligibility(p_food_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE is_orderable INT;

    SELECT IFNULL(availability, 0)
    INTO is_orderable
    FROM FoodItems
    WHERE food_id = p_food_id;

    RETURN IFNULL(is_orderable, 0);
END //

DELIMITER ;

-- Test
SELECT
    food_id,
    name,
    fn_check_food_eligibility(food_id) AS is_orderable
FROM FoodItems;