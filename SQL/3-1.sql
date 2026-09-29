SELECT [DISTINCT]
       column1 AS alias1,
       column2 AS alias2,
       expression AS alias3
FROM table_name alias
WHERE condition1
  AND condition2
  OR condition3
  AND column_name IN (...)
  AND column_name NOT IN (...)
  AND column_name BETWEEN low_value AND high_value
  AND column_name NOT BETWEEN low_value AND high_value
  AND column_name LIKE 'pattern'
  AND column_name NOT LIKE 'pattern'
  AND column_name IS NULL
  AND column_name IS NOT NULL
ORDER BY
      column1 ASC,
      column2 DESC
LIMIT n;