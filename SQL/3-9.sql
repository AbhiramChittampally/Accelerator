DELIMITER $$

CREATE PROCEDURE procedure_name
(
    IN in_parameter datatype,
    OUT out_parameter datatype,
    INOUT inout_parameter datatype
)

BEGIN

    -----------------------------------------------------------------
    -- 1. DECLARE VARIABLES
    -----------------------------------------------------------------

    DECLARE finished BOOLEAN DEFAULT FALSE;

    DECLARE v_empno INT;
    DECLARE v_ename VARCHAR(50);
    DECLARE v_salary DECIMAL(10,2);
    DECLARE v_bonus DECIMAL(10,2);

    -----------------------------------------------------------------
    -- 2. DECLARE CURSOR
    -----------------------------------------------------------------

    DECLARE emp_cursor CURSOR
    FOR
    SELECT empno, ename, sal
    FROM emp;

    -----------------------------------------------------------------
    -- 3. DECLARE HANDLER
    -----------------------------------------------------------------

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND
    SET finished = TRUE;

    -----------------------------------------------------------------
    -- 4. NORMAL SQL
    -----------------------------------------------------------------

    SET v_bonus = 0;

    SELECT sal
    INTO v_salary
    FROM emp
    WHERE empno = in_parameter;

    -----------------------------------------------------------------
    -- 5. IF
    -----------------------------------------------------------------

    IF v_salary < 2000 THEN

        SET v_bonus = v_salary * 0.10;

    ELSEIF v_salary < 4000 THEN

        SET v_bonus = v_salary * 0.05;

    ELSE

        SET v_bonus = v_salary * 0.02;

    END IF;

    -----------------------------------------------------------------
    -- 6. CASE
    -----------------------------------------------------------------

    CASE

        WHEN v_bonus >= 300 THEN
            SELECT 'High Bonus';

        WHEN v_bonus >= 100 THEN
            SELECT 'Medium Bonus';

        ELSE
            SELECT 'Low Bonus';

    END CASE;

    -----------------------------------------------------------------
    -- 7. OPEN CURSOR
    -----------------------------------------------------------------

    OPEN emp_cursor;

    -----------------------------------------------------------------
    -- 8. LOOP
    -----------------------------------------------------------------

    read_loop : LOOP

        FETCH emp_cursor
        INTO
        v_empno,
        v_ename,
        v_salary;

        IF finished THEN
            LEAVE read_loop;
        END IF;

        -------------------------------------------------------------
        -- Business Logic
        -------------------------------------------------------------

        IF v_salary < 2000 THEN

            SET v_bonus = v_salary * 0.10;

        ELSE

            SET v_bonus = v_salary * 0.05;

        END IF;

        SELECT
        v_empno,
        v_ename,
        v_bonus;

    END LOOP;

    -----------------------------------------------------------------
    -- 9. CLOSE CURSOR
    -----------------------------------------------------------------

    CLOSE emp_cursor;

    -----------------------------------------------------------------
    -- 10. OUT PARAMETER
    -----------------------------------------------------------------

    SET out_parameter = v_bonus;

    -----------------------------------------------------------------
    -- 11. INOUT PARAMETER
    -----------------------------------------------------------------

    SET inout_parameter = inout_parameter + 100;

END$$

DELIMITER ; 













--/*===============================================================
--             SQL 3.9 MASTER STORED PROCEDURE BOILERPLATE
-- ===============================================================*/

-- CREATE PROCEDURE procedure_name
-- (
--     -- INPUT PARAMETERS
--     IN p_input1 INT,
--     IN p_input2 DECIMAL(10,2),

--     -- OUTPUT PARAMETERS
--     OUT p_status VARCHAR(100),

--     -- INPUT + OUTPUT
--     INOUT p_counter INT
-- )
-- BEGIN

--     /*===========================================================
--                         DECLARE VARIABLES
--     ===========================================================*/

--     DECLARE v_id INT;
--     DECLARE v_name VARCHAR(100);
--     DECLARE v_salary DECIMAL(10,2);
--     DECLARE v_bonus DECIMAL(10,2);
--     DECLARE v_total DECIMAL(10,2);
--     DECLARE v_grade CHAR(1);
--     DECLARE v_discount DECIMAL(10,2);
--     DECLARE v_done BOOLEAN DEFAULT FALSE;
--     DECLARE v_loop INT DEFAULT 1;

--     /*===========================================================
--                         CURSOR (OPTIONAL)
--     ===========================================================*/

--     DECLARE employee_cursor CURSOR FOR
--         SELECT employee_id, salary
--         FROM Employees;

--     /*===========================================================
--                         START TRANSACTION
--     ===========================================================*/

--     START TRANSACTION;

--     /*===========================================================
--                         READ DATA
--     ===========================================================*/

