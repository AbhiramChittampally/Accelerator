USE fs;

EXPLAIN
SELECT *
FROM Customers
WHERE email = 'amit.sharma@gmail.com';

CREATE INDEX idx_customer_email
ON Customers(email);

EXPLAIN
SELECT *
FROM Customers
WHERE email = 'amit.sharma@gmail.com';

SELECT *
FROM Customers
WHERE email = 'amit.sharma@gmail.com';