/*
Problem 16: Business Rule Enforcement Views (Topic 3.10)
Scenario: The regional operations head needs a specialized 
administrative portal to view and update records exclusively for 
Sales department employees (Department 30). However, the system must 
strictly prevent administrators from accidentally modifying data 
through this portal in a way that would cause the employee to drop 
out of their department scope.

The Task: Design an isolated view named v_sales_staff_exclusive 
pulling employee parameters from department 30. Append a view 
integrity constraint phrase (WITH CHECK OPTION) to explicitly prevent 
any raw table changes through the view layer that would violate the 
view's original filtering criteria.

Expected output=
-----------------
+-------+-------+----------+---------+--------+
| empno | ename | job      | sal     | deptno |
+-------+-------+----------+---------+--------+
|  7499 | ALLEN | SALESMAN | 1952.20 |     30 |
+-------+-------+----------+---------+--------+
1 row in set (0.00 sec)

*/
use fs;
-- Drop the view if it already exists
DROP VIEW IF EXISTS v_sales_staff_exclusive;

-- Create the view
CREATE VIEW v_sales_staff_exclusive AS

SELECT
    empno,
    ename,
    job,
    sal,
    deptno
FROM emp
WHERE deptno = 30

WITH CHECK OPTION;

-- Display the required record
SELECT
    empno,
    ename,
    job,
    sal,
    deptno
FROM v_sales_staff_exclusive
WHERE empno = 7499;