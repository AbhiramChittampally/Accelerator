/*
The internal audit department needs a unified exception report detailing extreme pay scenarios across corporate levels. 
Write a read-only SQL query that extracts the employee name, their supervisor's name, and their salary for employees 
who earn more money than their direct supervisor. Use a UNION ALL block to append another dataset matching high-earner outliers: 
employees whose base salary is strictly greater than the calculated average salary of all active managers combined.

case=1
output=
employee_name	manager_name	employee_salary
SCOTT	JONES	3000.00
FORD	JONES	3000.00
KEVIN	N/A - System Outlier	5000.00



*/
use fs;
select
    e.ename as employee_name,
    m.ename as manager_name,
    e.sal as employee_salary
from emp e
join emp m
on e.mgr=m.empno
where e.sal > m.sal

UNION ALL

select 
    e.ename as employee_name,
    'N/A - System Outlier' as manager_name,
    e.sal as employee_salary
from emp e
WHERE e.job <> 'MANAGER'
AND e.sal > 
(
    select avg(sal)
    from emp
    where job='MANAGER'
)
AND e.empno NOT IN
(
    SELECT e1.empno
    FROM emp e1
    JOIN emp m1
    ON e1.mgr = m1.empno
    WHERE e1.sal > m1.sal
);
