USE fs;

EXPLAIN
SELECT *
FROM Orders
WHERE customer_id = 1
AND status = 'Delivered';

CREATE INDEX idx_orders_cust_status
ON Orders(customer_id, status);

EXPLAIN
SELECT *
FROM Orders
WHERE customer_id = 1
AND status = 'Delivered';

SELECT *
FROM Orders
WHERE customer_id = 1
AND status = 'Delivered';