# SQL Comprehensive Revision Guide (Day 14 – Day 17)

---

## 🎯 Master Exam Cheat Sheet (Days 14–17)

### 1. Joins Mastery Cheat Sheet
| Join Type | Syntax | Purpose / Behavior | Common Test Pattern |
| :--- | :--- | :--- | :--- |
| **`INNER JOIN`** | `FROM A JOIN B ON A.id = B.id` | Returns only rows where matching keys exist in both tables. | Matching orders to customers or food items. |
| **`LEFT JOIN`** | `FROM A LEFT JOIN B ON A.id = B.id` | Retains all rows from table A; fills columns from table B with `NULL` if no match. | Showing customers with 0 orders (`COUNT(B.id)`), or items never delivered. |
| **`SELF JOIN`** | `FROM emp e JOIN emp m ON e.mgr = m.empno` | Joins a table to itself using aliases to resolve hierarchical relationships. | Employee-to-Manager reporting, comparing coworkers. |
| **Non-Equi Join** | `FROM emp e JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal` | Joins tables on an inequality or range condition rather than equality `=`. | Mapping salaries into grades or tax brackets. |

---

### 2. `WHERE` vs `HAVING`
- **`WHERE`**: Filters **individual source rows BEFORE aggregation**. Cannot contain aggregate functions (e.g. `WHERE SUM(sal) > 1000` is illegal).
- **`HAVING`**: Filters **grouped summary rows AFTER aggregation**. Operates on aggregate expressions (e.g. `HAVING COUNT(*) > 2`, `HAVING SUM(sal) > 2500`).
- **Subqueries in `HAVING`**: Used to benchmark a group's aggregate against a company-wide or outer-group metric:
  ```sql
  HAVING SUM(sal) > (SELECT AVG(total_sal) FROM (SELECT SUM(sal) AS total_sal FROM emp GROUP BY deptno) AS t)
  ```

---

### 3. Subquery Types & Execution Flow
| Subquery Type | Definition | Placement | Correlated? | Performance Note |
| :--- | :--- | :--- | :---: | :--- |
| **Scalar Subquery** | Returns strictly 1 row and 1 column. | `SELECT`, `WHERE`, `HAVING` | Can be either | Replaces a constant value (e.g. `WHERE sal > (SELECT AVG(sal) FROM emp)`). |
| **Uncorrelated Subquery** | Independent query; runs **once** for the entire statement. | `WHERE`, `FROM`, `HAVING` | **No** | Very fast. Inner query executes first, result fed to outer. |
| **Correlated Subquery** | References column(s) from outer query row (e.g. `WHERE e2.deptno = e.deptno`). Runs **once per candidate outer row**. | `SELECT`, `WHERE`, `HAVING` | **Yes** | Acts like a nested loop. Crucial for peer comparisons. |
| **Derived Table (Inline Subquery)** | Subquery placed in `FROM` clause; must be aliased (`AS t`). | `FROM` / `JOIN` | No | Creates a temporary virtual table on the fly. |

---

### 4. `EXISTS` vs `IN` vs `NOT IN` vs `NOT EXISTS`
- **`EXISTS`**: Tests for presence of rows. Returns `TRUE` the instant 1 row matches. Very fast with correlated subqueries (`SELECT 1 FROM ... WHERE ...`).
- **`NOT EXISTS`**: Safe against `NULL`s. Best for finding unmatched entities.
- **⚠️ The `NOT IN` NULL Trap**:
  If the subquery inside `NOT IN (SELECT col FROM ...)` returns even a single `NULL` value, the entire `NOT IN` evaluates to `UNKNOWN`, and the outer query returns **0 rows**!
  - **Rule:** Always filter out `NULL`s if using `NOT IN`:
    ```sql
    WHERE customer_id NOT IN (SELECT customer_id FROM Orders WHERE customer_id IS NOT NULL)
    ```

---

### 5. Set Operators Comparison
All set operators require:
1. The same number of columns in each `SELECT`.
2. Compatible data types in corresponding columns.

| Operator | Action | Duplicate Handling |
| :--- | :--- | :--- |
| **`UNION`** | Combines result sets of two queries | **Removes duplicates** (performs sort/hash deduplication) |
| **`UNION ALL`** | Combines result sets of two queries | **Keeps all duplicates** (fastest, no sorting) |
| **`INTERSECT`** | Returns only rows present in **both** query results | Retains distinct common rows |
| **`EXCEPT`** | Returns rows from Query 1 that are **not** present in Query 2 | Removes matches and duplicates |

---
---

# DAY 17 — Advanced Subqueries, Correlated Filters & Set Operators

### [D17_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q1.sql) — Uncorrelated Scalar Subquery in WHERE
```sql
USE fs;

SELECT order_id, customer_id, food_id, quantity
FROM Orders 
WHERE quantity > (SELECT AVG(quantity) FROM Orders)
ORDER BY quantity DESC, order_id ASC;
```
- **Concept:** Uncorrelated subquery calculates company-wide average quantity once. Outer query filters orders exceeding that average.

---

### [D17_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q2.sql) — Matching Categories with INTERSECT
```sql
USE fs;

SELECT DISTINCT f.category
FROM FoodItems f
WHERE f.price > 150

INTERSECT

SELECT f.category
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id;
```
- **Concept:** `INTERSECT` operator finds common distinct categories meeting both requirements: having premium items ($> 150$) AND having active sales transactions.

