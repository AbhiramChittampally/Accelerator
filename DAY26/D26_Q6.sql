/*
Problem : Departmental Compensation Tier Splitting
Scenario:
The Research Department (deptno 20) is restructuring bonus allocations based on 
salary distribution brackets. The compensation team wants to partition department 20 
staff evenly into 2 distinct compensation tiers (Tier 1 for upper bracket, 
Tier 2 for lower bracket) based on current earnings.

case=1
output=
empno	ename	sal	salary_tier
7788	SCOTT	3000.00	1
7902	FORD	3000.00	1
7566	JONES	2975.00	1
7876	KEVIN	1100.00	2
7900	JAMES	950.00	2
7369	SMITH	800.00	2



*/
use fs;
USE fs;

SELECT
    empno,
    ename,
    sal,
    NTILE(2) OVER
    (
        ORDER BY sal DESC
    ) AS salary_tier
FROM emp
WHERE deptno = 20;