# SQL Concepts (3.1–3.6) & Problems (DAY14–DAY17) — Complete Explanation

---

## Part 1: SQL Concept Files — What Each One Teaches

### 📘 [3-1.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-1.sql) — SELECT, WHERE, ORDER BY

This is the **foundation boilerplate** for reading data. Key clauses:

| Clause | Purpose | Example |
|---|---|---|
| `SELECT` | Choose which columns to return | `SELECT name, salary` |
| `DISTINCT` | Remove duplicate rows | `SELECT DISTINCT department` |
| `AS` (alias) | Rename a column in output | `salary AS pay` |
| `FROM` | Which table to read from | `FROM employees` |
| `WHERE` | Filter rows **before** grouping | `WHERE salary > 50000` |
| `AND / OR` | Combine multiple conditions | `WHERE dept='Sales' AND sal>50000` |
| `IN (...)` | Match against a list | `WHERE dept IN ('Sales','HR')` |
| `BETWEEN ... AND` | Range check (inclusive) | `WHERE salary BETWEEN 40000 AND 60000` |
| `LIKE` | Pattern matching (`%` = any chars, `_` = one char) | `WHERE name LIKE 'A%'` |
| `IS NULL / IS NOT NULL` | Check for missing values | `WHERE department IS NULL` |
| `ORDER BY` | Sort results | `ORDER BY salary DESC` |
| `LIMIT` | Cap number of rows returned | `LIMIT 5` |

**Execution order**: `FROM → WHERE → SELECT → DISTINCT → ORDER BY → LIMIT`

---

### 📘 [3-2.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-2.sql) — Aggregations & GROUP BY

Aggregate functions **collapse multiple rows into one value**:

| Function | What it does |
|---|---|
| `COUNT(*)` | Total number of rows |
| `COUNT(column)` | Non-NULL values in that column |
| `COUNT(DISTINCT col)` | Unique non-NULL values |
| `SUM(col)` | Add up all values |
| `AVG(col)` | Arithmetic mean |
| `MIN(col)` | Smallest value |
| `MAX(col)` | Largest value |

**GROUP BY** splits the table into groups, then applies the aggregate to each group:
```sql
SELECT department, AVG(salary) FROM employees GROUP BY department;
```

**HAVING** filters **after** grouping (WHERE filters **before**):
```sql
SELECT department, COUNT(*) AS cnt
FROM employees
GROUP BY department
HAVING cnt > 2;       -- can't use WHERE here because cnt doesn't exist yet
```

**Execution order**: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`

---

### 📘 [3-3.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-3.sql) — JOINs

JOINs **combine rows from two or more tables** based on a related column:

| Join Type | What it keeps |
|---|---|
| `INNER JOIN` | Only rows that match in **both** tables |
| `LEFT JOIN` | All rows from left table + matching from right (NULL if no match) |
| `RIGHT JOIN` | All rows from right table + matching from left |
| `FULL OUTER JOIN` | All rows from both (NULL where no match) |
| `SELF JOIN` | Join a table **to itself** (e.g., employee → manager) |

```sql
-- INNER JOIN: only employees who have a department
SELECT e.name, d.dname
FROM emp e
INNER JOIN dept d ON e.deptno = d.deptno;

-- LEFT JOIN: all employees, even those without a department
SELECT e.name, d.dname
FROM emp e
LEFT JOIN dept d ON e.deptno = d.deptno;

-- SELF JOIN: find each employee's manager
SELECT e.ename AS employee, m.ename AS manager
FROM emp e
JOIN emp m ON e.mgr = m.empno;
```

**Anti-Join Pattern** — find rows with NO match:
```sql
SELECT e.name FROM emp e
LEFT JOIN dept d ON e.deptno = d.deptno
WHERE d.id IS NULL;  -- employees with no department
```

---

### 📘 [3-4.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-4.sql) — Subqueries

A subquery is a **query nested inside another query**:

| Type | Where it sits | Correlation |
|---|---|---|
| **Scalar subquery** | In SELECT (returns 1 value) | Usually uncorrelated |
| **Multi-row subquery** | In WHERE with IN/NOT IN | Uncorrelated |
| **Correlated subquery** | In WHERE/HAVING (references outer query) | Correlated — runs once per outer row |
| **EXISTS / NOT EXISTS** | In WHERE (checks if rows exist) | Correlated |

```sql
-- Scalar: one value alongside every row
SELECT name, sal, (SELECT AVG(sal) FROM emp) AS company_avg FROM emp;

-- Multi-row uncorrelated: list of IDs
WHERE dept_id IN (SELECT id FROM dept WHERE location='NYC')

-- Correlated: references outer table
WHERE sal > (SELECT AVG(sal) FROM emp e2 WHERE e2.deptno = e.deptno)

-- EXISTS: "does at least one matching row exist?"
WHERE EXISTS (SELECT 1 FROM project p WHERE p.emp_id = e.emp_id)
```

---

### 📘 [3-5.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-5.sql) — Set Operations

Combine results of **two SELECT statements** (must have same number of columns with compatible types):

| Operation | What it does |
|---|---|
| `UNION` | Combine + **remove duplicates** (slower) |
| `UNION ALL` | Combine + **keep duplicates** (faster) |
| `INTERSECT` | Only rows in **both** queries |
| `EXCEPT` | Rows in first query but **not** in second |

```sql
SELECT name FROM employees_2023
UNION                          -- unique names across both years
SELECT name FROM employees_2024;

