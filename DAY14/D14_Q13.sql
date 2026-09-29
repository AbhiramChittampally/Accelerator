/*
Problem Description:
The organizational analysts want to check the distribution of specific clerical and administrative roles across standard corporate branches.
Write an SQL query to find the employee's name, their job, their department number, and the department name.
Filter the rows to include only those employees whose job role is exactly 'CLERK' and whose department is not located in 'New York'. 
Sort the results alphabetically by the employee's name.


case=1
output=
employee_name	job	deptno	department_name
JAMES	CLERK	20	Research
KEVIN	CLERK	20	Research
SMITH	CLERK	20	Research


*/
use fs;
select
    e.ename as employee_name,
    e.job,
    e.deptno,
    d.dname as department_name
from emp e
join dept d
on d.deptno=e.deptno
where e.job='CLERK' and d.location NOT IN('NEW YORK')
order by e.ename;