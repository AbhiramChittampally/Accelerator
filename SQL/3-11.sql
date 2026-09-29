/*=========================================================
        SQL 3.11 MASTER BOILERPLATE
        Common Table Expressions (CTEs)
=========================================================*/

---------------------------------------------------------
-- SIMPLE CTE
---------------------------------------------------------
WITH employee_data AS
(
    SELECT *
    FROM emp
)
SELECT *
FROM employee_data;

---------------------------------------------------------
-- FILTERED CTE
---------------------------------------------------------
WITH it_employees AS
(
    SELECT *
    FROM emp
    WHERE deptno = 20
)
SELECT *
FROM it_employees;

---------------------------------------------------------
-- MULTIPLE CTEs
---------------------------------------------------------
WITH departments AS
(
    SELECT *
    FROM dept
),
employees AS
(
    SELECT *
    FROM emp
)
SELECT e.empno,
       e.ename,
       d.dname
FROM employees e
JOIN departments d
ON e.deptno = d.deptno;

---------------------------------------------------------
-- CHAINED CTEs
---------------------------------------------------------
WITH employees AS
(
    SELECT *
    FROM emp
),
high_salary AS
(
    SELECT *
    FROM employees
    WHERE sal > 3000
)
SELECT *
FROM high_salary;

---------------------------------------------------------
-- RECURSIVE CTE
---------------------------------------------------------
WITH RECURSIVE Numbers AS
(
    SELECT 1 AS n

    UNION ALL

    SELECT n + 1
    FROM Numbers
    WHERE n < 10
)
SELECT *
FROM Numbers;

---------------------------------------------------------
-- ORGANIZATION HIERARCHY
---------------------------------------------------------
WITH RECURSIVE OrgChart AS
(
    SELECT emp_id,
           employee,
           manager
    FROM Employees
    WHERE manager IS NULL

    UNION ALL

    SELECT e.emp_id,
           e.employee,
           e.manager
    FROM Employees e
    JOIN OrgChart o
      ON e.manager = o.emp_id
)
SELECT *
FROM OrgChart;







WITH

first_cte AS
(
    SELECT ...
    FROM ...
),

second_cte AS
(
    SELECT ...
    FROM first_cte
),

third_cte AS
(
    SELECT ...
    FROM second_cte
)

SELECT *
FROM third_cte;