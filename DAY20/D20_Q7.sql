USE fs;



CREATE PROCEDURE sp_get_order_count_by_status(
    IN p_status VARCHAR(20),
    OUT total_orders INT
)
BEGIN
    SELECT COUNT(*)
    INTO total_orders
    FROM Orders
    WHERE status = p_status;
END 

DELIMITER ;

-- Call the procedure
CALL sp_get_order_count_by_status('Delivered', @total_orders_delivered);

-- Display the OUT parameter
SELECT @total_orders_delivered AS total_orders_delivered;