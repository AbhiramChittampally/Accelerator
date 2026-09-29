/*
Topic: Bottom-Up Recursive CTE

Statement: Trace the direct management hierarchy starting from SMITH (empno 7369) up to the top-level executive (KEVIN). Display empno, ename, job, and mgr.


case=1
output=
empno	ename	job	mgr
7369	SMITH	CLERK	7902
7902	FORD	ANALYST	7566
7566	JONES	MANAGER	7839
7839	KEVIN	PRESIDENT	NULL



*/
use fs;
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    SELECT
        empno,
        ename,
        job,
        mgr
    FROM emp
    WHERE empno = 7369

    UNION ALL

    SELECT
        e.empno,
        e.ename,
        e.job,
        e.mgr
    FROM emp e
    JOIN EmployeeHierarchy eh
    ON e.empno = eh.mgr
)

SELECT
    empno,
    ename,
    job,
    mgr
FROM EmployeeHierarchy;