--     SELECT employee_id,
--            employee_name,
--            salary
--     INTO v_id,
--          v_name,
--          v_salary
--     FROM Employees
--     WHERE employee_id = p_input1;

--     /*===========================================================
--                         VALIDATION
--     ===========================================================*/

--     IF v_id IS NULL THEN

--         SET p_status = 'Employee Not Found';

--         ROLLBACK;

--     ELSE

--         /*=======================================================
--                             IF / ELSEIF / ELSE
--         =======================================================*/

--         IF v_salary >= 100000 THEN

--             SET v_bonus = 20000;

--         ELSEIF v_salary >= 70000 THEN

--             SET v_bonus = 10000;

--         ELSEIF v_salary >= 50000 THEN

--             SET v_bonus = 5000;

--         ELSE

--             SET v_bonus = 1000;

--         END IF;

--         /*=======================================================
--                             CASE
--         =======================================================*/

--         SET v_grade =
--         CASE

--             WHEN v_salary >= 100000 THEN 'A'

--             WHEN v_salary >= 70000 THEN 'B'

--             WHEN v_salary >= 50000 THEN 'C'

--             ELSE 'D'

--         END;

--         /*=======================================================
--                         CALCULATIONS
--         =======================================================*/

--         SET v_total = v_salary + v_bonus;

--         SET v_discount =
--         CASE

--             WHEN p_input2 >= 5000 THEN 15

--             WHEN p_input2 >= 2000 THEN 10

--             ELSE 5

--         END;

--         /*=======================================================
--                             INSERT
--         =======================================================*/

--         INSERT INTO BonusHistory
--         (
--             employee_id,
--             bonus,
--             total_salary
--         )
--         VALUES
--         (
--             v_id,
--             v_bonus,
--             v_total
--         );

--         /*=======================================================
--                             UPDATE
--         =======================================================*/

--         UPDATE Employees
--         SET salary = v_total
--         WHERE employee_id = v_id;

--         /*=======================================================
--                             DELETE
--         =======================================================*/

--         DELETE FROM TempTable
--         WHERE employee_id = v_id;

--     END IF;

--     /*===========================================================
--                         WHILE LOOP
--     ===========================================================*/

--     SET v_loop = 1;

--     WHILE v_loop <= 5 DO

--         SET v_loop = v_loop + 1;

--     END WHILE;

--     /*===========================================================
--                         REPEAT LOOP
--     ===========================================================*/

--     REPEAT

--         SET p_counter = p_counter + 1;

--     UNTIL p_counter >= 10

--     END REPEAT;

--     /*===========================================================
--                         GENERIC LOOP
--     ===========================================================*/

--     loop_label:
--     LOOP

--         IF p_counter >= 20 THEN
--             LEAVE loop_label;
--         END IF;

--         SET p_counter = p_counter + 1;

--         IF MOD(p_counter,2)=0 THEN
--             ITERATE loop_label;
--         END IF;

--     END LOOP;

--     /*===========================================================
--                         FOR LOOP (PostgreSQL Style)
--     ===========================================================*/

--     /*
--     FOR i IN 1..10 LOOP

--         -- statements

--     END LOOP;
--     */

--     /*===========================================================
--                             CURSOR
--     ===========================================================*/

--     /*
--     OPEN employee_cursor;

--     cursor_loop:
--     LOOP

--         FETCH employee_cursor
--         INTO v_id,
--              v_salary;

--         IF v_done THEN
--             LEAVE cursor_loop;
--         END IF;

--         UPDATE Employees
--         SET salary = salary + 1000
--         WHERE employee_id = v_id;

--     END LOOP;

--     CLOSE employee_cursor;
--     */

--     /*===========================================================
--                     RETURN OUTPUT PARAMETERS
--     ===========================================================*/

--     SET p_status = 'SUCCESS';

--     SET p_counter = p_counter + 1;

--     /*===========================================================
--                         COMMIT
--     ===========================================================*/

--     COMMIT;

-- END;


-- /*===============================================================
--                 MASTER STORED FUNCTION TEMPLATE
-- ===============================================================*/

-- CREATE FUNCTION function_name
-- (
--     p_value DECIMAL(10,2),
--     p_type VARCHAR(50)
-- )
-- RETURNS DECIMAL(10,2)

-- BEGIN

--     DECLARE v_result DECIMAL(10,2);

--     SET v_result =
--     CASE

--         WHEN p_type='Gold' THEN 20

--         WHEN p_type='Silver' THEN 10

--         WHEN p_type='Bronze' THEN 5

--         ELSE 0

--     END;

--     RETURN v_result;

-- END;


-- /*===============================================================
--                     EXECUTION
-- ===============================================================*/

-- CALL procedure_name(101,5000,@status,@counter);

-- SELECT @status,@counter;

-- SELECT function_name(5000,'Gold');