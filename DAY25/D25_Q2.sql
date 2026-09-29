/*
The internal auditing team is standardizing escalation pathways across the entire 
workforce. For every employee listed in the company, they need to identify the 
ultimate executive supervisor at the very top of their reporting chain 
(where no higher manager exists). This mapping will establish clear chains 
of command from frontline staff directly up to executive management.

case=1
output=
original_emp	ultimate_boss
7839	KEVIN
7566	KEVIN
7698	KEVIN
7782	KEVIN
7499	KEVIN
7521	KEVIN
7654	KEVIN
7788	KEVIN
7844	KEVIN
7900	KEVIN
7902	KEVIN
7934	KEVIN
7369	KEVIN
7876	KEVIN



*/
use fs;
WITH RECURSIVE emph as
(
    select
        empno as original_emp,
        
        empno,
        ename,
        mgr
    from emp
    where mgr is null
    
    
    UNION ALL
    
    select 
        e.empno as original_emp,
        e.empno,
        eh.ename,
        e.mgr
    from emp e
    join  emph eh
    on e.mgr=eh.empno
)
SELECT
    original_emp,
    ename AS ultimate_boss
FROM emph
ORDER BY original_emp;