/*
The food delivery kitchen staff needs item-level preparation tickets printed for 
every individual item ordered rather than grouped totals. If a customer orders a 
quantity of 5 items, the system must generate 5 distinct sequence rows for that order 
line.
This granular expansion helps chefs track individual meal prep steps sequentially 
during peak rush hours.

case=1
output=

order_id	customer_id	food_id	item_number	quantity
1	1	2	1	1
2	1	5	1	3
2	1	5	2	3
2	1	5	3	3
3	1	6	1	2
3	1	6	2	2
4	2	3	1	2
4	2	3	2	2
5	2	10	1	1
6	2	4	1	4
6	2	4	2	4
6	2	4	3	4
6	2	4	4	4
7	3	1	1	1
8	3	7	1	2
8	3	7	2	2
9	3	9	1	1
10	4	8	1	1
11	4	2	1	2
11	4	2	2	2
12	4	5	1	4
12	4	5	2	4
12	4	5	3	4
12	4	5	4	4
13	4	10	1	2
13	4	10	2	2
14	5	3	1	3
14	5	3	2	3
14	5	3	3	3
15	5	4	1	5
15	5	4	2	5
15	5	4	3	5
15	5	4	4	5
15	5	4	5	5
16	5	6	1	4
16	5	6	2	4
16	5	6	3	4
16	5	6	4	4
17	5	1	1	1
18	1	8	1	2
18	1	8	2	2
19	2	9	1	2
19	2	9	2	2
20	3	10	1	3
20	3	10	2	3
20	3	10	3	3



*/
USE fs;

WITH RECURSIVE OrderItems AS
(
    
    SELECT
        order_id,
        customer_id,
        food_id,
        1 AS item_number,
        quantity
    FROM Orders

    UNION ALL

    
    SELECT
        order_id,
        customer_id,
        food_id,
        item_number + 1,
        quantity
    FROM OrderItems
    WHERE item_number < quantity
)

SELECT
    order_id,
    customer_id,
    food_id,
    item_number,
    quantity
FROM OrderItems
ORDER BY order_id, item_number;

