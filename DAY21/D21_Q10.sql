/*
Problem 20: Recursive Staff Hierarchy Salary Projector (Topic 3.9)
Scenario: When auditing management costs, senior leadership needs a quick way to calculate the direct team cost under any given manager. 
Rather than pulling multi-row lists into spreadsheets to sum up salaries manually, they need a clean functional tool that can be used 
directly within a standard SELECT query.

The Task: Write a stored scalar function named fn_get_manager_team_cost that takes a manager_id integer as an input parameter. 
The function must look up that manager's personal salary, calculate the sum of the salaries of all employees who report directly to them (mgr = manager_id), 
and return the combined total cost as a single DECIMAL value.

Expected output=
-----------------
+-------+--------------+-----------------------+
| empno | manager_name | direct_reporting_cost |
+-------+--------------+-----------------------+
|  7566 | JONES        |              11305.92 |
|  7698 | BLAKE        |               9145.27 |
+-------+--------------+-----------------------+
2 rows in set (0.01 sec)


*/
use fs;

DELIMITER $$

CREATE FUNCTION fn_get_manager_team_cost
(
    p_manager_id INT
)

RETURNS DECIMAL(10,2)

DETERMINISTIC

BEGIN

    DECLARE v_manager_salary DECIMAL(10,2);

    DECLARE v_team_salary DECIMAL(10,2);

    DECLARE v_total_cost DECIMAL(10,2);

    SELECT sal
    INTO v_manager_salary
    FROM emp
    WHERE empno = p_manager_id;

    SELECT IFNULL(SUM(sal),0)
    INTO v_team_salary
    FROM emp
    WHERE mgr = p_manager_id;

    SET v_total_cost = v_manager_salary + v_team_salary;

    RETURN v_total_cost;

END $$

DELIMITER ;

SELECT
    empno,
    ename AS manager_name,
    fn_get_manager_team_cost(empno) AS direct_reporting_cost
FROM emp
WHERE empno IN (7566,7698);