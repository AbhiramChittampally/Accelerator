WITH RECURSIVE cte_name AS
(
    ------------------------------------------------
    -- Anchor Query
    ------------------------------------------------

    SELECT
        columns,
        1 AS level
    FROM table_name
    WHERE starting_condition

    UNION ALL

    ------------------------------------------------
    -- Recursive Query
    ------------------------------------------------

    SELECT
        t.columns,
        c.level + 1
    FROM table_name t
    JOIN cte_name c
        ON recursive_condition
)

----------------------------------------------------
-- Main Query
----------------------------------------------------

SELECT *
FROM cte_name;