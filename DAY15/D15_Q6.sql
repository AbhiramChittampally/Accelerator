/*
Problem Description:
The reward and recognition committee is auditing the salary distribution across standard organizational tiers. 
Write an SQL query to find the salary grade numbers from the salgrade table along with the count of employees whose salaries fall into those respective grade brackets.
Only show grades that have more than 2 employees assigned to them, and sort the grades in ascending order.

case=1
output=
salary_grade	employee_count
1	8
2	10
3	7
4	6



*/
use fs;
select
    s.grade as salary_grade,
    count(*) as employee_count
from emp e
join salgrade s
on e.sal between s.losal and s.hisal
group by s.grade
having count(*)>2
order by salary_grade