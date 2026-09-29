/*
Problem Description:
The HR internal compliance framework requires a complex cross-reference mapping that links employees to both their workspace location and their salary classification tier. 
Write an SQL query to find the employee's name, their department name, their work location, and their exact salary grade tier. 
Sort the entire output file primary by the department name alphabetically, and secondary by the salary grade in descending order.


case=1
output=
employee_name	department_name	location	salary_grade
CLARK	Accounting	New York	4
ALLEN	Accounting	New York	3
CLARK	Accounting	New York	3
CLARK	Accounting	New York	2
FORD	Accounting	New York	2
ALLEN	Accounting	New York	2
FORD	Accounting	New York	1
ALLEN	Accounting	New York	1
KEVIN	Operations	Boston	6
KEVIN	Operations	Boston	5
KEVIN	Operations	Boston	4
MARTIN	Operations	Boston	2
MARTIN	Operations	Boston	1
JONES	Research	Dallas	4
FORD	Research	Dallas	4
SCOTT	Research	Dallas	4
SCOTT	Research	Dallas	3
JONES	Research	Dallas	3
FORD	Research	Dallas	3
SCOTT	Research	Dallas	2
FORD	Research	Dallas	2
JONES	Research	Dallas	2
SMITH	Research	Dallas	1
KEVIN	Research	Dallas	1
JAMES	Research	Dallas	1
BLAKE	Sales	Chicago	4
BLAKE	Sales	Chicago	3
KEVIN	Sales	Chicago	3
ALLEN	Sales	Chicago	2
KEVIN	Sales	Chicago	2
BLAKE	Sales	Chicago	2
KEVIN	Sales	Chicago	1
ALLEN	Sales	Chicago	1



*/
use fs;
select
    e.ename as employee_name,
    d.dname as department_name,
    d.location,
    s.grade as salary_grade
from emp e
join dept d
on e.deptno=d.deptno
join salgrade s
on e.sal between s.losal and s.hisal
order by department_name , salary_grade desc
