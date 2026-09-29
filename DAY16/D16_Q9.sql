/*
Problem Description:
The executive committee needs an audit report containing the details of all employees who are either 
the absolute lowest earner in their respective department, or hold the maximum tenure (earliest hire date) 
across the whole company. Bring these two distinct granular groups together into one dataset matrix 
by joining them using a UNION ALL set operator.

case=1
output=
empno	ename	deptno	audit_tag
7369	SMITH	20	Lowest Department Earner
7521	ALLEN	30	Lowest Department Earner
7654	MARTIN	40	Lowest Department Earner
7934	FORD	10	Lowest Department Earner
7839	KEVIN	40	Company Senior Tenure



*/
use fs;
select
    e.empno,
    e.ename,
    e.deptno,
    'Lowest Department Earner' as audit_tag
from emp e
where e.sal=(
    select min(e1.sal)
    from emp e1
    where e1.deptno=e.deptno
)
union all

select
    e.empno,
    e.ename,
    e.deptno,
    'Company Senior Tenure' as audit_tag
from emp e
where e.hiredate=(
    select min(e1.hiredate)
    from emp e1
    
)