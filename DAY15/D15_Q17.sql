/*
Problem Description:
The HR department wants to audit regional branches that currently house active analytical or technical staff. 
Write an SQL query to extract the department number, department name, and regional location from the dept table. 
Use a correlated subquery with an EXISTS operator to filter for departments that have at least one employee working as an 'ANALYST'.

case=1
output=
deptno	dname	location
20	Research	Dallas



*/
use fs;
select
    d.deptno,
    d.dname,
    d.location
from dept d
where exists
(
    select *
    from emp e
    where e.deptno=d.deptno
    and e.job='ANALYST'
);