---

### [D17_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q3.sql) — Scalar Subquery in SELECT Projection
```sql
USE fs;

SELECT 
    ename AS employee_name,
    deptno,
    sal AS salary,
    (SELECT MAX(sal) FROM emp) AS company_max_salary
FROM emp
ORDER BY salary DESC;
```
- **Concept:** Scalar subquery `(SELECT MAX(sal) FROM emp)` executes once and projects the company-wide maximum salary as an inline column alongside every single employee row.

---

### [D17_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q4.sql) — Correlated EXISTS for Management Presence
```sql
USE fs;

SELECT d.deptno, d.dname
FROM dept d
WHERE EXISTS (
    SELECT 1
    FROM emp e
    WHERE e.deptno = d.deptno
      AND e.job = 'MANAGER'
);
```
- **Concept:** `EXISTS` tests whether at least one matching row exists for that department. It stops evaluating as soon as the first match is found (short-circuit evaluation).

---

### [D17_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q5.sql) — Correlated Subquery in HAVING (City-Level Benchmark)
```sql
USE fs;

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.address AS city_address,
    SUM(o.total_amount) AS total_customer_lifetime_spend
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.address
HAVING SUM(o.total_amount) > (
    SELECT AVG(o2.total_amount)
    FROM Customers c2
    JOIN Orders o2 ON c2.customer_id = o2.customer_id
    WHERE c2.address = c.address
)
ORDER BY total_customer_lifetime_spend DESC;
```
- **Concept:** Correlated subquery inside `HAVING`.
- **Key Takeaway:** Filters each customer's lifetime total against the historical average transaction size of customers living in that *same city* (`WHERE c2.address = c.address`).

---

### [D17_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q6.sql) — UNION for High-Engagement Segmentation
```sql
USE fs;

SELECT c.customer_id, c.first_name, c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.quantity > 3

UNION

SELECT c.customer_id, c.first_name, c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 300;
```
- **Concept:** Combines two criteria (large quantity OR large total amount) into a single unified list. `UNION` automatically eliminates duplicate customer rows.

---

### [D17_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q7.sql) — Multi-Tier Nested Subquery
```sql
USE fs;

SELECT 
    e.ename AS employee_name,
    d.dname AS department_name,
    d.location,
    e.sal AS salary
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.sal > (
    SELECT AVG(sal)
    FROM emp
    WHERE deptno = (
        SELECT deptno
        FROM emp
        GROUP BY deptno
        ORDER BY SUM(sal) DESC
        LIMIT 1
    )
);
```
- **Concept:** 3-tier subquery nesting:
  1. Innermost subquery finds the `deptno` with the highest total salary expenditure (`ORDER BY SUM(sal) DESC LIMIT 1`).
  2. Middle subquery computes the average salary of that specific department.
  3. Outer query returns employees earning more than that average.

---

### [D17_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q8.sql) — Correlated Subquery on Non-Equi Joins
```sql
USE fs;

SELECT 
    e.empno,
    e.ename,
    e.deptno,
    e.sal,
    s.grade
FROM emp e
JOIN salgrade s ON e.sal >= s.losal
WHERE s.grade > (
    SELECT AVG(s2.grade)
    FROM emp e2
    JOIN salgrade s2 ON e2.sal >= s2.losal
    WHERE e2.deptno = e.deptno
)
ORDER BY e.deptno, s.grade DESC, e.empno ASC;
```
- **Concept:** Evaluates salary grade tiers against the department average grade tier using a correlated subquery linked via `e2.deptno = e.deptno`.

---

### [D17_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q9.sql) — UNION ALL with Negative Match Exclusion
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    m.ename AS manager_name,
    e.sal AS employee_salary
FROM emp e
JOIN emp m ON e.mgr = m.empno
WHERE e.sal > m.sal

UNION ALL

SELECT 
    e.ename AS employee_name,
    'N/A - System Outlier' AS manager_name,
    e.sal AS employee_salary
FROM emp e
WHERE e.job <> 'MANAGER'
  AND e.sal > (SELECT AVG(sal) FROM emp WHERE job = 'MANAGER')
  AND e.empno NOT IN (
      SELECT e1.empno
      FROM emp e1
      JOIN emp m1 ON e1.mgr = m1.empno
      WHERE e1.sal > m1.sal
  );
```
- **Concept:** Combines two distinct datasets with `UNION ALL`:
  1. Employees earning more than their direct manager.
  2. Non-managers earning more than the average manager salary who were NOT already captured in the first block (using `NOT IN`).

---

### [D17_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q10.sql) — NOT EXISTS for Unmatched Records
```sql
USE fs;

SELECT f.food_id, f.name, f.category, f.price
FROM FoodItems f
WHERE NOT EXISTS (
    SELECT 1
    FROM Orders o
    WHERE o.food_id = f.food_id
      AND o.status = 'Delivered'
);
```
- **Concept:** Identifies catalog items with zero completed deliveries. `NOT EXISTS` safely verifies that no matching row exists in `Orders` with `status = 'Delivered'`.

---

### [D17_Q11.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q11.sql) — Inline Derived Table Join
```sql
USE fs;

SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount,
    t.total_customer_orders
FROM Orders o
JOIN (
    SELECT customer_id, COUNT(*) AS total_customer_orders
    FROM Orders
    GROUP BY customer_id
) AS t ON o.customer_id = t.customer_id
ORDER BY o.order_id;
```
- **Concept:** Pre-aggregating data in an inline derived table (`FROM (...) AS t`) and joining it back to individual order rows to display customer historical totals on every transaction.

---

### [D17_Q12.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q12.sql) — Correlated Spending Spike Outliers
```sql
USE fs;

SELECT o.order_id, o.customer_id, o.food_id, o.total_amount
FROM Orders o
WHERE o.total_amount > (
    2 * (
        SELECT AVG(o2.total_amount)
        FROM Orders o2
        WHERE o2.customer_id = o.customer_id
    )
);
```
- **Concept:** Detects orders where the amount is strictly $> 2 \times$ that customer's personal average order amount using a correlated subquery linked on `o2.customer_id = o.customer_id`.

---

### [D17_Q13.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q13.sql) — Correlated Subquery in HAVING for Market Share
```sql
USE fs;

SELECT 
    f.name AS food_item_name,
    f.category,
    SUM(o.total_amount) AS item_total_revenue
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.total_amount) > (
    0.35 * (
        SELECT SUM(o2.total_amount)
        FROM FoodItems f2
        JOIN Orders o2 ON f2.food_id = o2.food_id
        WHERE f2.category = f.category
    )
)
ORDER BY item_total_revenue DESC;
```
- **Concept:** Filters aggregated items where item revenue exceeds 35% of total category revenue. The correlated subquery sums all revenues for the outer row's category (`f2.category = f.category`).

---

### [D17_Q14.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q14.sql) — Nested Subquery in HAVING (Headcount > Average Headcount)
```sql
USE fs;

SELECT 
    d.deptno,
    d.dname,
    SUM(e.sal) AS total_department_payroll
FROM emp e
JOIN dept d ON e.deptno = d.deptno
GROUP BY d.deptno, d.dname
HAVING COUNT(*) > (
    SELECT AVG(emp_count)
    FROM (
        SELECT COUNT(*) AS emp_count
        FROM emp
        GROUP BY deptno
    ) AS t
);
```
- **Concept:** The subquery inside `HAVING` computes the average department size across the company by taking `AVG(emp_count)` from an inline derived table `(SELECT COUNT(*) FROM emp GROUP BY deptno) AS t`.

---

### [D17_Q15.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY17/D17_Q15.sql) — Correlated Subquery in HAVING (Category Benchmark)
```sql
USE fs;

SELECT
    f.name AS food_item_name,
    f.category,
    SUM(o.quantity) AS total_quantity_sold
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE o.status = 'Delivered'
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.quantity) > (
    SELECT AVG(o2.quantity)
    FROM FoodItems f2
    JOIN Orders o2 ON f2.food_id = o2.food_id
    WHERE f2.category = f.category
      AND o2.status = 'Delivered'
)
ORDER BY total_quantity_sold DESC;
```
- **Concept:** Filters delivered food items whose cumulative quantity sold exceeds the average individual order quantity in that same category.

---
---

# DAY 16 — Advanced Correlated Queries, Ratios & Set Combinations

### [D16_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q1.sql) — Outlier Spenders with Clean Order History
```sql
USE fs;

SELECT DISTINCT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > (
    SELECT MAX(beverage_revenue)
    FROM (
        SELECT SUM(o2.total_amount) AS beverage_revenue
        FROM FoodItems f
        JOIN Orders o2 ON f.food_id = o2.food_id
        WHERE f.category = 'Beverages' AND o2.status = 'Delivered'
        GROUP BY f.food_id
    ) AS t
)
AND NOT EXISTS (
    SELECT 1
    FROM Orders o3
    WHERE o3.customer_id = c.customer_id AND o3.status = 'Cancelled'
);
```
- **Concept:** Combines a benchmark subquery against peak beverage revenue with `NOT EXISTS` to exclude customers with any cancelled orders.

---

### [D16_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q2.sql) — Matching Department Criteria via INTERSECT
```sql
USE fs;

SELECT deptno
FROM emp
GROUP BY deptno
HAVING AVG(sal) > (SELECT AVG(sal) FROM emp)

INTERSECT

SELECT DISTINCT deptno
FROM emp
WHERE sal >= (
    SELECT MIN(sal)
    FROM (
        SELECT sal
        FROM emp
        ORDER BY sal DESC
        LIMIT 3
    ) AS top_earners
);
```
- **Concept:** `INTERSECT` finds departments meeting two independent criteria:
  1. Department average salary $>$ company average salary.
  2. Department employs at least one top-3 company earner.

---

### [D16_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q3.sql) — High-Value Order Filtering
```sql
USE fs;

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    o.order_id,
    o.total_amount
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > (SELECT AVG(total_amount) FROM Orders)
ORDER BY o.total_amount DESC;
```
- **Concept:** Standard join with an uncorrelated scalar subquery filtering transactions above overall average spend.

---

### [D16_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q4.sql) — Categorized Employee Tracks with UNION
```sql
USE fs;