SELECT name FROM employees_2023
INTERSECT                      -- people who worked BOTH years
SELECT name FROM employees_2024;
```

---

### 📘 [3-6.sql](file:///C:/Users/Abhiram Chittampally/Documents/ACC/SQL/3-6.sql) — Constraints & Schema Design

DDL (Data Definition Language) for **creating tables** with integrity rules:

| Constraint | Purpose |
|---|---|
| `PRIMARY KEY` | Uniquely identifies each row (NOT NULL + UNIQUE) |
| `FOREIGN KEY` | Links to another table's primary key |
| `NOT NULL` | Column cannot be empty |
| `UNIQUE` | No duplicate values |
| `CHECK` | Validates a condition (e.g., `CHECK(age >= 18)`) |
| `DEFAULT` | Auto-fill value if none provided |
| `AUTO_INCREMENT` | Auto-generate sequential IDs |
| `ON DELETE CASCADE` | When parent row deleted → child rows auto-deleted |
| `ON DELETE RESTRICT` | Prevent deleting parent if children exist |
| `ON UPDATE CASCADE` | When parent key updated → child FKs auto-updated |

**Composite Primary Key** — multiple columns together form the key:
```sql
CONSTRAINT pk_order_items PRIMARY KEY(order_id, product_id)
```

**Bridge Table** — connects two parent tables in a many-to-many relationship (e.g., OrderItems connects Orders ↔ Products).

---

---

## Part 2: DAY14 Problems (15 Problems) — SELECT, WHERE, ORDER BY, JOINs, GROUP BY

> **DAY14 focuses on**: 3.1 (SELECT/WHERE/ORDER BY), 3.2 (Aggregations/GROUP BY), 3.3 (JOINs)

---

### [D14_Q1](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q1.sql) — Department salary analysis with JOIN + GROUP BY + HAVING

```sql
SELECT d.dname AS department_name, SUM(e.sal) AS total_salary, AVG(e.sal) AS average_salary
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE d.location IN ('Dallas', 'Chicago')
GROUP BY d.deptno, d.dname
HAVING AVG(e.sal) > 1000
ORDER BY total_salary DESC;
```

**Concepts used**: `JOIN` (3.3) to link emp↔dept, `WHERE IN` (3.1) to filter locations, `GROUP BY` + `SUM/AVG` (3.2) to aggregate per department, `HAVING` (3.2) to filter groups, `ORDER BY DESC` (3.1).

**How it works**: Joins employees to departments → keeps only Dallas/Chicago → groups by department → calculates total and average salary → filters out departments with avg ≤ 1000 → sorts by total salary descending.

---

### [D14_Q2](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q2.sql) — Customer ordering patterns with JOIN + GROUP BY + HAVING

```sql
SELECT c.first_name, c.last_name, SUM(o.quantity) AS total_items_ordered
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 2
ORDER BY total_items_ordered DESC;
```

**Concepts**: `JOIN` to connect Customers↔Orders, `WHERE` to filter status, `GROUP BY` customer, `SUM` for total items, `HAVING COUNT > 2` to keep only frequent buyers.

---

### [D14_Q3](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q3.sql) — Salesman compensation with calculated columns

```sql
SELECT e.ename AS employee_name, e.job AS job_title, d.dname AS department_name,
       e.sal + e.comm AS total_compensation
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.job = 'SALESMAN' AND e.comm > 0 AND d.location IN ('Chicago','Tempe')
ORDER BY total_compensation DESC;
```

**Concepts**: **Calculated column** (`sal + comm`), multiple `WHERE` conditions with `AND`, `IN` for location filtering, `AS` aliases (3.1).

---

### [D14_Q4](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q4.sql) — Revenue by food category with GROUP BY + HAVING

```sql
SELECT f.name AS food_item_name, f.category, SUM(o.total_amount) AS total_revenue
FROM FoodItems f
JOIN Orders o ON o.food_id = f.food_id
WHERE f.category IN ('Main Course','Breakfast')
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.quantity) > 2
ORDER BY total_revenue DESC;
```

**Key insight**: `WHERE` filters categories **before** grouping, `HAVING SUM(quantity) > 2` filters **after** grouping. This is the core WHERE vs HAVING distinction.

---

### [D14_Q5](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q5.sql) — Management hierarchy with SELF JOIN

```sql
SELECT e.empno AS employee_id, e.ename AS employee_name, m.ename AS manager_name
FROM emp e
JOIN emp m ON e.mgr = m.empno
ORDER BY manager_name ASC;
```

**Concept**: **Self Join** (3.3) — the `emp` table is joined to **itself**. `e` is the employee alias, `m` is the manager alias. `e.mgr = m.empno` links each employee to their manager's row. Employees with no manager (`mgr IS NULL`) are excluded by the INNER JOIN.

---

### [D14_Q6](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q6.sql) — Multi-table JOIN (3 tables)

```sql
SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_full_name, c.phone,
       f.name AS food_item_name, o.order_date
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.status = 'Preparing' AND f.price > 100
ORDER BY o.order_date ASC;
```

**Concepts**: **Three-table JOIN chain** (Customers → Orders → FoodItems), `CONCAT()` to combine strings, multiple WHERE filters.

---

### [D14_Q7](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q7.sql) — Aggregates with exclusion filter

```sql
SELECT deptno, MAX(sal) AS maximum_salary, MIN(sal) AS minimum_salary, COUNT(*) AS total_employees
FROM emp
WHERE job NOT IN ('PRESIDENT')
GROUP BY deptno
HAVING maximum_salary > 2000;
```

**Concepts**: `NOT IN` to exclude rows, `MAX/MIN/COUNT` aggregates (3.2), single-table query (no join needed).

---

### [D14_Q8](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q8.sql) — LEFT JOIN to show zero-count items

```sql
SELECT f.name AS food_item_name, f.category, COUNT(o.order_id) AS total_delivered_orders
FROM FoodItems f
LEFT JOIN Orders o ON o.food_id = f.food_id AND o.status = 'Delivered'
GROUP BY f.name, f.food_id, f.category
ORDER BY f.name ASC;
```

**Key concept**: `LEFT JOIN` (3.3) ensures **all food items appear**, even those with zero delivered orders. The `AND o.status='Delivered'` is placed **in the ON clause** (not WHERE) so that unmatched items still appear with `COUNT = 0`. If put in WHERE, it would filter out NULL rows and defeat the LEFT JOIN.

---

### [D14_Q9](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q9.sql) — Date filtering with JOIN

```sql
SELECT e.ename AS employee_name, e.hiredate, e.job, d.location
FROM emp e
JOIN dept d ON d.deptno = e.deptno
WHERE e.hiredate < '1997-01-01' AND d.location IN ('Dallas','New York')
ORDER BY e.hiredate;
```

**Concepts**: Date comparison with string literal `'1997-01-01'`, `IN` for multiple values, `ORDER BY` for chronological sort.

---

### [D14_Q10](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q10.sql) — Loyal customer spending with NOT IN

```sql
SELECT c.customer_id, c.email, SUM(o.total_amount) AS total_amount_spent
FROM Customers c
JOIN Orders o ON o.customer_id = c.customer_id
WHERE o.status NOT IN ("Cancelled")
GROUP BY c.customer_id, c.email
HAVING SUM(o.total_amount) > 500
ORDER BY total_amount_spent DESC;
```

**Concepts**: `NOT IN` to exclude cancelled orders, `GROUP BY` + `SUM` + `HAVING` to find big spenders.

---

### [D14_Q11](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q11.sql) — Salary grade mapping with BETWEEN in JOIN

```sql
SELECT e.ename AS employee_name, e.job, e.sal AS salary, s.grade AS salary_grade
FROM emp e
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
ORDER BY s.grade DESC;
```

**Key concept**: **Non-equi JOIN** — instead of `ON a.id = b.id`, uses `ON e.sal BETWEEN s.losal AND s.hisal`. This maps each salary to its grade bracket. One salary can fall into multiple overlapping grades, producing multiple rows per employee.

---

### [D14_Q12](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q12.sql) — Category volume analysis

```sql
SELECT f.category, SUM(o.quantity) AS total_quantity_ordered
FROM FoodItems f
JOIN Orders o ON o.food_id = f.food_id
GROUP BY f.category
HAVING SUM(o.quantity) > 5
ORDER BY total_quantity_ordered DESC;
```

**Concepts**: Standard `GROUP BY` with `HAVING` filter pattern (3.2).

---

### [D14_Q13](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q13.sql) — Filtered join with NOT IN

```sql
SELECT e.ename AS employee_name, e.job, e.deptno, d.dname AS department_name
FROM emp e
JOIN dept d ON d.deptno = e.deptno
WHERE e.job = 'CLERK' AND d.location NOT IN ('NEW YORK')
ORDER BY e.ename;
```

---

### [D14_Q14](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q14.sql) — High-quantity order filtering

```sql
SELECT o.order_id, c.customer_id, o.quantity AS maximum_quantity
FROM Customers c
JOIN Orders o ON o.customer_id = c.customer_id
WHERE o.quantity >= 3 AND o.status IN ('Delivered','Preparing')
ORDER BY o.quantity DESC;
```

**Concepts**: `>=` comparison, `IN` for multiple statuses (3.1).

---

### [D14_Q15](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY14/D14_Q15.sql) — Three-table JOIN for order details

```sql
SELECT c.email, o.order_date, f.name AS food_item_name, f.price AS unit_price, o.total_amount
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.status = 'Pending'
ORDER BY o.order_date ASC;
```

**Concepts**: Multi-table JOIN chain (3.3), WHERE filter, ORDER BY.

---

---

## Part 3: DAY15 Problems (20 Problems) — JOINs, Aggregations, Subqueries intro

> **DAY15 focuses on**: 3.2 (Aggregations/GROUP BY/HAVING), 3.3 (JOINs — especially SELF JOIN & LEFT JOIN), 3.4 (Subqueries intro)

---

### [D15_Q1](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q1.sql) — Manager subordinate salary (SELF JOIN + GROUP BY)

```sql
SELECT m.ename AS manager_name, AVG(e.sal) AS average_subordinate_salary
FROM emp e
JOIN emp m ON e.mgr = m.empno
GROUP BY m.ename
HAVING AVG(e.sal) > 1500
ORDER BY average_subordinate_salary DESC;
```

**How it works**: Self-joins `emp` to itself (employee `e` → manager `m`), groups by manager, computes average of subordinate salaries, filters managers where avg > 1500.

---

### [D15_Q2](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q2.sql) — Menu category analysis (single table GROUP BY)

```sql
SELECT category, COUNT(*) AS total_available_items, AVG(price) AS average_price
FROM FoodItems
WHERE availability = 1 AND price >= 50
GROUP BY category;
```

**Concepts**: WHERE filters **before** grouping (removes unavailable and cheap items), then groups by category.

---

### [D15_Q3](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q3.sql) — LEFT JOIN for zero-order customers

```sql
SELECT c.address, CONCAT(c.first_name,' ',c.last_name) AS customer_name,
       COUNT(o.order_id) AS total_orders_placed
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.address, c.first_name, c.last_name;
```

**Key concept**: `LEFT JOIN` guarantees all customers appear. If a customer has no orders, `COUNT(o.order_id)` returns 0 (because `o.order_id` is NULL and COUNT ignores NULLs).

---

### [D15_Q4](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q4.sql) — Department salary pool (WHERE + HAVING combo)

```sql
SELECT d.dname AS department_name, d.location, SUM(e.sal) AS qualified_salary_pool
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.sal > 1200
GROUP BY d.dname, d.location
HAVING SUM(e.sal) > 2500;
```

**Concepts**: `WHERE` removes low-salary employees first, `HAVING` filters departments after summing.

---

### [D15_Q5](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q5.sql) — Category + quantity filter

```sql
SELECT o.order_id, f.name AS food_item_name, f.category, o.quantity
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE f.category IN ('Snacks','Beverages')
GROUP BY o.order_id
HAVING o.quantity >= 2
ORDER BY o.quantity DESC;
```

---

### [D15_Q6](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q6.sql) — Salary grade employee count (Non-equi JOIN)

```sql
SELECT s.grade AS salary_grade, COUNT(*) AS employee_count
FROM emp e
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
GROUP BY s.grade
HAVING COUNT(*) > 2
ORDER BY salary_grade;
```

**Concept**: `BETWEEN` in JOIN condition maps salaries to grade brackets.

---

### [D15_Q7](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q7.sql) — Self JOIN filtered by manager IDs

```sql
SELECT e.ename AS employee_name, e.hiredate, e.sal AS salary, m.ename AS manager_name
FROM emp e
JOIN emp m ON e.mgr = m.empno
WHERE m.empno IN ('7698','7566') AND e.sal > 1000
ORDER BY employee_name;
```

---

### [D15_Q8](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q8.sql) — Date-level order analysis

```sql
SELECT DATE(order_date) AS explicit_date, COUNT(order_id) AS total_orders,
       MAX(total_amount) AS max_order_amount
