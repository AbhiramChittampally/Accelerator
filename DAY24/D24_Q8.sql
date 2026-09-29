/*

Topic: Top-Down Hierarchy with Depth & Path Generation

Statement: Generate a full hierarchy starting from top management (mgr IS NULL), assigning organizational levels (1, 2, 3...) and displaying the management path string (e.g., KEVIN -> JONES -> FORD).

case=1
output=
empno	ename	lvl	path
7839	KEVIN	1	KEVIN
7566	JONES	2	KEVIN -> JONES
7698	BLAKE	2	KEVIN -> BLAKE
7782	CLARK	2	KEVIN -> CLARK
7499	ALLEN	3	KEVIN -> BLAKE -> ALLEN
7521	ALLEN	3	KEVIN -> BLAKE -> ALLEN
7654	MARTIN	3	KEVIN -> BLAKE -> MARTIN
7788	SCOTT	3	KEVIN -> JONES -> SCOTT
7844	KEVIN	3	KEVIN -> BLAKE -> KEVIN
7900	JAMES	3	KEVIN -> BLAKE -> JAMES
7902	FORD	3	KEVIN -> JONES -> FORD
7934	FORD	3	KEVIN -> CLARK -> FORD
7369	SMITH	4	KEVIN -> JONES -> FORD -> SMITH
7876	KEVIN	4	KEVIN -> JONES -> SCOTT -> KEVIN



*/
use fs;
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
   
    SELECT
        empno,
        ename,
        1 AS lvl,
        ename AS path
    FROM emp
    WHERE mgr IS NULL

    UNION ALL

    
    SELECT
        e.empno,
        e.ename,
        eh.lvl + 1,
        CONCAT(eh.path, ' -> ', e.ename)
    FROM emp e
    JOIN EmployeeHierarchy eh
    ON e.mgr = eh.empno
)

SELECT
    empno,
    ename,
    lvl,
    path
FROM EmployeeHierarchy;