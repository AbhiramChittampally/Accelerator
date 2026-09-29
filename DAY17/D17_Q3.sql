/*
Problem Description:
The regional managers require a clean breakdown of the employee payroll to analyze individual salary weights against company baselines. 
Write a read-only SQL query to list each employee's name, their department number, and their exact salary from the emp table. 
Include a dynamically calculated column named company_max_salary using a scalar subquery to display the absolute highest salary alongside every employee row.

case=1
output=
employee_name	deptno	salary	company_max_salary
KEVIN	40	5000.00	5000.00
SCOTT	20	3000.00	5000.00
FORD	20	3000.00	5000.00
JONES	20	2975.00	5000.00
BLAKE	30	2850.00	5000.00
CLARK	10	2450.00	5000.00
ALLEN	10	1600.00	5000.00
KEVIN	30	1500.00	5000.00
FORD	10	1300.00	5000.00
ALLEN	30	1250.00	5000.00
MARTIN	40	1250.00	5000.00
KEVIN	20	1100.00	5000.00
JAMES	20	950.00	5000.00
SMITH	20	800.00	5000.00



*/
use fs;
select 
    ename as employee_name,
    deptno,
    sal as salary,
    (select max(sal) from emp) as company_max_salary
from emp
order by salary desc;