FROM Orders
GROUP BY order_date
HAVING MAX(total_amount) > 300;
```

**Concept**: `DATE()` extracts just the date part, `GROUP BY` date, `HAVING MAX()` filters.

---

### [D15_Q9](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q9.sql) — Email pattern matching with LIKE

```sql
SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_name, c.email, c.address,
       SUM(o.quantity) AS total_quantity_ordered
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE c.email LIKE '%@yahoo.com'
GROUP BY c.customer_id, customer_name, c.address
ORDER BY SUM(o.quantity) DESC;
```

**Concept**: `LIKE '%@yahoo.com'` — `%` matches any characters before `@yahoo.com` (3.1 pattern matching).

---

### [D15_Q10](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q10.sql) — Manager payroll audit (SELF JOIN)

```sql
SELECT m.empno AS manager_id, m.ename AS manager_name,
       SUM(e.sal) AS total_subordinate_payroll
FROM emp e
JOIN emp m ON e.mgr = m.empno
GROUP BY m.empno, m.ename
HAVING SUM(e.sal) > 4000
ORDER BY total_subordinate_payroll DESC;
```

---

### [D15_Q11](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q11.sql) — Hiring trends with exclusion

```sql
SELECT e.ename AS employee_name, e.job, e.hiredate, d.dname AS department_name
FROM emp e
JOIN dept d ON e.deptno = d.deptno
WHERE e.hiredate > '1995-01-01' AND d.location NOT IN ('Boston','Tempe')
ORDER BY e.hiredate;
```

---

### [D15_Q12](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q12.sql) — Breads delivery count

```sql
SELECT f.name AS food_item_name, f.category, COUNT(o.food_id) AS total_successful_orders
FROM FoodItems f
JOIN Orders o ON f.food_id = o.food_id
WHERE f.category = 'Breads' AND o.status = 'Delivered'
GROUP BY f.name, f.category;
```

---

### [D15_Q13](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q13.sql) — Customer order value metrics

```sql
SELECT c.customer_id, COUNT(o.order_id) AS qualified_orders_count,
       AVG(o.total_amount) AS average_order_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount >= 100
