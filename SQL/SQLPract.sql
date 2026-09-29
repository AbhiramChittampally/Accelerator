DELIMITER $$

CREATE PROCEDURE employee_bonus_report()

BEGIN

    DECLARE finished BOOLEAN DEFAULT FALSE;

    DECLARE v_name VARCHAR(50);

    DECLARE v_salary DECIMAL(10,2);

    DECLARE bonus DECIMAL(10,2);

    DECLARE emp_cursor CURSOR
    FOR
    SELECT ename,sal
    FROM emp;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND
    SET finished=TRUE;

    OPEN emp_cursor;

    read_loop: LOOP

        FETCH emp_cursor
        INTO
        v_name,
        v_salary;

        IF finished THEN
            LEAVE read_loop;
        END IF;

        IF v_salary<2000 THEN

            SET bonus=v_salary*0.10;

        ELSE

            SET bonus=v_salary*0.05;

        END IF;

        SELECT
        v_name,
        bonus;

    END LOOP;

    CLOSE emp_cursor;

END $$

DELIMITER ;

CALL employee_bonus_report();