SELECT
    e.empno,
    e.ename,
    'High Salary Tier in Chicago' AS classification_reason
FROM emp e
JOIN dept d ON e.deptno = d.deptno
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
WHERE d.location = 'Chicago' AND s.grade IN (4, 5)

UNION

SELECT DISTINCT
    e.empno,
    e.ename,
    'Manages Underpaid Subordinates' AS classification_reason
FROM emp e
JOIN emp s ON e.empno = s.mgr
WHERE s.sal < 1500;
```
- **Concept:** Using `UNION` with hardcoded string literals (`'High Salary Tier in Chicago'`) to label and merge disparate business criteria.

---

### [D16_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q5.sql) — Multi-Condition Join Filtering
```sql
USE fs;

SELECT
    o.order_id,
    c.first_name,
    f.name AS food_item_name,
    o.quantity,
    o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.quantity > 1 AND o.total_amount > 200
ORDER BY o.total_amount DESC;
```
- **Concept:** Multi-table join across 3 tables filtered by both quantity and total amount thresholds.

---

### [D16_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q6.sql) — Most Expensive Item per Category (Correlated Subquery)
```sql
USE fs;

SELECT f.food_id, f.name, f.category, f.price
FROM FoodItems f
WHERE f.price = (
    SELECT MAX(f2.price)
    FROM FoodItems f2
    WHERE f2.category = f.category
);
```
- **Concept:** Classic SQL pattern to find the record with the maximum value per group without window functions. Correlated subquery checks `MAX(f2.price)` within the same category (`f2.category = f.category`).

---

### [D16_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q7.sql) — Customer Profile Segmentation (INTERSECT + EXCEPT)
```sql
USE fs;

-- Ordered Chicken Biryani
SELECT customer_id FROM Orders
WHERE food_id = (SELECT food_id FROM FoodItems WHERE name = 'Chicken Biryani')

INTERSECT

-- AND ordered Mango Lassi
SELECT customer_id FROM Orders
WHERE food_id = (SELECT food_id FROM FoodItems WHERE name = 'Mango Lassi')

EXCEPT

-- BUT NEVER ordered Samosa
SELECT customer_id FROM Orders
WHERE food_id = (SELECT food_id FROM FoodItems WHERE name = 'Samosa');
```
- **Concept:** Complex audience segmentation using Set Operators:
  - `INTERSECT` enforces that the customer ordered BOTH Biryani AND Lassi.
  - `EXCEPT` completely excludes any customer who ordered Samosa.

---

### [D16_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q8.sql) — Comparing Department Sub-Totals with Outer WHERE
```sql
USE fs;

SELECT d.deptno, d.dname
FROM dept d
WHERE (
    SELECT SUM(e.sal)
    FROM emp e
    WHERE e.deptno = d.deptno AND e.hiredate BETWEEN '1990-01-01' AND '1999-12-31'
) = (
    SELECT SUM(e.sal)
    FROM emp e
    WHERE e.deptno = d.deptno
);
```
- **Concept:** Detects departments where 100% of the payroll goes to employees hired in the 1990s. Compares the 1990s payroll subquery directly to the total department payroll subquery.

---

### [D16_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q9.sql) — UNION ALL for Distinct Operational Audits
```sql
USE fs;

-- Lowest earner in department
SELECT e.empno, e.ename, e.deptno, 'Lowest Department Earner' AS audit_tag
FROM emp e
WHERE e.sal = (SELECT MIN(e1.sal) FROM emp e1 WHERE e1.deptno = e.deptno)

UNION ALL

-- Longest company tenure
SELECT e.empno, e.ename, e.deptno, 'Company Senior Tenure' AS audit_tag
FROM emp e
WHERE e.hiredate = (SELECT MIN(e1.hiredate) FROM emp e1);
```
- **Concept:** Combines department-level minima with company-level extrema using `UNION ALL`.

---

### [D16_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q10.sql) — Correlated Scalar Subquery for Percentage Contribution
```sql
USE fs;

SELECT 
    e.ename,
    e.deptno,
    e.sal,
    ROUND(
        (e.sal * 100.0) / (
            SELECT SUM(e1.sal)
            FROM emp e1
            WHERE e1.deptno = e.deptno
        ), 
        2
    ) AS department_contribution_percentage
FROM emp e
ORDER BY deptno, e.sal DESC;
```
- **Concept:** Scalar correlated subquery embedded directly inside the `SELECT` calculation to calculate an individual's share of their department's total salary pool.

---

### [D16_Q11.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q11.sql) — Correlated Subquery in HAVING vs Derived Benchmark
```sql
USE fs;

SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    SUM(o.total_amount) AS total_lifetime_spending
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING (
    SELECT SUM(o1.total_amount)
    FROM Orders o1
    JOIN FoodItems f ON o1.food_id = f.food_id
    WHERE o1.customer_id = c.customer_id AND f.category = 'Breakfast'
) > (
    SELECT AVG(breakfast_total)
    FROM (
        SELECT SUM(o2.total_amount) AS breakfast_total
        FROM Orders o2
        JOIN FoodItems f1 ON o2.food_id = f1.food_id
        WHERE f1.category = 'Breakfast'
        GROUP BY o2.customer_id
    ) AS t
);
```
- **Concept:** Deeply nested `HAVING` condition: compares a customer's personal Breakfast spend to the platform-wide average customer Breakfast spend.

---

### [D16_Q12.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q12.sql) — UNION of Department Location and Supervisor Checks
```sql
USE fs;

