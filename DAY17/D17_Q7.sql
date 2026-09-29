/*
Problem Description:
An enterprise HR metrics developer needs to flag anomalous salaries where individuals out-earn the localized aggregate averages. 
Write a read-only SQL query to extract the employee name, department name, location, and salary from the emp and dept tables. 
The query must use nested subqueries to filter and return only those employees whose salary is strictly greater than the average 
salary of the entire department that holds the maximum aggregate payroll budget across the company.  

case=1
output=
employee_name	department_name	location	salary
JONES	Research	Dallas	2975.00
BLAKE	Sales	Chicago	2850.00
CLARK	Accounting	New York	2450.00
SCOTT	Research	Dallas	3000.00
KEVIN	Operations	Boston	5000.00
FORD	Research	Dallas	3000.00



*/
use fs;
select 
    e.ename as employee_name,
    d.dname as department_name,
    d.location,
    e.sal as salary
from emp e
join dept d
on e.deptno=d.deptno
where e.sal >
(
    select avg(sal)
    from emp
    where deptno=
    (
        select
            deptno
            
        from emp
        group by deptno
        order by sum(sal) desc
        limit 1
                            
    )
)