/*

Problem Description:
The operational audit team wants to review veterans working in key corporate locations to schedule long-service awards. 
Write an SQL query to retrieve the employee name, their hire date, their job description, and their department location. 
Filter the records to only display employees who were hired before January 1, 1997, and who are located in 'Dallas' or 'New York'. 
Sort the output so that the longest-serving employee appears first.



case=1
output=
employee_name	hiredate	job	location
CLARK	1993-05-14	MANAGER	New York
SMITH	1993-06-13	CLERK	Dallas
JONES	1995-10-31	MANAGER	Dallas
SCOTT	1996-03-05	ANALYST	Dallas

*/
use fs;
select
    e.ename as employee_name,
    e.hiredate,
    e.job,d.location
from emp e
join dept d
on d.deptno=e.deptno
where e.hiredate < '1997-01-01'
and d.location IN('Dallas','New York')

order by e.hiredate