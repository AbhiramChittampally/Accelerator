/*

Problem Description:
The executive leadership team wants to run a cost-center check on departments that employ highly paid analytical staff.
Write an SQL query to fetch the department name, location, and the total salary pool for employees within that department. 
Filter out any staff members whose salary is less than or equal to 1200 before grouping, and 
only show departments whose total combined salary pool for these qualified individuals is greater than 2500.

case=1
output=
department_name	location	qualified_salary_pool
Accounting	New York	5350.00
Sales	Chicago	5600.00
Research	Dallas	8975.00
Operations	Boston	6250.00

*/
use fs;
SELECT
    d.dname as department_name,
    d.location,
    sum(e.sal) as qualified_salary_pool
    
from emp e
join dept d
on e.deptno=d.deptno
where e.sal>1200
group by
d.dname,d.location
having sum(e.sal)>2500
