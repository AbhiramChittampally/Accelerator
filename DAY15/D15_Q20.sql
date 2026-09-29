
/*
Problem Description:
The compensation committee wants to identify individual employees who are exceptionally well-paid relative to their specific peer job roles. 
Write an SQL query to find the employee number, name, job title, and salary from the emp table. 
Use a correlated subquery to evaluate and filter out individuals earning more than the average salary computed for their own respective job designation.


case=1
output=
empno	ename	job	sal
7499	ALLEN	SALESMAN	1600.00
7566	JONES	MANAGER	2975.00
7698	BLAKE	MANAGER	2850.00
7844	KEVIN	SALESMAN	1500.00
7876	KEVIN	CLERK	1100.00
7934	FORD	CLERK	1300.00



*/
use fs;
USE fs;

SELECT
    e.empno,
    e.ename,
    e.job,
    e.sal
FROM emp e
WHERE e.sal >
(
    SELECT AVG(e2.sal)
    FROM emp e2
    WHERE e2.job = e.job
);