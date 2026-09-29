/*
Topic: Date Sequence Generation

Statement: Generate a sequence of daily dates from 2026-07-10 to 2026-07-17 to find dates where NO food orders were placed.

case=1
output=
order_date
2026-07-10
2026-07-11
2026-07-12
2026-07-13
2026-07-14
2026-07-15
2026-07-16
2026-07-17



*/
USE fs;

WITH RECURSIVE DateSequence AS
(
    SELECT DATE('2026-07-10') AS order_date

    UNION ALL

    SELECT DATE_ADD(order_date, INTERVAL 1 DAY)
    FROM DateSequence
    WHERE order_date < '2026-07-17'
)

SELECT
    d.order_date
FROM DateSequence d
LEFT JOIN Orders o
ON d.order_date = o.order_date
WHERE o.order_date IS NULL;