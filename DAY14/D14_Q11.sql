/*
Problem Description:
The compensation committee needs to cross-reference employee salaries against standard grade brackets to analyze workforce distribution. 
Write an SQL query to retrieve the employee name, their job title, their exact salary, and the corresponding salary grade from the salgrade table. 
An employee's salary falls into a grade if it is between the low salary (losal) and high salary (hisal) boundaries.
Sort the results from the highest grade to the lowest grade.

case=1
output=
employee_name	job	salary	salary_grade
KEVIN	PRESIDENT	5000.00	6
KEVIN	PRESIDENT	5000.00	5
SCOTT	ANALYST	3000.00	4
FORD	ANALYST	3000.00	4
JONES	MANAGER	2975.00	4
CLARK	MANAGER	2450.00	4
KEVIN	PRESIDENT	5000.00	4
BLAKE	MANAGER	2850.00	4
KEVIN	SALESMAN	1500.00	3
SCOTT	ANALYST	3000.00	3
CLARK	MANAGER	2450.00	3
BLAKE	MANAGER	2850.00	3
JONES	MANAGER	2975.00	3
FORD	ANALYST	3000.00	3
ALLEN	SALESMAN	1600.00	3
CLARK	MANAGER	2450.00	2
KEVIN	SALESMAN	1500.00	2
FORD	ANALYST	3000.00	2
FORD	CLERK	1300.00	2
SCOTT	ANALYST	3000.00	2
BLAKE	MANAGER	2850.00	2
MARTIN	SALESMAN	1250.00	2
JONES	MANAGER	2975.00	2
ALLEN	SALESMAN	1250.00	2
ALLEN	SALESMAN	1600.00	2
SMITH	CLERK	800.00	1
MARTIN	SALESMAN	1250.00	1
KEVIN	SALESMAN	1500.00	1
KEVIN	CLERK	1100.00	1
JAMES	CLERK	950.00	1
ALLEN	SALESMAN	1250.00	1
ALLEN	SALESMAN	1600.00	1
FORD	CLERK	1300.00	1


*/
use fs;
select
    e.ename as employee_name,
    e.job,
    e.sal as salary,
    s.grade as salary_grade
from emp e
join salgrade s
on e.sal BETWEEN s.losal and s.hisal
order by s.grade desc

