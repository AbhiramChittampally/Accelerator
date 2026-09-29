/*
Problem Description:
The HR talent acquisition division wants to look back at historical hiring trends to track expansion across regional nodes.
Write an SQL query to pull the employee name, job title, hire date, and department name for all workers who were hired after January 1, 1995.
Exclude anyone working out of the 'Boston' or 'Tempe' regional branches.
Sort the records chronologically by hire date.

case=1
output=
employee_name	job	hiredate	department_name
KEVIN	SALESMAN	1995-06-04	Sales
JONES	MANAGER	1995-10-31	Research
SCOTT	ANALYST	1996-03-05	Research
ALLEN	SALESMAN	1996-03-26	Sales
FORD	ANALYST	1997-12-05	Research
ALLEN	SALESMAN	1998-08-15	Accounting
KEVIN	CLERK	1999-06-04	Research
FORD	CLERK	2000-01-21	Accounting
JAMES	CLERK	2000-06-23	Research



*/
use fs;
select
    e.ename as employee_name,
    e.job,
    e.hiredate,
    d.dname as department_name
FROM emp e
join dept d
on e.deptno=d.deptno
where e.hiredate > '1995-01-01' and d.location not IN ('Boston','Tempe')
order by e.hiredate