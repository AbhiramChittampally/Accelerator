/*
Problem Description:
The financial compensation auditor needs to verify leadership pay distributions inside organizational units.
Write a read-only SQL query to select the employee number, employee name, department number, salary, and corresponding salary grade 
tier from the emp and salgrade tables. The logic must use a correlated subquery to filter and return only those individuals
whose personal grade is strictly higher than the average salary grade tier computed across their specific department node

case=1
output=
empno	ename	deptno	sal	grade
7782	CLARK	10	2450.00	4
7499	ALLEN	10	1600.00	3
7782	CLARK	10	2450.00	3
7566	JONES	20	2975.00	4
7788	SCOTT	20	3000.00	4
7902	FORD	20	3000.00	4
7566	JONES	20	2975.00	3
7788	SCOTT	20	3000.00	3
7902	FORD	20	3000.00	3
7698	BLAKE	30	2850.00	4
7698	BLAKE	30	2850.00	3
7844	KEVIN	30	1500.00	3
7839	KEVIN	40	5000.00	6
7839	KEVIN	40	5000.00	5
7839	KEVIN	40	5000.00	4



*/
use fs;
select 
    e.empno,
    e.ename,
    e.deptno,
    e.sal,
    s.grade
from emp e
join salgrade s
on e.sal>=s.losal
where s.grade >
(
    SELECT AVG(s2.grade)
    FROM emp e2
    JOIN salgrade s2
    ON e2.sal >= s2.losal
    WHERE e2.deptno = e.deptno
)
ORDER BY
    e.deptno,
    s.grade desc,
    e.empno asc;