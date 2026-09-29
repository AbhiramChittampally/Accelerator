/*
Problem Description:
The financial control team wants to flag departments whose total payroll expenditure exceeds the average department-wise payroll across the company. 
Write an SQL query to find the department number and the sum of salaries for these high-expense departments. 
Group the records by department number and use a subquery inside the HAVING clause to benchmark against the overall average departmental total salary pool.

case=1
output=
deptno	total_payroll
20	11825.00



*/
use fs;
select
    deptno,
    sum(sal) as total_payroll
from emp e
group by deptno
having sum(sal)>
(
    select avg(total_salary)
    from
    (
        select sum(sal) as total_salary
        from emp
        group by deptno
    )as t
)