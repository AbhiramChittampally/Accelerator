/*
Problem 14: Restricting Sensitive Executive Salaries (Topic 3.10)
Scenario: Compliance teams require a data masking model that lets mid-level internal analysts audit organizational charts and payroll department assignments. However, strict data privacy regulations mandate that the precise financial earnings of high-level managers and executives remain classified. Analysts should see standard structural details but get masked values for senior salaries.

The Task: Construct a view named v_bias_free_salaries that joins emp and dept. It should project the employee's ID, name, designation, and department name. Incorporate conditional statement masking logic: if the employee's job title is explicitly 'MANAGER' or 'PRESIDENT', show their salary value as NULL (masked); otherwise, output their actual salary amount.
Expected output=
-----------------
+-------+---------------+-----------+--------+-----------------+-------------+
| empno | employee_name | job       | deptno | department_name | safe_salary |
+-------+---------------+-----------+--------+-----------------+-------------+
|  7782 | CLARK         | MANAGER   |     10 | Accounting      |        NULL |
|  7934 | MILLER        | CLERK     |     10 | Accounting      |     1826.41 |
|  7839 | KEVIN         | PRESIDENT |     40 | Operations      |        NULL |
+-------+---------------+-----------+--------+-----------------+-------------+
3 rows in set (0.01 sec)

*/
use fs;
DELIMITER $$

CREATE PROCEDURE sp_apply_department_raises()
BEGIN

    DECLARE v_deptno INT;
    DECLARE v_location VARCHAR(30);
    DECLARE done INT DEFAULT FALSE;

    DECLARE dept_cursor CURSOR FOR
        SELECT deptno, location
        FROM dept;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET done = TRUE;

    OPEN dept_cursor;

    department_loop: LOOP

        FETCH dept_cursor
        INTO v_deptno, v_location;

        IF done THEN
            LEAVE department_loop;
        END IF;

        IF v_location = 'New York' THEN

            UPDATE emp
            SET sal = sal * 1.12
            WHERE deptno = v_deptno;

        ELSEIF v_location = 'Dallas' THEN

            UPDATE emp
            SET sal = sal * 1.08
            WHERE deptno = v_deptno;

        ELSEIF v_location = 'Chicago' THEN

            UPDATE emp
            SET sal = sal * 1.05
            WHERE deptno = v_deptno;

        ELSE

            UPDATE emp
            SET sal = sal * 1.02
            WHERE deptno = v_deptno;

        END IF;

    END LOOP;

    CLOSE dept_cursor;

END $$

DELIMITER ;