SELECT e.empno, e.ename, 'High Salary Tier in Chicago' AS classification_reason
FROM emp e
WHERE e.deptno IN (SELECT d.deptno FROM dept d WHERE d.location = 'Chicago')
  AND e.sal BETWEEN (SELECT s.losal FROM salgrade s WHERE s.grade = 4)
                AND (SELECT s.hisal FROM salgrade s WHERE s.grade = 5)

UNION

SELECT e.empno, e.ename, 'Manages Underpaid Subordinates' AS classification_reason
FROM emp e
WHERE e.empno IN (SELECT mgr FROM emp WHERE sal < 1500);
```
- **Concept:** Subqueries used inside `WHERE IN (...)` combined with `UNION` to merge two independent employee cohorts.

---

### [D16_Q13.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q13.sql) — INTERSECT with Subquery Top-Tier Earner
```sql
USE fs;

SELECT deptno
FROM emp
GROUP BY deptno
HAVING AVG(sal) > (SELECT AVG(sal) FROM emp)

INTERSECT

SELECT DISTINCT deptno
FROM emp
WHERE sal >= (
    SELECT MIN(sal)
    FROM (
        SELECT DISTINCT sal
        FROM emp
        ORDER BY sal DESC 
        LIMIT 2
    ) AS t
);
```
- **Concept:** Finds departments with above-average compensation that also employ someone earning $\ge$ the 2nd highest salary in the company.

---

### [D16_Q14.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q14.sql) — Food Item Transaction Outliers
```sql
USE fs;

SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    f.name AS food_item_name,
    o.total_amount
FROM Orders o
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.total_amount > (
    SELECT AVG(o1.total_amount)
    FROM Orders o1
    WHERE o1.food_id = o.food_id
)
ORDER BY o.total_amount DESC;
```
- **Concept:** Correlated subquery checks if an individual order amount exceeds the average order amount spent on that *specific item* (`o1.food_id = o.food_id`).

---

### [D16_Q15.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY16/D16_Q15.sql) — Peak Revenue Item per Category via Derived Tables
```sql
USE fs;

SELECT t.food_item_name, t.category, t.total_revenue
FROM (
    SELECT 
        f.food_id,
        f.name AS food_item_name,
        f.category,
        SUM(o.total_amount) AS total_revenue
    FROM FoodItems f
    JOIN Orders o ON f.food_id = o.food_id
    WHERE o.status = 'Delivered'
    GROUP BY f.food_id, f.name, f.category
) AS t
WHERE t.total_revenue = (
    SELECT MAX(t2.total_revenue)
    FROM (
        SELECT f.category, SUM(o.total_amount) AS total_revenue
        FROM FoodItems f
        JOIN Orders o ON f.food_id = o.food_id
        WHERE o.status = 'Delivered'
        GROUP BY f.food_id, f.category
    ) AS t2
    WHERE t2.category = t.category
)
ORDER BY total_revenue DESC;
```
- **Concept:** Top-1 per group pattern using nested derived tables and correlated aggregation.

---
---

# DAY 15 — Aggregations, Group Filters & Subquery Patterns

### [D15_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q1.sql) — Manager Average Subordinate Salary
```sql
USE fs;

SELECT
    m.ename AS manager_name,
    AVG(e.sal) AS average_subordinate_salary
FROM emp e
JOIN emp m ON e.mgr = m.empno
GROUP BY m.ename
HAVING AVG(e.sal) > 1500
ORDER BY average_subordinate_salary DESC;
```
- **Concept:** Self-join grouped by supervisor with `HAVING AVG(e.sal) > 1500`.

---

### [D15_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q2.sql) — Category Pricing Distribution
```sql
USE fs;

SELECT
    category,
    COUNT(*) AS total_available_items,
    AVG(price) AS average_price
FROM FoodItems 
WHERE availability = 1 AND price >= 50
GROUP BY category;
```
- **Concept:** Pre-filtering source rows using `WHERE` before aggregating with `GROUP BY category`.

---

### [D15_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q3.sql) — Preserving Zero Orders with LEFT JOIN
```sql
USE fs;

SELECT
    c.address,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(o.order_id) AS total_orders_placed
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.address, c.first_name, c.last_name;
```
- **Key Exam Trap:** Use `COUNT(o.order_id)`, NOT `COUNT(*)`. `COUNT(*)` counts the row generated by the left join and would output `1` for customers with no orders; `COUNT(o.order_id)` properly evaluates `NULL` to `0`.

---

### [D15_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q4.sql) — Qualified Salary Pool (WHERE + HAVING)
```sql
USE fs;

SELECT
    d.dname AS department_name,
    d.location,
    SUM(e.sal) AS qualified_salary_pool
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.sal > 1200
GROUP BY d.dname, d.location
HAVING SUM(e.sal) > 2500;
```
- **Concept:** `WHERE e.sal > 1200` filters employees *before* summing; `HAVING SUM(e.sal) > 2500` filters departments *after* summing.

---

### [D15_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q5.sql) — Category Multi-Filter
```sql
USE fs;

