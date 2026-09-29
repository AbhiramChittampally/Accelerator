/*
Problem Description:
The strategic analysts require a list of departments where the average employee salary is greater than the company-wide average salary, 
and which also employ at least one worker who ranks in the top earner brackets across the entire company. Write an SQL query using nested table derivatives,
multi-level scalar metrics, and an INTERSECT operator block to join these matching criteria groups cleanly.

case=1
output=
deptno
40



*/
use fs;
SELECT deptno
FROM emp
GROUP BY deptno
HAVING AVG(sal) >
(
    SELECT AVG(sal)
    FROM emp
)

INTERSECT

SELECT DISTINCT deptno
FROM emp
WHERE sal >=
(
    SELECT MIN(sal)
    FROM
    (
        SELECT sal
        FROM emp
        ORDER BY sal DESC
        LIMIT 3
    ) AS top_earners
);