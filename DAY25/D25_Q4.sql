/*
Window Functions (ROW_NUMBER, RANK, DENSE_RANK)
---------------------------------------------------
The compensation committee is performing an internal pay equity study across all
departments. They want to rank employees by salary within each department, ensuring 
tied salaries receive the exact same rank while keeping rank numbers strictly 
consecutive. This will highlight how individual compensation compares locally within 
each team.

case=1
output=
deptno	ename	sal	sal_rank
10	CLARK	2450.00	1
10	ALLEN	1600.00	2
10	FORD	1300.00	3
20	SCOTT	3000.00	1
20	FORD	3000.00	1
20	JONES	2975.00	2
20	KEVIN	1100.00	3
20	JAMES	950.00	4
20	SMITH	800.00	5
30	BLAKE	2850.00	1
30	KEVIN	1500.00	2
30	ALLEN	1250.00	3
40	KEVIN	5000.00	1
40	MARTIN	1250.00	2


*/
USE fs;

SELECT
    deptno,
    ename,
    sal,
    DENSE_RANK() OVER
    (
        PARTITION BY deptno
        ORDER BY sal DESC
    ) AS sal_rank
FROM emp;