SELECT
    o.order_id,
    f.name AS food_item_name,
    f.category,
    o.quantity
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE f.category IN ('Snacks', 'Beverages')
  AND o.quantity >= 2
ORDER BY o.quantity DESC;
```
- **Concept:** Join between fact and dimension tables with discrete list filtering.

---

### [D15_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q6.sql) — Employee Count per Salary Grade
```sql
USE fs;

SELECT
    s.grade AS salary_grade,
    COUNT(*) AS employee_count
FROM emp e
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
GROUP BY s.grade
HAVING COUNT(*) > 2
ORDER BY salary_grade;
```
- **Concept:** Non-equi join grouped by grade with `HAVING COUNT(*) > 2`.

---

### [D15_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q7.sql) — Self-Join with Multi-Condition WHERE
```sql
USE fs;

SELECT 
    e.ename AS employee_name,
    e.hiredate,
    e.sal AS salary,
    m.ename AS manager_name
FROM emp e
JOIN emp m ON e.mgr = m.empno
WHERE m.empno IN (7698, 7566) AND e.sal > 1000
ORDER BY employee_name;
```
- **Concept:** Self-join retrieving direct reports of specific managers with salary constraints.

---

### [D15_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q8.sql) — Grouping by Date
```sql
USE fs;

SELECT
    DATE(order_date) AS explicit_date,
    COUNT(order_id) AS total_orders,
    MAX(total_amount) AS max_order_amount
FROM Orders 
GROUP BY DATE(order_date)
HAVING MAX(total_amount) > 300;
```
- **Concept:** Truncating timestamps using `DATE(order_date)` and filtering groups on `MAX(total_amount) > 300`.

---

### [D15_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q9.sql) — LIKE Pattern Matching with Grouping
```sql
USE fs;

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.address,
    SUM(o.quantity) AS total_quantity_ordered
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE c.email LIKE '%@yahoo.com'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.address
ORDER BY total_quantity_ordered DESC;
```
- **Concept:** Pre-filtering strings using `LIKE '%@yahoo.com'` before aggregating quantities per customer.

---

### [D15_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q10.sql) — Cumulative Subordinate Payroll
```sql
USE fs;

SELECT 
    m.empno AS manager_id,
    m.ename AS manager_name,
    SUM(e.sal) AS total_subordinate_payroll
FROM emp e
JOIN emp m ON e.mgr = m.empno
GROUP BY m.empno, m.ename
HAVING SUM(e.sal) > 4000
ORDER BY total_subordinate_payroll DESC;
```
- **Concept:** Self-join calculating the total payroll commanded by each manager.

---

### [D15_Q11.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q11.sql) — Multi-Table Filter on Dates and Locations
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    e.job,
    e.hiredate,
    d.dname AS department_name
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.hiredate > '1995-01-01' 
  AND d.location NOT IN ('Boston', 'Tempe')
ORDER BY e.hiredate;
```
- **Concept:** Standard relational join combining temporal filters (`>` date) and set exclusion (`NOT IN`).

---

### [D15_Q12.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q12.sql) — Order Count on Filtered Status
```sql
USE fs;

SELECT 
    f.name AS food_item_name,
    f.category,
    COUNT(o.order_id) AS total_successful_orders
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE f.category = 'Breads' AND o.status = 'Delivered'
GROUP BY f.food_id, f.name, f.category;
```
- **Concept:** Inner join aggregating successful orders for a targeted category.

---

### [D15_Q13.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q13.sql) — Average Order Value on Qualified Orders
```sql
USE fs;

SELECT
    c.customer_id,
    COUNT(o.order_id) AS qualified_orders_count,
    AVG(o.total_amount) AS average_order_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount >= 100
GROUP BY c.customer_id
HAVING COUNT(o.order_id) >= 2;
```
- **Concept:** `WHERE o.total_amount >= 100` filters out low-value orders prior to calculating the average, and `HAVING COUNT(o.order_id) >= 2` restricts output to frequent spenders.

---

### [D15_Q14.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q14.sql) — 3-Table Join with Non-Equi Mapping
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    d.dname AS department_name,
    d.location,
    s.grade AS salary_grade
FROM emp e
JOIN dept d ON e.deptno = d.deptno
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
ORDER BY department_name, salary_grade DESC;
```
- **Concept:** Merging standard equi-join (`emp` + `dept`) with non-equi join (`emp` + `salgrade`) in a single query.

---

### [D15_Q15.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q15.sql) — Fulfilled Dining Revenue Ranking
```sql
USE fs;

SELECT 
    f.name AS food_item_name,
    f.category,
    SUM(o.total_amount) AS revenue_collected
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE o.status = 'Delivered'
GROUP BY f.food_id, f.name, f.category
ORDER BY revenue_collected DESC;
```
- **Concept:** Simple revenue aggregation filtered for completed deliveries.

---

### [D15_Q16.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q16.sql) — Subquery Baseline Price Comparison
```sql
USE fs;

SELECT
    o.order_id,
    o.customer_id,
    o.total_amount
FROM Orders o
JOIN FoodItems f ON o.food_id = f.food_id
WHERE f.price > (SELECT AVG(price) FROM FoodItems);
```
- **Concept:** Filters orders containing food items whose menu price is higher than the overall average menu price.

---

### [D15_Q17.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q17.sql) — Correlated EXISTS for Role Audits
```sql
USE fs;

