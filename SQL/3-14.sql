----------------------------------------------------
-- LAG
----------------------------------------------------

SELECT
    columns,
    LAG(column_name, offset, default_value)
        OVER (
            PARTITION BY group_column
            ORDER BY sort_column
        ) AS previous_value
FROM table_name;


----------------------------------------------------
-- LEAD
----------------------------------------------------

SELECT
    columns,
    LEAD(column_name, offset, default_value)
        OVER (
            PARTITION BY group_column
            ORDER BY sort_column
        ) AS next_value
FROM table_name;


----------------------------------------------------
-- Running Total
----------------------------------------------------

SELECT
    columns,
    SUM(column_name)
        OVER (
            PARTITION BY group_column
            ORDER BY sort_column
        ) AS running_total
FROM table_name;


----------------------------------------------------
-- Running Average
----------------------------------------------------

SELECT
    columns,
    AVG(column_name)
        OVER (
            PARTITION BY group_column
            ORDER BY sort_column
        ) AS running_average
FROM table_name;


----------------------------------------------------
-- Moving Average (3-row window)
----------------------------------------------------

SELECT
    columns,
    AVG(column_name)
        OVER (
            ORDER BY sort_column
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS moving_average
FROM table_name;