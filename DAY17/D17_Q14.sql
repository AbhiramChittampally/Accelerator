/*
Problem Description:
The HR planning board requires a workspace distribution matrix to analyze operational units. Write a read-only SQL query to find the department number, 
department name, and the sum of salaries from the employee database. Filter the final rows using a multi-layered nested subquery 
inside the HAVING clause so that you only return organizational units whose total active employee headcount is strictly greater than 
the average employee headcount computed across all active departments in the enterprise.

case=1
output=
deptno	dname	total_department_payroll
20	Research	11825.00



*/
use fs;
select 
    d.deptno,
    d.dname,
    sum(e.sal) as total_department_payroll
from emp e
join dept d
on e.deptno=d.deptno
group by d.deptno,d.dname
having count(*) >
(
    select avg(emp_count)
    from
    (
        select
            
            count(*) as emp_count
            from emp
            group by deptno
    )as t
)