SELECT d.deptno, d.dname, d.location
FROM dept d
WHERE EXISTS (
    SELECT 1
    FROM emp e
    WHERE e.deptno = d.deptno AND e.job = 'ANALYST'
);
```
- **Concept:** Using `EXISTS` to check if a department currently employs an `'ANALYST'`.

---

### [D15_Q18.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q18.sql) — Subquery in HAVING (Department Payroll vs Mean Payroll)
```sql
USE fs;

SELECT
    deptno,
    SUM(sal) AS total_payroll
FROM emp e
GROUP BY deptno
HAVING SUM(sal) > (
    SELECT AVG(total_salary)
    FROM (
        SELECT SUM(sal) AS total_salary
        FROM emp
        GROUP BY deptno
    ) AS t
);
```
- **Concept:** Benchmarking group sums against the average group sum using a subquery inside `HAVING`.

---

### [D15_Q19.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q19.sql) — NOT IN with NULL-Safe Subquery
```sql
USE fs;

SELECT customer_id, first_name, last_name, email
FROM Customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id 
    FROM Orders 
    WHERE customer_id IS NOT NULL
);
```
- **Key Exam Trap:** When writing `WHERE col NOT IN (SELECT col FROM ...)`, always add `WHERE col IS NOT NULL` inside the subquery to avoid NULL evaluation failures!

---

### [D15_Q20.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY15/D15_Q20.sql) — Correlated Subquery on Job Designation
```sql
USE fs;

SELECT e.empno, e.ename, e.job, e.sal
FROM emp e
WHERE e.sal > (
    SELECT AVG(e2.sal)
    FROM emp e2
    WHERE e2.job = e.job
);
```
- **Concept:** Returns employees who earn more than the average salary for their own job title (`WHERE e2.job = e.job`).

---
---

# DAY 14 — Joins, Aggregation & Foundation Analytics

### [D14_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q1.sql) — Multi-Condition Aggregations
```sql
USE fs;

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
```
- **Concept:** Standard join with `WHERE` filtering by location and `HAVING` filtering on `AVG(e.sal) > 1000`.

---

### [D14_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q2.sql) — Delivered Orders Volume Filter
```sql
USE fs;

SELECT
    c.first_name,
    c.last_name,
    SUM(o.quantity) AS total_items_ordered
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 2
ORDER BY total_items_ordered DESC;
```
- **Concept:** `WHERE` limits rows to `'Delivered'`, `HAVING COUNT(o.order_id) > 2` ensures customer placed at least 3 delivered orders, and `SUM(o.quantity)` sums total items.

---

### [D14_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q3.sql) — Arithmetic Expressions in SELECT
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    e.job AS job_title,
    d.dname AS department_name,
    (e.sal + e.comm) AS total_compensation
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.job = 'SALESMAN'
  AND e.comm > 0
  AND d.location IN ('Chicago', 'Tempe')
ORDER BY total_compensation DESC;
```
- **Concept:** Calculating total compensation as `(e.sal + e.comm)` with multiple `WHERE` conditions. Note: in SQL, adding a `NULL` commission yields `NULL`, so `e.comm > 0` ensures valid numeric addition.

---

### [D14_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q4.sql) — Grouping by Category with Thresholds
```sql
USE fs;

SELECT
    f.name AS food_item_name,
    f.category,
    SUM(o.total_amount) AS total_revenue
FROM FoodItems f
JOIN Orders o ON o.food_id = f.food_id
WHERE f.category IN ('Main Course', 'Breakfast')
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.quantity) > 2
ORDER BY total_revenue DESC;
```
- **Concept:** Aggregating revenue while filtering on quantity volume inside `HAVING`.

---

### [D14_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q5.sql) — Self-Join (Employee to Direct Manager)
```sql
USE fs;

SELECT
    e.empno AS employee_id,
    e.ename AS employee_name,
    m.ename AS manager_name
FROM emp e
JOIN emp m ON e.mgr = m.empno
ORDER BY manager_name ASC;
```
- **Concept:** Self-join pattern linking `e.mgr` to `m.empno`. Automatically excludes root employees (`mgr IS NULL`).

---

### [D14_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q6.sql) — 3-Table Join with String Formatting
```sql
USE fs;

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_full_name,
    c.phone,
    f.name AS food_item_name,
    o.order_date
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.status = 'Preparing' AND f.price > 100
ORDER BY o.order_date ASC;
```
- **Concept:** Multi-table join across `Customers`, `Orders`, and `FoodItems` with `CONCAT`.

---

### [D14_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q7.sql) — Extremum Grouping & Exclusions
```sql
USE fs;

SELECT
    deptno,
    MAX(sal) AS maximum_salary,
    MIN(sal) AS minimum_salary,
    COUNT(*) AS total_employees
FROM emp
WHERE job NOT IN ('PRESIDENT')
GROUP BY deptno
HAVING MAX(sal) > 2000;
```
- **Concept:** Pre-excluding top executives (`WHERE job NOT IN ('PRESIDENT')`) before evaluating department extrema.

---

