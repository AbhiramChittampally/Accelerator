/*
Problem Description:
The HR system requires a comprehensive master list showing distinct employee tracks who are either working in top salary tiers (Grade 4 or 5) 
within a department located in 'Chicago', or are direct supervisors tracking subordinates who make less than 1500 base salary. 
Use structural subqueries combined with a UNION clause to bring these distinct operational groups together.

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
SELECT
    e.empno,
    e.ename,
    'High Salary Tier in Chicago' AS classification_reason
FROM emp e
JOIN dept d
ON e.deptno = d.deptno
JOIN salgrade s
ON e.sal BETWEEN s.losal AND s.hisal
WHERE d.location = 'Chicago'
AND s.grade IN (4,5)

UNION

SELECT DISTINCT
    e.empno,
    e.ename,
    'Manages Underpaid Subordinates' AS classification_reason
FROM emp e
JOIN emp s
ON e.empno = s.mgr
WHERE s.sal < 1500;