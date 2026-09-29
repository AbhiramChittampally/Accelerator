/* UNION */
SELECT
    id,
    name,
    salary
FROM employee

UNION

SELECT
    id,
    name,
    salary
FROM retired_employee

/* UNION ALL */
UNION ALL

SELECT
    id,
    name,
    salary
FROM contract_employee

/* INTERSECT */
INTERSECT

SELECT
    id,
    name,
    salary
FROM project_employee

/* EXCEPT (MINUS in Oracle) */
EXCEPT

SELECT
    id,
    name,
    salary
FROM terminated_employee

ORDER BY
    salary DESC,
    name;