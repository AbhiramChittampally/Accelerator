SELECT
    grouping_column1,
    grouping_column2,
    COUNT(*) AS total_rows,
    COUNT(column_name) AS non_null_count,
    COUNT(DISTINCT column_name) AS unique_count,
    SUM(numeric_column) AS total,
    AVG(numeric_column) AS average,
    MIN(numeric_column) AS minimum,
    MAX(numeric_column) AS maximum
FROM table_name
WHERE row_condition
GROUP BY
    grouping_column1,
    grouping_column2
HAVING aggregate_condition
ORDER BY
    grouping_column1 ASC;