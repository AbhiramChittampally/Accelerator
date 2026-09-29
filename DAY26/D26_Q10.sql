/*
Problem : Recent Role Onboarding Audit
Human Resources is performing a review of new team members onboarded into various
 positions across the enterprise. For every distinct job role, they need to list 
 the 2 most recently hired employees based on their official hire dates. 
 This ensures recent additions are appropriately scheduled for 90-day performance
 evaluations.

case=1
output=
empno	ename	job	hiredate
7902	FORD	ANALYST	1997-12-05
7788	SCOTT	ANALYST	1996-03-05
7900	JAMES	CLERK	2000-06-23
7934	FORD	CLERK	2000-01-21
7566	JONES	MANAGER	1995-10-31
7782	CLARK	MANAGER	1993-05-14
7839	KEVIN	PRESIDENT	1990-06-09
7654	MARTIN	SALESMAN	1998-12-05
7499	ALLEN	SALESMAN	1998-08-15



*/
use fs;
WITH HiresRanked AS (
    SELECT 
        empno, 
        ename, 
        job, 
        hiredate,
        ROW_NUMBER() OVER (
            PARTITION BY job 
            ORDER BY hiredate DESC
        ) AS rn
    FROM emp
)
SELECT empno, ename, job, hiredate
FROM HiresRanked
WHERE rn <= 2;