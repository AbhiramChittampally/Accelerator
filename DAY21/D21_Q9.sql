/*
Problem 19: Employee Salary Grade Heatmap View (Topic 3.10)
Scenario: The human resources and financial analytics teams require a comprehensive high-level dashboard to understand payroll distribution 
across the company. They need to see where corporate funds are concentrated by tracking the number of workers and the total combined 
payroll expenditures grouped by both geographical office locations and salary bands.

The Task: Construct a complex view matrix named v_payroll_grade_heatmap that joins the emp, dept, and salgrade tables. The system must evaluate 
which salary bracket an employee falls into using a conditional BETWEEN evaluation, and then group the results by the department location and salary grade.

Expected output=
-----------------
+-----------------+--------------+----------------+---------------------+
| office_location | salary_grade | employee_count | group_payroll_spend |
+-----------------+--------------+----------------+---------------------+
| Dallas          |            5 |              3 |            11305.92 |
| Boston          |            5 |              1 |             5306.04 |
| Chicago         |            3 |              3 |             4846.28 |
| New York        |            5 |              1 |             3442.07 |
| Chicago         |            5 |              1 |             3299.24 |
| New York        |            3 |              1 |             1826.41 |
| Dallas          |            2 |              1 |             1385.68 |
| New York        |            1 |              1 |             1200.00 |
| Chicago         |            1 |              1 |             1099.75 |
| Dallas          |            1 |              1 |             1007.77 |
+-----------------+--------------+----------------+---------------------+
10 rows in set (0.00 sec)
*/
DROP VIEW IF EXISTS v_payroll_grade_heatmap;

CREATE VIEW v_payroll_grade_heatmap AS

SELECT

    d.loc AS office_location,

    s.grade AS salary_grade,

    COUNT(e.empno) AS employee_count,

    SUM(e.sal) AS group_payroll_spend

FROM emp e

JOIN dept d
ON e.deptno = d.deptno

JOIN salgrade s
ON e.sal BETWEEN s.losal AND s.hisal

GROUP BY
    d.loc,
    s.grade;

SELECT *
FROM v_payroll_grade_heatmap;