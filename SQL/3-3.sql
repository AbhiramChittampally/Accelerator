SELECT
    t1.column1,
    t1.column2,
    t2.column3,
    t3.column4,
    COUNT(t4.column5) AS total_count,
    SUM(t4.amount) AS total_amount,
    AVG(t4.amount) AS avg_amount,
    MAX(t4.amount) AS max_amount,
    MIN(t4.amount) AS min_amount
FROM table1 t1

INNER JOIN table2 t2
    ON t1.id = t2.table1_id

LEFT JOIN table3 t3
    ON t2.id = t3.table2_id

RIGHT JOIN table4 t4
    ON t3.id = t4.table3_id

/* FULL OUTER JOIN (PostgreSQL/SQL Server/Oracle)
FULL OUTER JOIN table5 t5
    ON t1.id = t5.table1_id
*/

/* SELF JOIN */
INNER JOIN table1 t6
    ON t1.manager_id = t6.employee_id

WHERE
    t1.status = 'Active'
    AND t2.salary > 50000
    AND t3.city = 'Hyderabad'

GROUP BY
    t1.column1,
    t1.column2,
    t2.column3,
    t3.column4

HAVING
    COUNT(*) > 2
    AND SUM(t4.amount) > 10000

ORDER BY
    total_amount DESC,
    t1.column1;