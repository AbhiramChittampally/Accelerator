/*

Topic: Recursive CTE Aggregation

Statement: Find all subordinates (direct and indirect) reporting to manager JONES (empno 7566).
case=1
output=
empno	ename	mgr
7788	SCOTT	7566
7902	FORD	7566
7369	SMITH	7902
7876	KEVIN	7788



*/
use fs;
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    
    SELECT
        empno,
        ename,
        mgr
    FROM emp
    WHERE mgr = 7566

    UNION ALL

    
    SELECT
        e.empno,
        e.ename,
        e.mgr
    FROM emp e
    JOIN EmployeeHierarchy eh
    ON e.mgr = eh.empno
)

SELECT
    empno,
    ename,
    mgr
FROM EmployeeHierarchy;