GROUP BY c.customer_id
HAVING COUNT(o.customer_id) >= 2;
```

**Concept**: `WHERE` removes small orders first, then `HAVING` ensures at least 2 qualifying orders remain.

---

### [D15_Q14](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q14.sql) — Three-table JOIN (emp + dept + salgrade)

```sql
SELECT e.ename AS employee_name, d.dname AS department_name, d.location,
       s.grade AS salary_grade
FROM emp e
JOIN dept d ON e.deptno = d.deptno
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
ORDER BY department_name, salary_grade DESC;
```

**Concept**: Combines equi-join (emp↔dept) with non-equi-join (emp↔salgrade via BETWEEN).

---

### [D15_Q15](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q15.sql) — Revenue from delivered orders

```sql
SELECT f.name AS food_item_name, f.category, SUM(o.total_amount) AS revenue_collected
FROM FoodItems f
INNER JOIN Orders o ON f.food_id = o.food_id
WHERE o.status = 'Delivered'
GROUP BY f.food_id, f.name, f.category
ORDER BY revenue_collected DESC;
```

---

### [D15_Q16](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q16.sql) — 🆕 First Subquery! (Uncorrelated in WHERE)

```sql
SELECT o.order_id, o.customer_id, o.total_amount
FROM Orders o
JOIN FoodItems f ON o.food_id = f.food_id
WHERE f.price > (SELECT AVG(price) FROM FoodItems);
```

**Concept**: **Uncorrelated subquery** (3.4) — `SELECT AVG(price) FROM FoodItems` runs **once**, returns a single number, and every order is compared against it. The subquery doesn't reference the outer query.

---

### [D15_Q17](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q17.sql) — EXISTS correlated subquery

```sql
SELECT d.deptno, d.dname, d.location
FROM dept d
WHERE EXISTS (SELECT * FROM emp e WHERE e.deptno = d.deptno AND e.job = 'ANALYST');
```

**Concept**: **EXISTS** (3.4) — for each department `d`, checks if **at least one** employee in that department is an ANALYST. This is a **correlated** subquery because it references `d.deptno` from the outer query. Returns the department row only if the inner query finds ≥ 1 match.

---

### [D15_Q18](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q18.sql) — Subquery in HAVING clause

```sql
SELECT deptno, SUM(sal) AS total_payroll
FROM emp
GROUP BY deptno
HAVING SUM(sal) > (
    SELECT AVG(total_salary) FROM (
        SELECT SUM(sal) AS total_salary FROM emp GROUP BY deptno
    ) AS t
);
```

**Concept**: **Nested subquery in HAVING** (3.4) — the innermost query computes total salary per department, the middle query averages those totals, and HAVING compares each department's total against that average. This is a **two-level deep** subquery.

---

### [D15_Q19](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q19.sql) — NOT IN subquery

```sql
SELECT customer_id, first_name, last_name, email
FROM Customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM Orders WHERE customer_id IS NOT NULL);
```

**Concept**: **Uncorrelated NOT IN subquery** — the inner query finds all customer IDs that placed orders; the outer query returns customers **not** in that list (i.e., customers who never ordered).

---

### [D15_Q20](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY15/D15_Q20.sql) — Correlated subquery (salary vs job average)

```sql
SELECT e.empno, e.ename, e.job, e.sal
FROM emp e
WHERE e.sal > (SELECT AVG(e2.sal) FROM emp e2 WHERE e2.job = e.job);
```

**Concept**: **Correlated subquery** (3.4) — for each employee `e`, the inner query computes the average salary of all employees with the **same job** (`e2.job = e.job`). Only employees earning above their job's average are returned. Runs once per outer row.

---

---

## Part 4: DAY16 Problems (15 Problems) — Advanced Subqueries, Set Operations, Complex JOINs

> **DAY16 focuses on**: 3.4 (Subqueries — correlated, nested, EXISTS), 3.5 (Set Operations — UNION, INTERSECT, EXCEPT)

---

### [D16_Q1](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q1.sql) — Nested subquery + NOT EXISTS

```sql
SELECT DISTINCT c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS full_name, c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > (
    SELECT MAX(beverage_revenue) FROM (
        SELECT SUM(o2.total_amount) AS beverage_revenue
        FROM FoodItems f JOIN Orders o2 ON f.food_id = o2.food_id
        WHERE f.category = 'Beverages' AND o2.status = 'Delivered'
        GROUP BY f.food_id
    ) AS t
)
AND NOT EXISTS (SELECT 1 FROM Orders o3 WHERE o3.customer_id = c.customer_id AND o3.status = 'Cancelled');
```

**Concepts**: **Multi-level nested subquery** (inner computes beverage revenue per item → outer finds MAX of those), `NOT EXISTS` ensures customer has no cancelled orders. Combines 3.4 subqueries with the anti-pattern.

---

### [D16_Q2](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q2.sql) — INTERSECT with nested subquery

```sql
SELECT deptno FROM emp GROUP BY deptno
HAVING AVG(sal) > (SELECT AVG(sal) FROM emp)
INTERSECT
SELECT DISTINCT deptno FROM emp
WHERE sal >= (SELECT MIN(sal) FROM (SELECT sal FROM emp ORDER BY sal DESC LIMIT 3) AS top_earners);
```

**Concepts**: **INTERSECT** (3.5) — only departments satisfying BOTH conditions: (1) average salary above company average, AND (2) has at least one top-3 earner. Uses nested subquery to find the cutoff salary for top 3.

---

### [D16_Q3](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q3.sql) — Uncorrelated subquery for average comparison

```sql
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, c.email, o.order_id, o.total_amount
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > (SELECT AVG(total_amount) FROM Orders)
ORDER BY o.total_amount DESC;
```

**Concept**: Simple **uncorrelated scalar subquery** — `AVG(total_amount)` computed once, used as threshold.

---

### [D16_Q4](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q4.sql) — UNION combining two classification groups

```sql
-- Group 1: High salary tier employees in Chicago
SELECT e.empno, e.ename, 'High Salary Tier in Chicago' AS classification_reason
FROM emp e JOIN dept d ON e.deptno = d.deptno
JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
WHERE d.location = 'Chicago' AND s.grade IN (4,5)

