/*
Problem Description:
The HR systems division requires a comprehensive analytics list showing distinct employee tracks who meet high-profile administrative conditions. 
The report needs to display employees who are either working in top salary tiers (Grade 4 or 5) within a department located in 'Chicago', 
or are direct supervisors tracking subordinates who make less than 1500 base salary. Use structural analytical subqueries combined with
a UNION clause to compile these distinct operational groups together.

case=1
output=
empno	ename	classification_reason
7698	BLAKE	High Salary Tier in Chicago
7902	FORD	Manages Underpaid Subordinates
7698	BLAKE	Manages Underpaid Subordinates
7788	SCOTT	Manages Underpaid Subordinates
7782	CLARK	Manages Underpaid Subordinates



*/
use fs;
select 
    e.empno,
    e.ename,
    'High Salary Tier in Chicago' as classification_reason
from emp e
where e.deptno in
(
    select d.deptno
    from dept d
    where d.location='Chicago'
)
and 
e.sal 
between
(
    select s.losal
    from salgrade s
    where s.grade= 4
    
)
and
(
    select s.hisal
    from salgrade s
    where s.grade=5
)

UNION

select
    e.empno,
    e.ename,
    'Manages Underpaid Subordinates' as classification_reason
from emp e
where e.empno in
(
    select mgr 
    from emp
    where sal <1500
)
