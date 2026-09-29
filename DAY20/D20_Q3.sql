/*
Problem 3: Safe Income Calculator
----------------------------------
Scenario: Accounting needs to calculate the net income of employees.
 However, many employees have NULL values in their commission (comm)
  column, which breaks standard mathematical equations.

The Task: Write a stored scalar function named fn_get_net_income
that takes an employee's salary and commission as inputs, checks 
if the commission is NULL (replacing it with 0), and returns the 
combined net income.

Expected output:
---------------
+--------+---------+---------+------------+
| ename  | sal     | comm    | net_income |
+--------+---------+---------+------------+
| SMITH  |  800.00 |    0.00 |     800.00 |
| ALLEN  | 1600.00 |  300.00 |    1900.00 |
| WARD   | 1250.00 |  500.00 |    1750.00 |
| JONES  | 2975.00 |    NULL |    2975.00 |
| MARTIN | 1250.00 | 1400.00 |    2650.00 |
+--------+---------+---------+------------+

*/
USE fs;

DELIMITER //

CREATE FUNCTION fn_get_net_income(
    p_sal DECIMAL(10,2),
    p_comm DECIMAL(10,2)
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN p_sal + IFNULL(p_comm,0);
END //

DELIMITER ;

SELECT
    ename,
    sal,
    comm,
    fn_get_net_income(sal,comm) AS net_income
FROM emp;