UNION

-- Group 2: Managers of underpaid subordinates
SELECT DISTINCT e.empno, e.ename, 'Manages Underpaid Subordinates' AS classification_reason
FROM emp e JOIN emp s ON e.empno = s.mgr
WHERE s.sal < 1500;
```

**Concept**: **UNION** (3.5) merges two completely different classification queries into one result. `UNION` removes duplicates across the two sets.

---

### [D16_Q5](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q5.sql) — Three-table JOIN with quantity/amount filter

```sql
SELECT o.order_id, c.first_name, f.name AS food_item_name, o.quantity, o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.quantity > 1 AND o.total_amount > 200
ORDER BY o.total_amount DESC;
```

---

### [D16_Q6](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q6.sql) — Correlated subquery for max price per category

```sql
SELECT f.food_id, f.name, f.category, f.price
FROM FoodItems f
WHERE f.price = (SELECT MAX(f2.price) FROM FoodItems f2 WHERE f2.category = f.category);
```

**Concept**: **Correlated subquery** — for each food item, finds the MAX price within its own category. Only items whose price equals that max are returned (i.e., the most expensive item per category).

---

### [D16_Q7](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q7.sql) — INTERSECT + EXCEPT chain

```sql
-- Customers who ordered Chicken Biryani
SELECT customer_id FROM Orders WHERE food_id = (SELECT food_id FROM FoodItems WHERE name='Chicken Biryani')
INTERSECT
-- AND also ordered Mango Lassi
SELECT customer_id FROM Orders WHERE food_id = (SELECT food_id FROM FoodItems WHERE name='Mango Lassi')
EXCEPT
-- BUT never ordered Samosa
SELECT customer_id FROM Orders WHERE food_id = (SELECT food_id FROM FoodItems WHERE name='Samosa');
```

**Concept**: Chains **INTERSECT** then **EXCEPT** (3.5). Read as: "customers who ordered A AND B BUT NOT C". Each subquery resolves the food name to its ID.

---

### [D16_Q8](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q8.sql) — Correlated subquery comparing two totals

```sql
SELECT d.deptno, d.dname
FROM dept d
WHERE (SELECT SUM(e.sal) FROM emp e WHERE e.deptno = d.deptno
       AND e.hiredate BETWEEN '1990-01-01' AND '1999-12-31')
    = (SELECT SUM(e.sal) FROM emp e WHERE e.deptno = d.deptno);
