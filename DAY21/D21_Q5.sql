/*
Problem 15: Recursive Manager Auto-Onboarding (Topic 3.9)
Scenario: HR needs to simplify onboarding for new hires. 
Rather than requiring staff to manually look up organizational 
structures to assign a line manager during initial profile setup,
the database system should automatically look up the department's
top earner and assign them as the direct manager.

The Task: Create a stored procedure named sp_onboard_employee 
that takes ename, job, sal, and deptno. Inside the engine routine,
query the emp table to look up whichever individual holds the highest
salary in that specific department, storing their empno into a 
variable. Finally, insert the new worker record using that variable
value to populate the manager ID (mgr) column.

Expected output=
-----------------
+-------+--------+------+--------+
| empno | ename  | mgr  | deptno |
+-------+--------+------+--------+
|  8001 | VIKRAM | 7782 |     10 |
+-------+--------+------+--------+
1 row in set (0.00 sec)
*/
DELIMITER $$

CREATE PROCEDURE sp_onboard_employee
(
    IN p_ename VARCHAR(50),
    IN p_job VARCHAR(30),
    IN p_sal DECIMAL(10,2),
    IN p_deptno INT
)
BEGIN

    DECLARE v_mgr INT;

    SELECT empno
    INTO v_mgr
    FROM emp
    WHERE deptno = p_deptno
    ORDER BY sal DESC
    LIMIT 1;

    INSERT INTO emp
    (
        empno,
        ename,
        job,
        mgr,
        hiredate,
        sal,
        comm,
        deptno
    )
    VALUES
    (
        8001,
        p_ename,
        p_job,
        v_mgr,
        CURDATE(),
        p_sal,
        NULL,
        p_deptno
    );

END $$

DELIMITER ;

CALL sp_onboard_employee
(
    'VIKRAM',
    'CLERK',
    1500,
    10
);

SELECT
    empno,
    ename,
    mgr,
    deptno
FROM emp
WHERE empno = 8001;