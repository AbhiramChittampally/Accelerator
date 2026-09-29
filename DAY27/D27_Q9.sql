/*
Problem : 
The recruitment department is evaluating hiring frequency across different job roles. 
For each job designation, determine the first person hired and the most recent person
 hired using FIRST_VALUE() and LAST_VALUE() window functions, then calculate the 
 total span in days between those two key hires.

case=1
output=
job	first_hired_emp	first_hire_date	latest_hired_emp	latest_hire_date	hiring_span_days
ANALYST	SCOTT	1996-03-05	FORD	1997-12-05	640
CLERK	SMITH	1993-06-13	JAMES	2000-06-23	2567
MANAGER	BLAKE	1992-06-11	JONES	1995-10-31	1237
PRESIDENT	KEVIN	1990-06-09	KEVIN	1990-06-09	0
SALESMAN	KEVIN	1995-06-04	MARTIN	1998-12-05	1280



*/
use fs;
WITH RoleHires AS (
    SELECT DISTINCT
        job,
        FIRST_VALUE(ename) OVER (
            PARTITION BY job ORDER BY hiredate ASC
        ) AS first_hired_emp,
        FIRST_VALUE(hiredate) OVER (
            PARTITION BY job ORDER BY hiredate ASC
        ) AS first_hire_date,
        LAST_VALUE(ename) OVER (
            PARTITION BY job ORDER BY hiredate ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS latest_hired_emp,
        LAST_VALUE(hiredate) OVER (
            PARTITION BY job ORDER BY hiredate ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS latest_hire_date
    FROM emp
)
SELECT 
    job,
    first_hired_emp,
    first_hire_date,
    latest_hired_emp,
    latest_hire_date,
    DATEDIFF(latest_hire_date, first_hire_date) AS hiring_span_days
FROM RoleHires;