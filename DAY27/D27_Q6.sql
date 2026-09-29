/*
Problem : 
The HR rewards team is auditing salary dispersion across departments. 
They want to calculate the numeric gap between the maximum and minimum salary 
within each department, alongside the mid-tier salary using ROW_NUMBER() and COUNT() 
logic within a CTE to identify employees positioned closest to the departmental median.

case=1
output=
deptno	median_proxy_emp	sal	dept_sal_spread
10	ALLEN	1600.00	1150.00
20	KEVIN	1100.00	2200.00
30	KEVIN	1500.00	1600.00
40	MARTIN	1250.00	3750.00
*/
use fs;
WITH emp_rank AS
(
    SELECT
        deptno,
        ename,
        sal,
        ROW_NUMBER() OVER (
            PARTITION BY deptno
            ORDER BY sal
        ) AS rn,
        COUNT(*) OVER (
            PARTITION BY deptno
        ) AS cnt,
        MAX(sal) OVER (
            PARTITION BY deptno
        ) AS max_sal,
        MIN(sal) OVER (
            PARTITION BY deptno
        ) AS min_sal
    FROM emp
)

SELECT
    deptno,
    ename AS median_proxy_emp,
    sal,
    (max_sal - min_sal) AS dept_sal_spread
FROM emp_rank
WHERE rn = FLOOR((cnt + 1) / 2)
ORDER BY deptno;