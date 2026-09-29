/*
Problem : 
The compensation bench-marking group is creating salary range cards for every 
organizational unit. For every individual employee record, present their actual 
salary alongside the highest salary and lowest salary within their assigned 
department using window boundary frames.

case=1
output=
deptno	ename	sal	max_dept_sal	min_dept_sal
10	CLARK	2450.00	2450.00	1300.00
10	ALLEN	1600.00	2450.00	1300.00
10	FORD	1300.00	2450.00	1300.00
20	SCOTT	3000.00	3000.00	800.00
20	FORD	3000.00	3000.00	800.00
20	JONES	2975.00	3000.00	800.00
20	KEVIN	1100.00	3000.00	800.00
20	JAMES	950.00	3000.00	800.00
20	SMITH	800.00	3000.00	800.00
30	BLAKE	2850.00	2850.00	1250.00
30	KEVIN	1500.00	2850.00	1250.00
30	ALLEN	1250.00	2850.00	1250.00
40	KEVIN	5000.00	5000.00	1250.00
40	MARTIN	1250.00	5000.00	1250.00
*/
USE fs;

SELECT
    deptno,
    ename,
    sal,

    MAX(sal) OVER
    (
        PARTITION BY deptno
        order by sal DESC
        
    ) AS max_dept_sal,

    MIN(sal) OVER
    (
        PARTITION BY deptno
    ) AS min_dept_sal

FROM emp;