```

**Concept**: Two **correlated scalar subqueries** compared with `=`. Departments where the salary of 90s-hired employees equals the total department salary (meaning everyone was hired in the 90s).

---

### [D16_Q9](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q9.sql) — UNION ALL combining two audit groups

```sql
-- Group 1: Lowest earner in each department
SELECT e.empno, e.ename, e.deptno, 'Lowest Department Earner' AS audit_tag
FROM emp e WHERE e.sal = (SELECT MIN(e1.sal) FROM emp e1 WHERE e1.deptno = e.deptno)

UNION ALL

-- Group 2: Most senior employee overall
SELECT e.empno, e.ename, e.deptno, 'Company Senior Tenure' AS audit_tag
FROM emp e WHERE e.hiredate = (SELECT MIN(e1.hiredate) FROM emp e1);
```

**Concept**: **UNION ALL** (3.5) keeps duplicates (if someone is both lowest earner AND most senior, they appear twice). Each half uses a **correlated subquery** (3.4).

---

### [D16_Q10](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q10.sql) — Scalar correlated subquery in SELECT (percentage calc)

```sql
SELECT e.ename, e.deptno, e.sal,
    ROUND((e.sal * 100) / (SELECT SUM(e1.sal) FROM emp e1 WHERE e1.deptno = e.deptno), 2)
    AS department_contribution_percentage
FROM emp e ORDER BY deptno, e.sal DESC;
```

**Concept**: **Scalar subquery in SELECT** (3.4) — for each employee, computes what % their salary is of their department's total. `ROUND(..., 2)` formats to 2 decimal places.

---

### [D16_Q11](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q11.sql) — Complex HAVING with correlated + nested subqueries

```sql
SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_name, c.email,
       SUM(o.total_amount) AS total_lifetime_spending
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING (SELECT SUM(o1.total_amount) FROM Orders o1 JOIN FoodItems f ON o1.food_id = f.food_id
        WHERE o1.customer_id = c.customer_id AND f.category = 'Breakfast')
     > (SELECT AVG(breakfast_total) FROM
        (SELECT SUM(o2.total_amount) AS breakfast_total FROM Orders o2
         JOIN FoodItems f1 ON o2.food_id = f1.food_id WHERE f1.category = 'Breakfast'
         GROUP BY o2.customer_id) AS t);
```

**Concept**: **Two subqueries inside HAVING** — (1) correlated: this customer's breakfast spending, (2) nested uncorrelated: average breakfast spending across all customers. Only customers whose breakfast spending exceeds the average are returned.

---

### [D16_Q12](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q12.sql) — UNION with subquery-driven filters

```sql
-- Employees in salary grades 4-5 in Chicago departments
SELECT e.empno, e.ename, 'High Salary Tier in Chicago' AS classification_reason
FROM emp e
WHERE e.deptno IN (SELECT d.deptno FROM dept d WHERE d.location = 'Chicago')
  AND e.sal BETWEEN (SELECT losal FROM salgrade WHERE grade = 4)
                AND (SELECT hisal FROM salgrade WHERE grade = 5)
UNION
-- Managers of underpaid subordinates
SELECT e.empno, e.ename, 'Manages Underpaid Subordinates'
FROM emp e WHERE e.empno IN (SELECT mgr FROM emp WHERE sal < 1500);
```

**Concept**: Uses **subqueries to dynamically compute filter boundaries** instead of hardcoding numbers. The salary range comes from the salgrade table via subqueries.

---

### [D16_Q13](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q13.sql) — INTERSECT with nested top-N subquery

Similar to D16_Q2 — finds departments with above-average salary AND containing top-2 earners.

---

### [D16_Q14](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q14.sql) — Correlated subquery (per-food average)

```sql
SELECT o.order_id, o.customer_id, o.order_date, f.name AS food_item_name, o.total_amount
FROM Orders o JOIN FoodItems f ON o.food_id = f.food_id
WHERE o.total_amount > (SELECT AVG(o1.total_amount) FROM Orders o1 WHERE o1.food_id = o.food_id)
ORDER BY o.total_amount DESC;
```

**Concept**: **Correlated subquery** — computes average spending on **the same food item** (`o1.food_id = o.food_id`), returns orders that exceed their item's average.

---

### [D16_Q15](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY16/D16_Q15.sql) — Derived table + correlated subquery for top revenue per category

```sql
SELECT t.food_item_name, t.category, t.total_revenue
FROM (
    SELECT f.food_id, f.name AS food_item_name, f.category, SUM(o.total_amount) AS total_revenue
    FROM FoodItems f JOIN Orders o ON f.food_id = o.food_id WHERE o.status = 'Delivered'
    GROUP BY f.food_id, f.name, f.category
) AS t
WHERE t.total_revenue = (
    SELECT MAX(t2.total_revenue) FROM (
        SELECT f.food_id, f.category, SUM(o.total_amount) AS total_revenue
        FROM FoodItems f JOIN Orders o ON f.food_id = o.food_id WHERE o.status = 'Delivered'
        GROUP BY f.food_id, f.category
    ) AS t2 WHERE t2.category = t.category
) ORDER BY total_revenue DESC;
```

**Concept**: **Derived table** (subquery in FROM, aliased as `t`) — pre-computes per-item revenue. Then a **correlated subquery** in WHERE finds the max revenue for each category. Only items matching their category's max are returned.

---

---

## Part 5: DAY17 Problems (15 Problems) — Subqueries & Set Operations Mastery

> **DAY17 focuses on**: 3.4 (Subqueries — all types), 3.5 (Set Operations), combining everything

---

### [D17_Q1](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q1.sql) — Uncorrelated subquery (above-average quantity)

```sql
SELECT order_id, customer_id, food_id, quantity
FROM Orders
WHERE quantity > (SELECT AVG(quantity) FROM Orders)
ORDER BY quantity DESC, order_id ASC;
```

**Concept**: Classic **uncorrelated scalar subquery** — `AVG(quantity)` computed once, used as threshold.

---

### [D17_Q2](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q2.sql) — INTERSECT for premium categories with orders

```sql
SELECT DISTINCT f.category FROM FoodItems f WHERE f.price > 150
INTERSECT
SELECT f.category FROM FoodItems f JOIN Orders o ON f.food_id = o.food_id;
```

**Concept**: **INTERSECT** (3.5) — categories that are BOTH premium (price > 150) AND have actual orders.

---

### [D17_Q3](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q3.sql) — Scalar subquery in SELECT

```sql
SELECT ename AS employee_name, deptno, sal AS salary,
       (SELECT MAX(sal) FROM emp) AS company_max_salary