### [D14_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q8.sql) — Preserving Zero Counts via LEFT JOIN Condition
```sql
USE fs;

SELECT
    f.name AS food_item_name,
    f.category,
    COUNT(o.order_id) AS total_delivered_orders
FROM FoodItems f
LEFT JOIN Orders o 
  ON o.food_id = f.food_id
 AND o.status = 'Delivered'
GROUP BY f.name, f.food_id, f.category
ORDER BY f.name ASC;
```
- **Key Exam Trap:** Placing `AND o.status = 'Delivered'` in the **`ON` clause** of the `LEFT JOIN` preserves all food items (giving count 0 for items never delivered). If you placed it in the `WHERE` clause, it would convert the `LEFT JOIN` into an `INNER JOIN` and discard the 0-count items!

---

### [D14_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q9.sql) — Date and Location Filtering
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    e.hiredate,
    e.job,
    d.location
FROM emp e
JOIN dept d ON d.deptno = e.deptno
WHERE e.hiredate < '1997-01-01'
  AND d.location IN ('Dallas', 'New York')
ORDER BY e.hiredate ASC;
```
- **Concept:** Date comparison (`< '1997-01-01'`) and categorical matching.

---

### [D14_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q10.sql) — Customer Lifetime Spend Exclusion Filter
```sql
USE fs;

SELECT
    c.customer_id,
    c.email,
    SUM(o.total_amount) AS total_amount_spent
FROM Customers c
JOIN Orders o ON o.customer_id = c.customer_id
WHERE o.status NOT IN ('Cancelled')
GROUP BY c.customer_id, c.email
HAVING SUM(o.total_amount) > 500
ORDER BY total_amount_spent DESC;
```
- **Concept:** Excluding failed/cancelled transactions before summing spending per customer.

---

### [D14_Q11.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q11.sql) — Range Mapping with Non-Equi Joins
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    e.job,
    e.sal AS salary,
    s.grade AS salary_grade
FROM emp e
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
ORDER BY s.grade DESC;
```
- **Concept:** `BETWEEN s.losal AND s.hisal` maps numeric values into discrete categories without foreign keys.

---

### [D14_Q12.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q12.sql) — Category Volume Aggregation
```sql
USE fs;

SELECT
    f.category,
    SUM(o.quantity) AS total_quantity_ordered
FROM FoodItems f
JOIN Orders o ON o.food_id = f.food_id
GROUP BY f.category
HAVING SUM(o.quantity) > 5
ORDER BY total_quantity_ordered DESC;
```
- **Concept:** Category-level item volume aggregation.

---

### [D14_Q13.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q13.sql) — Department Exclusion Filtering
```sql
USE fs;

SELECT
    e.ename AS employee_name,
    e.job,
    e.deptno,
    d.dname AS department_name
FROM emp e
JOIN dept d ON d.deptno = e.deptno
WHERE e.job = 'CLERK' 
  AND d.location NOT IN ('New York')
ORDER BY e.ename;
```
- **Concept:** Equi-join with categorical exclusions.

---

### [D14_Q14.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q14.sql) — High Quantity Threshold
```sql
USE fs;

SELECT
    o.order_id,
    c.customer_id,
    o.quantity AS maximum_quantity
FROM Customers c
JOIN Orders o ON o.customer_id = c.customer_id
WHERE o.quantity >= 3 
  AND o.status IN ('Delivered', 'Preparing')
ORDER BY o.quantity DESC;
```
- **Concept:** Transaction-level status and quantity filters.

---

### [D14_Q15.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY14/D14_Q15.sql) — 3-Table Line-Item Reconciliation
```sql
USE fs;

SELECT
    c.email,
    o.order_date,
    f.name AS food_item_name,
    f.price AS unit_price,
    o.total_amount
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.status = 'Pending'
ORDER BY o.order_date ASC;
```
- **Concept:** Standard 3-table join producing line-item order details.

---
---

## 💡 Top 5 Exam Traps for Days 14–17

1. **LEFT JOIN Filter Placement (`ON` vs `WHERE`):**
   - If you want to keep all records from table A and display `0` for table B when no match occurs, condition on table B **must** be inside the `ON` clause:
     `LEFT JOIN Orders o ON o.food_id = f.food_id AND o.status = 'Delivered'`
   - If placed in `WHERE o.status = 'Delivered'`, `NULL` rows are eliminated and it behaves like an `INNER JOIN`.

2. **`COUNT(*)` vs `COUNT(col)` with `LEFT JOIN`:**
   - `COUNT(*)` counts rows, returning `1` for unmatched `LEFT JOIN` records!
   - `COUNT(b.id)` ignores `NULL`s, properly returning `0`.

3. **`NOT IN` with Subqueries that return `NULL`:**
   - Any `NULL` in the subquery result breaks `NOT IN`. Always add `WHERE col IS NOT NULL` inside the subquery, or use `NOT EXISTS`.

4. **Correlated Subqueries in `HAVING`:**
   - When filtering grouped data against category/department peers, reference the outer grouping column:
     `WHERE f2.category = f.category`

5. **`UNION` vs `UNION ALL`:**
   - `UNION` deduplicates and sorts (slower).
   - `UNION ALL` retains all rows (faster). Use `UNION ALL` unless duplicate removal is explicitly requested.
