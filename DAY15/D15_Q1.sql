/*

Problem Description:
The HR director wants to assess the management overhead by analyzing salary distributions mapped to individual supervisors. 
Write an SQL query to fetch the manager's name and the average salary of the employees who report directly to them. 
Group the data by the manager's identity, and only include managers where the average salary of their subordinates exceeds 1500.
Sort the final output by average salary in descending order.

case=1
output=
manager_name	average_subordinate_salary
JONES	3000.000000
KEVIN	2758.333333

*/
use fs;
select
 m.ename as manager_name,
 avg(e.sal) as average_subordinate_salary
from emp e
join emp m
on e.mgr= m.empno
group by m.ename
having avg(e.sal)>1500
order by average_subordinate_salary desc;