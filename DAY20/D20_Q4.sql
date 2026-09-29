/*
Problem 4: Department Safety Verification Transfer 
---------------------------------------------------
Scenario: HR requires a process to transfer employees to 
new departments. If a user inputs a non-existent department number,
the database should block the query to prevent invalid database state.

The Task: Create a stored procedure named sp_safe_employee_transfer 
that takes an empno and a target deptno. It must verify if the 
department exists in the dept table. If it does, update the 
employee record; if not, raise a database warning.

Expected output:
---------------
+------------------------------------------------------+
| status_message                                       |
+------------------------------------------------------+
| Success: Employee 7369 transferred to Department 10 |
+------------------------------------------------------+

*/
CREATE PROCEDURE sp_safe_employee_transfer(
    IN p_empno INT,
    IN p_deptno INT
)
BEGIN
    IF EXISTS (
        SELECT *
        FROM dept
        WHERE deptno = p_deptno
    ) THEN
        UPDATE emp
        SET deptno = p_deptno
        WHERE empno = p_empno;

        SELECT CONCAT(
            'Success: Employee ',
            p_empno,
            ' transferred to Department ',
            p_deptno
        ) AS status_message;
    ELSE
        SIGNAL SQLSTATE '01000'
        SET MESSAGE_TEXT = 'Department does not exist';
    END IF;
END