/*
Problem : 
The corporate governance team wants to determine the reporting distance
(number of management layers) between each employee and top-level executive
management. A recursive CTE must trace the manager chain upwards, 
incrementing a depth counter until reaching the root (mgr IS NULL), 
displaying each employee's ID, name, assigned supervisor, and total management
distance.

use fs;
case=1
output=
empno	ename	mgr	steps_to_president
7839	KEVIN	NULL	0
7566	JONES	7839	1
7698	BLAKE	7839	1
7782	CLARK	7839	1
7499	ALLEN	7698	2
7521	ALLEN	7698	2
7654	MARTIN	7698	2
7788	SCOTT	7566	2
7844	KEVIN	7698	2
7900	JAMES	7698	2
7902	FORD	7566	2
7934	FORD	7782	2
7369	SMITH	7902	3
7876	KEVIN	7788	3
*/

USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    SELECT
        empno,
        ename,
        mgr,
        0 AS steps_to_president
    FROM emp
    WHERE mgr IS NULL

    UNION ALL

    SELECT
        e.empno,
        e.ename,
        e.mgr,
        eh.steps_to_president + 1
    FROM emp e
    JOIN EmployeeHierarchy eh
    ON e.mgr = eh.empno
)

SELECT
    empno,
    ename,
    mgr,
    steps_to_president
FROM EmployeeHierarchy;