SELECT
    e.employee_id,
    e.employee_name,
    e.salary,

    /* Scalar Subquery */
    (
        SELECT AVG(salary)
        FROM employee
    ) AS company_avg_salary

FROM employee e

/* Multi-row Subquery */
WHERE e.department_id IN
(
    SELECT department_id
    FROM department
    WHERE location='Hyderabad'
)

/* Correlated Subquery */
AND e.salary >
(
    SELECT AVG(e2.salary)
    FROM employee e2
    WHERE e.department_id = e2.department_id
)

/* EXISTS */
AND EXISTS
(
    SELECT 1
    FROM project p
    WHERE p.employee_id = e.employee_id
)

/* NOT EXISTS */
AND NOT EXISTS
(
    SELECT 1
    FROM blacklist b
    WHERE b.employee_id = e.employee_id
)

GROUP BY
    e.employee_id,
    e.employee_name,
    e.salary

HAVING
    SUM(e.salary) >
    (
        SELECT AVG(total_salary)
        FROM
        (
            SELECT SUM(salary) AS total_salary
            FROM employee
            GROUP BY department_id
        ) x
    )

ORDER BY
    e.salary DESC;