/*
Problem : 
The payroll department is auditing cumulative salary payouts as new employees 
are registered into department rosters. For every department, display employees 
sorted by employee ID alongside a running cumulative sum of department salary 
expenses up to that employee row.

case=1
output=
deptno	empno	ename	sal	dept_running_sal_total
10	7499	ALLEN	1600.00	1600.00
10	7782	CLARK	2450.00	4050.00
10	7934	FORD	1300.00	5350.00
20	7369	SMITH	800.00	800.00
20	7566	JONES	2975.00	3775.00
20	7788	SCOTT	3000.00	6775.00
20	7876	KEVIN	1100.00	7875.00
20	7900	JAMES	950.00	8825.00
20	7902	FORD	3000.00	11825.00
30	7521	ALLEN	1250.00	1250.00
30	7698	BLAKE	2850.00	4100.00
30	7844	KEVIN	1500.00	5600.00
40	7654	MARTIN	1250.00	1250.00
40	7839	KEVIN	5000.00	6250.00


*/
use fs;

SELECT
    deptno,
    empno,
    ename,
    sal,
    SUM(sal) OVER
    (
        PARTITION BY deptno
        ORDER BY empno
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS dept_running_sal_total
FROM emp;