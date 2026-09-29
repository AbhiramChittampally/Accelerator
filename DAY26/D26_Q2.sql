/*
Problem : Second-In-Command Department Earners

The executive management team is creating a leadership succession program. 
As part of this initiative, they need to pinpoint the exact employees who hold 
the second-highest salary tier within each respective department. The query must 
properly account for tied top salaries so that true second-tier compensation earners
are retrieved.

case=1
output=
deptno	ename	sal
10	ALLEN	1600.00
20	JONES	2975.00
30	KEVIN	1500.00
40	MARTIN	1250.00



*/
use fs;
USE fs;

WITH DepartmentSalaryRank AS
(
    SELECT
        deptno,
        ename,
        sal,
        DENSE_RANK() OVER
        (
            PARTITION BY deptno
            ORDER BY sal DESC
        ) AS salary_rank
    FROM emp
)

SELECT
    deptno,
    ename,
    sal
FROM DepartmentSalaryRank
WHERE salary_rank = 2;