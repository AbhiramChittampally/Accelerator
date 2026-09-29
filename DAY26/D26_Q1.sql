/*
Problem: Comprehensive Salary Ranking Method Comparison

A data analytics instructor is preparing a SQL workshop demonstration on window 
ranking behavior. To illustrate how ties are handled differently, the system must 
rank all company employees by salary using ROW_NUMBER, RANK, and DENSE_RANK 
side-by-side. The goal is to visually demonstrate gap generation versus continuous 
integer ranking when identical salaries occur.

case=1
output=

ename	sal	row_num	rnk	dense_rnk
KEVIN	5000.00	1	1	1
SCOTT	3000.00	2	2	2
FORD	3000.00	3	2	2
JONES	2975.00	4	4	3
BLAKE	2850.00	5	5	4
CLARK	2450.00	6	6	5
ALLEN	1600.00	7	7	6
KEVIN	1500.00	8	8	7
FORD	1300.00	9	9	8
ALLEN	1250.00	10	10	9
MARTIN	1250.00	11	10	9
KEVIN	1100.00	12	12	10
JAMES	950.00	13	13	11
SMITH	800.00	14	14	12


*/
use fs;
USE fs;

SELECT
    ename,
    sal,
    ROW_NUMBER() OVER
    (
        ORDER BY sal DESC
    ) AS row_num,

    RANK() OVER
    (
        ORDER BY sal DESC
    ) AS rnk,

    DENSE_RANK() OVER
    (
        ORDER BY sal DESC
    ) AS dense_rnk

FROM emp;