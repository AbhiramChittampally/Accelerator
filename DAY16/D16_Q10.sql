/*
Problem Description:
The financial data analyst wants to understand the concentration of salary distribution inside each department. 
Write an SQL query to retrieve the employee name, department number, salary, and a calculated inline column called department_contribution_percentage. 
This column must use a correlated scalar subquery to find what percentage the individual's 
salary constitutes out of the total salary pool of their own department.

case=1
output=
ename	deptno	sal	department_contribution_percentage
CLARK	10	2450.00	45.79
ALLEN	10	1600.00	29.91
FORD	10	1300.00	24.30
SCOTT	20	3000.00	25.37
FORD	20	3000.00	25.37
JONES	20	2975.00	25.16
KEVIN	20	1100.00	9.30
JAMES	20	950.00	8.03
SMITH	20	800.00	6.77
BLAKE	30	2850.00	50.89
KEVIN	30	1500.00	26.79
ALLEN	30	1250.00	22.32
KEVIN	40	5000.00	80.00
MARTIN	40	1250.00	20.00



*/
use fs;
select 
    e.ename,
    e.deptno,
    e.sal,
    ROUND(
        (e.sal*100)/(
            select sum(e1.sal)
            from emp e1
            where e1.deptno=e.deptno
        ),2
    
    
    )as department_contribution_percentage
from emp e
order by deptno,e.sal Desc;
    
        