FROM emp ORDER BY salary DESC;
```

**Concept**: **Scalar subquery in SELECT** (3.4) — `(SELECT MAX(sal) FROM emp)` runs once and the same value appears alongside every row.

---

### [D17_Q4](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q4.sql) — EXISTS correlated subquery

```sql
SELECT d.deptno, d.dname
FROM dept d
WHERE EXISTS (SELECT 1 FROM emp e WHERE e.deptno = d.deptno AND e.job = 'MANAGER');
```

**Concept**: **EXISTS** — returns departments that have at least one MANAGER. `SELECT 1` is a convention meaning "we don't care what columns — just whether any row exists".

---

### [D17_Q5](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q5.sql) — Correlated subquery in HAVING

```sql
SELECT c.customer_id, CONCAT(c.first_name,' ',c.last_name) AS customer_name,
       c.address AS city_address, SUM(o.total_amount) AS total_customer_lifetime_spend
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > (
    SELECT AVG(o2.total_amount) FROM Customers c2 JOIN Orders o2 ON c2.customer_id = o2.customer_id
    WHERE c2.address = c.address
)
ORDER BY total_customer_lifetime_spend DESC;
```

**Concept**: **Correlated subquery inside HAVING** — for each customer, computes the average order amount of all customers **in the same city** (`c2.address = c.address`). Only customers whose total spend exceeds their city's average transaction are returned.

---

### [D17_Q6](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q6.sql) — UNION for combining two customer segments

```sql
SELECT c.customer_id, c.first_name, c.email
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id WHERE o.quantity > 3
UNION
SELECT c.customer_id, c.first_name, c.email
FROM Customers c JOIN Orders o ON c.customer_id = o.customer_id WHERE o.total_amount > 300;
```

**Concept**: **UNION** (3.5) — customers who ordered quantity > 3 **OR** spent > 300 per order. `UNION` deduplicates, so a customer matching both conditions appears only once.

---

### [D17_Q7](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q7.sql) — Multi-level nested subquery

```sql
SELECT e.ename AS employee_name, d.dname, d.location, e.sal AS salary
FROM emp e JOIN dept d ON e.deptno = d.deptno
WHERE e.sal > (
    SELECT AVG(sal) FROM emp WHERE deptno = (
        SELECT deptno FROM emp GROUP BY deptno ORDER BY SUM(sal) DESC LIMIT 1
    )
);
```

**Concept**: **Three-level nesting** — innermost finds the department with the highest total payroll → middle computes that department's average salary → outer returns employees earning more than that average. Each level depends on the one inside it.

---

### [D17_Q8](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q8.sql) — Correlated subquery with salary grades

```sql
SELECT e.empno, e.ename, e.deptno, e.sal, s.grade
FROM emp e JOIN salgrade s ON e.sal >= s.losal
WHERE s.grade > (
    SELECT AVG(s2.grade) FROM emp e2 JOIN salgrade s2 ON e2.sal >= s2.losal
    WHERE e2.deptno = e.deptno
)
ORDER BY e.deptno, s.grade DESC, e.empno ASC;
```

**Concept**: **Correlated subquery** comparing an employee's grade against their department's average grade.

---

### [D17_Q9](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q9.sql) — UNION ALL + SELF JOIN + NOT IN

```sql
-- Employees earning more than their manager
SELECT e.ename, m.ename AS manager_name, e.sal
FROM emp e JOIN emp m ON e.mgr = m.empno WHERE e.sal > m.sal

UNION ALL

