/*
Problem : 
The fraud and anomaly detection unit wants to identify unusual localized transaction 
spikes in order history. Write a query to flag order records where total spend is 
strictly higher than both the immediately preceding order and the immediately 
following order in time sequence.

case=1
output=
order_id	total_amount	prev_amt	next_amt
19	260.00	180.00	200.00
17	250.00	200.00	160.00
14	360.00	150.00	120.00
1	300.00	200.00	100.00
8	300.00	130.00	250.00
4	240.00	60.00	80.00

*/
USE fs;

WITH OrderComparison AS
(
    SELECT
        order_id,
        total_amount,

        LAG(total_amount) OVER
        (
            ORDER BY order_date DESC
        ) AS prev_amt,

        LEAD(total_amount) OVER
        (
            ORDER BY order_date DESC
        ) AS next_amt

    FROM Orders
)

SELECT
    order_id,
    total_amount,
    prev_amt,
    next_amt
FROM OrderComparison
WHERE total_amount > prev_amt
AND total_amount > next_amt;