/*
Problem Description:
The payroll department wants to pinpoint specific regional departments where the cumulative operational costs (sum of all employee salaries) 
are entirely driven by staff members hired in the 1990s decade. Write an SQL query using nested subquery groups that evaluates 
the total salary of employees hired between 1990 and 1999 and matches it against the absolute department total payroll.

case=1
output=
deptno	dname
30	Sales
40	Operations


*/
use fs;
select
    d.deptno,
    d.dname
from dept d
where 
    (
        select sum(e.sal)
        from emp e
        where e.deptno =d.deptno
        and e.hiredate between '1990-01-01' AND '1999-12-31'
    )
    =
    (
        select sum(e.sal)
        from emp e
        where e.deptno=d.deptno
    )