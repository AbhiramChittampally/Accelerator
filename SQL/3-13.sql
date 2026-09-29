SELECT *
FROM
(
    SELECT
        columns,
        ROW_NUMBER() OVER
        (
            PARTITION BY grouping_column
            ORDER BY sorting_column DESC
        ) AS rn
    FROM table_name
) t
WHERE rn = N;


----------------------------------------------------
-- ROW_NUMBER
----------------------------------------------------

SELECT *
FROM
(
    SELECT
        columns,
        ROW_NUMBER() OVER
        (
            PARTITION BY group_column
            ORDER BY sort_column DESC
        ) AS rn
    FROM table_name
) t
WHERE rn = 1;


----------------------------------------------------
-- RANK
----------------------------------------------------

SELECT
    columns,
    RANK() OVER
    (
        PARTITION BY group_column
        ORDER BY sort_column DESC
    ) AS rnk
FROM table_name;


----------------------------------------------------
-- DENSE_RANK
----------------------------------------------------

SELECT
    columns,
    DENSE_RANK() OVER
    (
        PARTITION BY group_column
        ORDER BY sort_column DESC
    ) AS dense_rank
FROM table_name;