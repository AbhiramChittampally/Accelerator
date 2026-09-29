/*
Problem 11: Bulk Department Salary Hike Adjuster 
Scenario: HR needs to implement location-based cost-of-living salary
 increases across different business regions. Rather than updating 
 departments one by one manually, they need an automated database 
 process that loops through every department profile, checks its 
 operational location, and applies a distinct percentage raise.

The Task: Create a stored procedure named sp_apply_department_raises
that uses a database cursor to iterate through all departments.
It must apply a 12% raise for workers in 'New York', an 8% raise
for 'Dallas', a 5% raise for 'Chicago', and a 2% raise for all other locations.


Expected output=
-----------------
+-------+--------+--------+---------+
| empno | ename  | deptno | sal     |
+-------+--------+--------+---------+
|  7782 | CLARK  |     10 | 3442.07 |
|  7934 | MILLER |     10 | 1826.41 |
|  7369 | SMITH  |     20 | 1007.77 |
|  7566 | JONES  |     20 | 3747.64 |
+-------+--------+--------+---------+
4 rows in set (0.00 sec)
*/

DELIMITER $$

CREATE PROCEDURE sp_apply_department_raises()

BEGIN

    DECLARE finished BOOLEAN DEFAULT FALSE;

    DECLARE v_deptno INT;
    DECLARE v_location VARCHAR(50);

    DECLARE dept_cursor CURSOR
    FOR
        SELECT deptno, location
        FROM dept;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND
    SET finished = TRUE;

    OPEN dept_cursor;

    read_loop: LOOP

        FETCH dept_cursor
        INTO v_deptno, v_location;

        IF finished THEN
            LEAVE read_loop;
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