USE fs;

-- DAY14 Q1: Department salary analysis
SELECT 'DAY14 Q1: Department salary analysis' AS test;
SELECT
    d.dname AS department_name,
    SUM(e.sal) AS total_salary,
    AVG(e.sal) AS average_salary
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE d.location IN ('Dallas', 'Chicago')
GROUP BY d.deptno, d.dname
HAVING AVG(e.sal) > 1000
ORDER BY total_salary DESC;

-- DAY15 Q1: Manager salary analysis
SELECT 'DAY15 Q1: Manager salary analysis' AS test;
SELECT
    m.ename AS manager_name,
    AVG(e.sal) AS average_subordinate_salary
FROM emp e
JOIN emp m ON e.mgr = m.empno
GROUP BY m.ename
HAVING AVG(e.sal) > 1500
ORDER BY average_subordinate_salary DESC;

-- DAY16 Q1: High-value customers
SELECT 'DAY16 Q1: High-value customers' AS test;
SELECT DISTINCT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount >
(
    SELECT MAX(beverage_revenue)
    FROM
    (
        SELECT SUM(o2.total_amount) AS beverage_revenue
        FROM FoodItems f
        JOIN Orders o2 ON f.food_id = o2.food_id
        WHERE f.category = 'Beverages'
          AND o2.status = 'Delivered'
        GROUP BY f.food_id
    ) AS t
)
AND NOT EXISTS
(
    SELECT 1
    FROM Orders o3
    WHERE o3.customer_id = c.customer_id
      AND o3.status = 'Cancelled'
);

-- Verify all tables exist
SELECT 'Table verification' AS test;
SELECT
    TABLE_NAME,
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'fs'
ORDER BY TABLE_NAME;