-- System outliers: non-managers earning above manager average, excluding those already in set 1
SELECT e.ename, 'N/A - System Outlier', e.sal
FROM emp e WHERE e.job <> 'MANAGER'
AND e.sal > (SELECT AVG(sal) FROM emp WHERE job = 'MANAGER')
AND e.empno NOT IN (SELECT e1.empno FROM emp e1 JOIN emp m1 ON e1.mgr = m1.empno WHERE e1.sal > m1.sal);
```

**Concept**: **UNION ALL** keeps duplicates, **SELF JOIN** compares employee↔manager salaries, **NOT IN subquery** excludes employees already captured in the first half.

---

### [D17_Q10](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q10.sql) — NOT EXISTS (anti-pattern)

```sql
SELECT f.food_id, f.name, f.category, f.price
FROM FoodItems f
WHERE NOT EXISTS (SELECT * FROM Orders o WHERE o.food_id = f.food_id AND o.status = 'Delivered');
```

**Concept**: **NOT EXISTS** (3.4) — finds food items with **zero** delivered orders. The anti-join pattern: "show me rows from A where no matching row exists in B".

---

### [D17_Q11](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q11.sql) — Derived table (inline subquery in FROM)

```sql
SELECT o.order_id, o.customer_id, o.order_date, o.status, o.total_amount, t.total_customer_orders
FROM Orders o
JOIN (SELECT customer_id, COUNT(*) AS total_customer_orders FROM Orders GROUP BY customer_id) AS t
ON o.customer_id = t.customer_id
ORDER BY o.order_id;
```

**Concept**: **Derived table** (subquery in FROM, aliased as `t`) — pre-computes the total order count per customer. Then this is joined back to the main Orders table so each order row shows the customer's total historical orders alongside it.

---

### [D17_Q12](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q12.sql) — Correlated subquery (2× average fraud detection)

```sql
SELECT o.order_id, o.customer_id, o.food_id, o.total_amount
FROM Orders o
WHERE o.total_amount > (2 * (SELECT AVG(o2.total_amount) FROM Orders o2 WHERE o2.customer_id = o.customer_id));
```

**Concept**: **Correlated subquery** — computes each customer's personal average, then finds orders exceeding **twice** that average (potential fraud spikes).

---

### [D17_Q13](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q13.sql) — Correlated subquery in HAVING (35% market share)

```sql
SELECT f.name AS food_item_name, f.category, SUM(o.total_amount) AS item_total_revenue
FROM FoodItems f JOIN Orders o ON f.food_id = o.food_id
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.total_amount) > (
    0.35 * (SELECT SUM(o2.total_amount) FROM FoodItems f2 JOIN Orders o2 ON f2.food_id = o2.food_id
            WHERE f2.category = f.category)
) ORDER BY item_total_revenue DESC;
```

**Concept**: **Correlated subquery in HAVING** — for each food item, computes the total revenue of its entire category, then checks if this item accounts for more than 35% of that category's revenue. The `f.category` reference makes it correlated.

---

### [D17_Q14](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q14.sql) — Nested subquery in HAVING (above-average headcount)

```sql
SELECT d.deptno, d.dname, SUM(e.sal) AS total_department_payroll
FROM emp e JOIN dept d ON e.deptno = d.deptno
GROUP BY d.deptno, d.dname
HAVING COUNT(*) > (
    SELECT AVG(emp_count) FROM (SELECT COUNT(*) AS emp_count FROM emp GROUP BY deptno) AS t
);
```

**Concept**: **Two-level nested subquery in HAVING** — inner counts employees per department, outer averages those counts. Only departments with above-average headcount are returned.

---

### [D17_Q15](file:///C:/Users/Abhiram Chittampally/Documents/ACC/DAY17/D17_Q15.sql) — Correlated subquery in HAVING (quantity vs category average)

```sql
SELECT f.name AS food_item_name, f.category, SUM(o.quantity) AS total_quantity_sold
FROM FoodItems f JOIN Orders o ON f.food_id = o.food_id
WHERE o.status = 'Delivered'
GROUP BY f.food_id, f.name, f.category
HAVING SUM(o.quantity) > (
    SELECT AVG(o2.quantity) FROM FoodItems f2 JOIN Orders o2 ON f2.food_id = o2.food_id
    WHERE f2.category = f.category AND o2.status = 'Delivered'
) ORDER BY total_quantity_sold DESC;
```

**Concept**: **Correlated subquery in HAVING** — compares each item's total delivered quantity against the average transaction quantity within its category.

---

---

## Summary: Concept → Problem Mapping

| Concept | Topic | Problems that use it |
|---|---|---|
| **3.1** SELECT/WHERE/ORDER BY | Filtering, sorting, LIKE, IN, BETWEEN, IS NULL, LIMIT, aliases | D14_Q1–Q15 (all), D15_Q2, Q5, Q9, Q11, Q12 |
| **3.2** GROUP BY / Aggregations | COUNT, SUM, AVG, MIN, MAX, HAVING | D14_Q1–Q4, Q7, Q10, Q12; D15_Q1–Q4, Q6, Q8, Q10, Q13, Q15 |
| **3.3** JOINs | INNER, LEFT, SELF, Non-equi (BETWEEN), Multi-table, Anti-join | D14_Q1–Q6, Q8–Q11, Q13–Q15; D15_Q1, Q3, Q4, Q6, Q7, Q10, Q14 |
| **3.4** Subqueries | Uncorrelated, Correlated, Scalar, EXISTS, NOT EXISTS, Nested, Derived tables | D15_Q16–Q20; D16_Q1–Q15; D17_Q1–Q15 |
| **3.5** Set Operations | UNION, UNION ALL, INTERSECT, EXCEPT | D16_Q2, Q4, Q7, Q9, Q12, Q13; D17_Q2, Q6, Q9 |
| **3.6** Constraints & Schema | PK, FK, UNIQUE, CHECK, CASCADE | Concept file only (no practice problems) |

---

## Key Patterns to Remember

```
┌─────────────────────────────────────────────────────────┐
│ WHERE  → filters individual ROWS    (before grouping)   │
│ HAVING → filters GROUPS             (after GROUP BY)    │
│                                                         │
│ INNER JOIN → only matching rows                         │
│ LEFT JOIN  → all left rows + NULLs for non-matches      │
│ SELF JOIN  → table joined to itself (employee→manager)  │
│                                                         │
│ Uncorrelated subquery → runs ONCE (independent)         │
│ Correlated subquery   → runs ONCE PER OUTER ROW         │
│ EXISTS → "does at least one row exist?"                  │
│ NOT EXISTS → anti-join pattern                           │
│ Derived table → subquery in FROM clause                  │
│                                                         │
│ UNION     → combine + deduplicate                       │
│ UNION ALL → combine + keep duplicates                   │
│ INTERSECT → only rows in BOTH                           │
│ EXCEPT    → rows in first but NOT second                │
└─────────────────────────────────────────────────────────┘
```
