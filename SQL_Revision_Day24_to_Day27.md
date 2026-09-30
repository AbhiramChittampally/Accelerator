# SQL Comprehensive Revision Guide (Day 24 – Day 27)

---

## 🎯 Master Exam Cheat Sheet

### 1. Window Ranking Functions Comparison
| Function | Ties Behavior | Gaps in Sequence? | Example for values (3000, 3000, 2975) | Typical Use Case |
| :--- | :--- | :---: | :--- | :--- |
| **`ROW_NUMBER()`** | Arbitrary distinct rank (1, 2, 3) | **No** | `1, 2, 3` | Top-1 per group, pagination, tie-breaking |
| **`RANK()`** | Same rank for ties (1, 1, 3) | **Yes** | `1, 1, 3` | Competition ranks, Olympic medals |
| **`DENSE_RANK()`** | Same rank for ties (1, 1, 2) | **No** | `1, 1, 2` | Nth-highest salary, salary tiers |
| **`NTILE(k)`** | Divides rows into `k` equal buckets | **No** | `1, 1, 2` | Quartiles, deciles, tier splitting |

---

### 2. Window Framing Syntax & Rules
```sql
{ROWS | RANGE} BETWEEN <frame_start> AND <frame_end>
```
- **Default Frame when `ORDER BY` is present:**
  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
- **Default Frame when `ORDER BY` is absent:**
  `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
- **Common Frames:**
  - Running Total: `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
  - Entire Partition (e.g. for `LAST_VALUE`): `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
  - Prior 2 rows (excluding current): `ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING`
  - 3-period Centered Moving Average: `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`

---

### 3. Value Functions (`LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`)
- **`LAG(col, [offset], [default]) OVER (PARTITION BY ... ORDER BY ...)`**: Looks backward (prior rows).
- **`LEAD(col, [offset], [default]) OVER (PARTITION BY ... ORDER BY ...)`**: Looks forward (subsequent rows).
- **`FIRST_VALUE(col) OVER (...)`**: Returns first row in frame (works with default frame).
- **`LAST_VALUE(col) OVER (...)`**: **MUST** specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, otherwise it stops at `CURRENT ROW` and returns the current row.

---

### 4. Recursive CTE Template
```sql
WITH RECURSIVE HierarchyCTE AS
(
    -- 1. ANCHOR MEMBER (Base condition, runs once)
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE manager_id IS NULL  -- (Top-down) or WHERE id = 7369 (Bottom-up)

    UNION ALL

    -- 2. RECURSIVE MEMBER (Iterates until JOIN returns 0 rows)
    SELECT e.id, e.name, e.manager_id, h.depth + 1
    FROM employees e
    JOIN HierarchyCTE h
      ON e.manager_id = h.id  -- (Top-down) or e.id = h.manager_id (Bottom-up)
)
SELECT * FROM HierarchyCTE;
```

---
---

# DAY 27 — Advanced Window Frames & Recursive Trees

### [D27_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q1.sql) — Cumulative Running Salary Payout per Department
```sql
USE fs;

SELECT
    deptno,
    empno,
    ename,
    sal,
    SUM(sal) OVER
    (
        PARTITION BY deptno
        ORDER BY empno
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS dept_running_sal_total
FROM emp;
```
- **Concept:** Computes running cumulative total of department salaries ordered by `empno`.
- **Key Takeaway:** The explicit window frame `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` ensures that every row includes itself and all previous rows in that department.

---

### [D27_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q2.sql) — Local Transaction Spikes (LAG + LEAD)
```sql
USE fs;

WITH OrderComparison AS
(
    SELECT
        order_id,
        total_amount,
        LAG(total_amount) OVER (ORDER BY order_date DESC) AS prev_amt,
        LEAD(total_amount) OVER (ORDER BY order_date DESC) AS next_amt
    FROM Orders
)
SELECT
    order_id,
    total_amount,
    prev_amt,
    next_amt
FROM OrderComparison
WHERE total_amount > prev_amt
  AND total_amount > next_amt;
```
- **Concept:** Finding local peaks in time series data.
- **Key Takeaway:** Uses `LAG()` and `LEAD()` simultaneously in a CTE, then filters in the outer query where `total_amount` strictly exceeds both neighbors.

---

### [D27_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q3.sql) — Department Salary Range Cards (MAX + MIN OVER)
```sql
USE fs;

SELECT
    deptno,
    ename,
    sal,
    MAX(sal) OVER (PARTITION BY deptno) AS max_dept_sal,
    MIN(sal) OVER (PARTITION BY deptno) AS min_dept_sal
FROM emp;
```
- **Concept:** Appending group-level aggregates to individual employee rows without collapsing rows.
- **Key Takeaway:** Omitting `ORDER BY` inside `OVER (PARTITION BY deptno)` ensures the `MAX` and `MIN` are calculated across the **entire partition**, not as a running min/max.

---

### [D27_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q4.sql) — Reporting Distance to Top Executive (Recursive CTE)
```sql
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    -- Anchor: President (root)
    SELECT empno, ename, mgr, 0 AS steps_to_president
    FROM emp
    WHERE mgr IS NULL

    UNION ALL

    -- Recursive: find subordinates and increment step
    SELECT e.empno, e.ename, e.mgr, eh.steps_to_president + 1
    FROM emp e
    JOIN EmployeeHierarchy eh ON e.mgr = eh.empno
)
SELECT empno, ename, mgr, steps_to_president
FROM EmployeeHierarchy;
```
- **Concept:** Top-down tree traversal to calculate organizational depth.
- **Key Takeaway:** Anchor starts where `mgr IS NULL` at depth `0`. The recursive join `ON e.mgr = eh.empno` increments depth by `1` at each tier until all reports are found.

---

### [D27_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q5.sql) — Spending Acceleration (Prior 2 Orders Average)
```sql
USE fs;

WITH CustomerOrders AS
(
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROUND(
            AVG(total_amount) OVER (
                PARTITION BY customer_id
                ORDER BY order_date
                ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING
            ), 
            2
        ) AS prior_2_avg
    FROM Orders
)
SELECT order_id, customer_id, order_date, total_amount, prior_2_avg
FROM CustomerOrders
WHERE total_amount > prior_2_avg;
```
- **Concept:** Custom window frame excluding the current row.
- **Key Takeaway:** `ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING` calculates the average of strictly the prior 2 orders without including the current order. The `, 2` in `ROUND(..., 2)` rounds the result to 2 decimals. For the first order, `prior_2_avg` is `NULL`, so `total_amount > NULL` is false and naturally filtered.

---

### [D27_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q6.sql) — Department Median Proxy Employee & Salary Spread
```sql
USE fs;

WITH emp_rank AS
(
    SELECT
        deptno,
        ename,
        sal,
        ROW_NUMBER() OVER (PARTITION BY deptno ORDER BY sal) AS rn,
        COUNT(*) OVER (PARTITION BY deptno) AS cnt,
        MAX(sal) OVER (PARTITION BY deptno) AS max_sal,
        MIN(sal) OVER (PARTITION BY deptno) AS min_sal
    FROM emp
)
SELECT
    deptno,
    ename AS median_proxy_emp,
    sal,
    (max_sal - min_sal) AS dept_sal_spread
FROM emp_rank
WHERE rn = FLOOR((cnt + 1) / 2)  -- or CEIL(cnt / 2)
ORDER BY deptno;
```
- **Concept:** Finding median element using row numbering and partition count.
- **Key Takeaway:**
  - Standard median index for 1-indexed sequences is `(cnt + 1) / 2`.
  - `FLOOR((cnt + 1) / 2)` and `CEIL(cnt / 2)` are mathematically identical for all integers.
  - Using `cnt / 2` alone fails for odd counts and causes 1-row departments to evaluate to `rn = 0` (which drops the row).

---

### [D27_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q7.sql) — Consecutive Order Gaps (LAG + DATEDIFF)
```sql
USE fs;

WITH CustomerGaps AS
(
    SELECT
        customer_id,
        order_id,
        DATEDIFF(
            order_date,
            LAG(order_date) OVER (
                PARTITION BY customer_id
                ORDER BY order_date ASC
            )
        ) AS days_since_prev_order
    FROM Orders
)
SELECT customer_id, order_id, days_since_prev_order
FROM CustomerGaps
WHERE days_since_prev_order IS NOT NULL;
```
- **Concept:** Measuring time delta between consecutive events per entity.
- **Key Takeaway:** `PARTITION BY customer_id` isolates calculation per user. `LAG()` looks at the prior row's date. `DATEDIFF(cur, prev)` computes elapsed days. `WHERE ... IS NOT NULL` removes the initial order.

---

### [D27_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q8.sql) — Menu Category Revenue Contribution Percentage
```sql
USE fs;

WITH cte AS (
    SELECT 
        f.category, 
        f.name AS food_name, 
        SUM(o.total_amount) AS item_revenue
    FROM Orders o 
    JOIN FoodItems f ON o.food_id = f.food_id
    GROUP BY f.food_id, f.category, f.name
),
cte2 AS (
    SELECT
        *,
        SUM(item_revenue) OVER (PARTITION BY category) AS category_total_revenue
    FROM cte
)
SELECT  
    *, 
    ROUND(item_revenue * 100 / category_total_revenue, 2) AS revenue_pct 
FROM cte2
ORDER BY category, item_revenue DESC;
```
- **Concept:** Two-stage aggregation (GROUP BY followed by Window Sum).
- **Key Takeaway:** First CTE aggregates to item level. Second CTE uses `SUM(item_revenue) OVER (PARTITION BY category)` without `ORDER BY` to compute category total on every item row.

---

### [D27_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q9.sql) — First & Last Hires with Span (FIRST_VALUE + LAST_VALUE)
```sql
USE fs;

WITH RoleHires AS (
    SELECT DISTINCT
        job,
        FIRST_VALUE(ename) OVER (
            PARTITION BY job ORDER BY hiredate ASC
        ) AS first_hired_emp,
        FIRST_VALUE(hiredate) OVER (
            PARTITION BY job ORDER BY hiredate ASC
        ) AS first_hire_date,
        LAST_VALUE(ename) OVER (
            PARTITION BY job ORDER BY hiredate ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS latest_hired_emp,
        LAST_VALUE(hiredate) OVER (
            PARTITION BY job ORDER BY hiredate ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS latest_hire_date
    FROM emp
)
SELECT 
    job,
    first_hired_emp,
    first_hire_date,
    latest_hired_emp,
    latest_hire_date,
    DATEDIFF(latest_hire_date, first_hire_date) AS hiring_span_days
FROM RoleHires;
```
- **Concept:** Extrema retrieval in partitioned data.
- **Key Takeaway:** `LAST_VALUE()` **must** have `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, otherwise it defaults to `CURRENT ROW` and returns the current row. `SELECT DISTINCT` deduplicates the rows per job.

---

### [D27_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY27/D27_Q10.sql) — Revenue Milestone Status Flagging
```sql
USE fs;

WITH RunningRevenue AS
(
    SELECT
        order_id,
        order_date,
        total_amount,
        SUM(total_amount) OVER
        (
            ORDER BY order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
    FROM Orders
)
SELECT
    order_id,
    order_date,
    total_amount,
    running_total,
    CASE
        WHEN running_total < 2000 THEN 'PRE MILESTONE'
        WHEN running_total - total_amount < 2000 THEN 'MILESTONE REACHED'
        ELSE 'POST MILESTONE'
    END AS milestone_status
FROM RunningRevenue;
```
- **Concept:** Detecting the transition row where a cumulative target is met.
- **Key Takeaway:** The condition `running_total - total_amount < 2000` evaluates the *prior* order's running sum. Combined with knowing `running_total >= 2000`, it precisely pinpoints the crossing record.

---
---

# DAY 26 — Ranking Methods, Sliding Frames & Lead/Lag

### [D26_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q1.sql) — Side-by-Side Ranking Comparison
```sql
USE fs;

SELECT
    ename,
    sal,
    ROW_NUMBER() OVER (ORDER BY sal DESC) AS row_num,
    RANK() OVER (ORDER BY sal DESC) AS rnk,
    DENSE_RANK() OVER (ORDER BY sal DESC) AS dense_rnk
FROM emp;
```
- **Concept:** Direct contrast of window ranking behaviors on tied salaries (e.g., SCOTT and FORD both earn 3000):
  - `ROW_NUMBER()`: 2, 3 (arbitrary distinct)
  - `RANK()`: 2, 2, next is 4 (skips rank 3)
  - `DENSE_RANK()`: 2, 2, next is 3 (no gaps)

---

### [D26_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q2.sql) — Second-Highest Salary Earner per Department
```sql
USE fs;

WITH DepartmentSalaryRank AS
(
    SELECT
        deptno,
        ename,
        sal,
        DENSE_RANK() OVER (
            PARTITION BY deptno
            ORDER BY sal DESC
        ) AS salary_rank
    FROM emp
)
SELECT deptno, ename, sal
FROM DepartmentSalaryRank
WHERE salary_rank = 2;
```
- **Concept:** Top-N and Nth-tier retrieval.
- **Key Takeaway:** Use `DENSE_RANK()`, NOT `ROW_NUMBER()`. If two employees share the top salary (Rank 1, 1), `ROW_NUMBER()` would call one of them rank 2 (wrong), whereas `DENSE_RANK()` correctly assigns rank 2 to the true next salary tier.

---

### [D26_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q3.sql) — Menu Item Popularity Ranking
```sql
USE fs;

WITH FoodPopularity AS
(
    SELECT
        f.name,
        f.category,
        SUM(o.quantity) AS total_qty
    FROM FoodItems f
    JOIN Orders o ON f.food_id = o.food_id
    GROUP BY f.food_id, f.name, f.category
)
SELECT
    name,
    category,
    total_qty,
    RANK() OVER (ORDER BY total_qty DESC) AS popularity_rank
FROM FoodPopularity;
```
- **Concept:** Ranking aggregate volumes across joined tables.
- **Key Takeaway:** CTE aggregates quantities by item first; outer query applies `RANK()` globally across all items.

---

### [D26_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q4.sql) — Category Pioneer (First Item Ordered per Category)
```sql
USE fs;

WITH CategoryOrders AS
(
    SELECT
        o.order_id,
        f.category,
        f.name AS food_item,
        o.order_date,
        ROW_NUMBER() OVER (
            PARTITION BY f.category
            ORDER BY o.order_date ASC
        ) AS rn
    FROM Orders o
    JOIN FoodItems f ON o.food_id = f.food_id
)
SELECT order_id, category, food_item, order_date
FROM CategoryOrders
WHERE rn = 1;
```
- **Concept:** Selecting the earliest record per group.
- **Key Takeaway:** `ROW_NUMBER() OVER (PARTITION BY category ORDER BY order_date ASC)` numbered from 1, and `WHERE rn = 1` picks the pioneer item.

---

### [D26_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q5.sql) — 3-Order Centered Moving Average
```sql
USE fs;

SELECT
    order_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS moving_avg_3_orders
FROM Orders;
```
- **Concept:** Centered moving average smoothing.
- **Key Takeaway:** `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` spans exactly 3 rows: the previous row, the current row, and the next row.

---

### [D26_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q6.sql) — Department Compensation Tier Splitting (NTILE)
```sql
USE fs;

SELECT
    empno,
    ename,
    sal,
    NTILE(2) OVER (ORDER BY sal DESC) AS salary_tier
FROM emp
WHERE deptno = 20;
```
- **Concept:** Equal-sized bucket distribution.
- **Key Takeaway:** `NTILE(2)` splits the sorted rows into two halves: top 50% get tier `1`, bottom 50% get tier `2`. If odd, the extra row goes into the lower-numbered bucket.

---

### [D26_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q7.sql) — Cumulative Platform Revenue Stream
```sql
USE fs;

SELECT
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) AS running_revenue_total
FROM Orders;
```
- **Concept:** Running total using default frame.
- **Key Takeaway:** When `ORDER BY` is provided without a frame, SQL defaults to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Note: If multiple rows have the identical `order_date`, `RANGE` will sum all duplicate date peers together.

---

### [D26_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q8.sql) — Sequential Transaction Variance / Delta
```sql
USE fs;

SELECT
    order_id, 
    order_date, 
    total_amount AS current_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    total_amount - LAG(total_amount, 1) OVER (ORDER BY order_date) AS amount_diff
FROM Orders;
```
- **Concept:** Step-by-step delta computation.
- **Key Takeaway:** Directly subtracts `LAG(total_amount, 1)` from `total_amount` in the `SELECT` list. The first row yields `NULL` for both `prev_amount` and `amount_diff`.

---

### [D26_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q9.sql) — Repeat Customer Order Interval Frequency in Hours
```sql
USE fs;

SELECT
    customer_id,
    order_id,
    order_date,
    LAG(order_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY order_date ASC
    ) AS prev_order_date,
    TIMESTAMPDIFF(
        HOUR,
        LAG(order_date, 1) OVER (
            PARTITION BY customer_id
            ORDER BY order_date ASC
        ),
        order_date
    ) AS hours_since_last_order
FROM Orders;
```
- **Concept:** Fine-grained time difference using `TIMESTAMPDIFF`.
- **Key Takeaway:** Unlike `DATEDIFF(date1, date2)` which only measures days, MySQL's `TIMESTAMPDIFF(unit, start_datetime, end_datetime)` accepts `HOUR`, `MINUTE`, or `SECOND`. Notice order: `(unit, earlier_date, later_date)`.

---

### [D26_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY26/D26_Q10.sql) — Top 2 Most Recently Hired Employees per Role
```sql
USE fs;

WITH HiresRanked AS (
    SELECT 
        empno, 
        ename, 
        job, 
        hiredate,
        ROW_NUMBER() OVER (
            PARTITION BY job 
            ORDER BY hiredate DESC
        ) AS rn
    FROM emp
)
SELECT empno, ename, job, hiredate
FROM HiresRanked
WHERE rn <= 2;
```
- **Concept:** Top-N per group pattern.
- **Key Takeaway:** Partitioning by `job` and ordering by `hiredate DESC` assigns `rn = 1` and `rn = 2` to the two newest hires per role. Outer filter `WHERE rn <= 2`.

---
---

# DAY 25 — Subtree Aggregations, Row Multipliers & Pay Equity

### [D25_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY25/D25_Q1.sql) — Total Subtree Headcount & Salary Budget (BLAKE, 7698)
```sql
USE fs;

WITH RECURSIVE TeamHierarchy AS
(
    -- Anchor: Manager BLAKE
    SELECT empno, ename, sal
    FROM emp
    WHERE empno = 7698

    UNION ALL

    -- Recursive: all direct and indirect reports
    SELECT e.empno, e.ename, e.sal
    FROM emp e
    JOIN TeamHierarchy th ON e.mgr = th.empno
)
SELECT
    COUNT(empno) AS total_team_members,
    SUM(sal) AS total_team_salary
FROM TeamHierarchy;
```
- **Concept:** Aggregating metrics across an entire management subtree.
- **Key Takeaway:** Anchor starts specifically with `empno = 7698`. The recursive step cascades down to all subordinates. The outer query aggregates `COUNT()` and `SUM()` across the full collected team.

---

### [D25_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY25/D25_Q2.sql) — Map Every Employee to Ultimate Top Boss
```sql
USE fs;

WITH RECURSIVE emph AS
(
    -- Anchor: Top boss (mgr IS NULL)
    SELECT
        empno AS original_emp,
        empno,
        ename,
        mgr
    FROM emp
    WHERE mgr IS NULL

    UNION ALL

    -- Recursive: pass top boss name down through each layer
    SELECT 
        e.empno AS original_emp,
        e.empno,
        eh.ename,
        e.mgr
    FROM emp e
    JOIN emph eh ON e.mgr = eh.empno
)
SELECT
    original_emp,
    ename AS ultimate_boss
FROM emph
ORDER BY original_emp;
```
- **Concept:** Propagating an ancestor attribute down the entire hierarchy.
- **Key Takeaway:** In the recursive step, `eh.ename` keeps propagating the root president's name down to each subordinate row.

---

### [D25_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY25/D25_Q3.sql) — Granular Order Expansion / Row Multiplication
```sql
USE fs;

WITH RECURSIVE OrderItems AS
(
    -- Anchor: first item number for each order
    SELECT
        order_id,
        customer_id,
        food_id,
        1 AS item_number,
        quantity
    FROM Orders

    UNION ALL

    -- Recursive: increment item_number until reaching quantity
    SELECT
        order_id,
        customer_id,
        food_id,
        item_number + 1,
        quantity
    FROM OrderItems
    WHERE item_number < quantity
)
SELECT order_id, customer_id, food_id, item_number, quantity
FROM OrderItems
ORDER BY order_id, item_number;
```
- **Concept:** Generating $N$ physical rows from a single quantity number using a recursive CTE.
- **Key Takeaway:** The anchor assigns `item_number = 1`. The recursive step increments `item_number + 1` with condition `WHERE item_number < quantity`. If an order has `quantity = 4`, it generates 4 separate rows (useful for printing tickets, generating barcodes, or unnesting quantities).

---

### [D25_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY25/D25_Q4.sql) — Pay Equity Ranking without Gaps (DENSE_RANK)
```sql
USE fs;

SELECT
    deptno,
    ename,
    sal,
    DENSE_RANK() OVER (
        PARTITION BY deptno
        ORDER BY sal DESC
    ) AS sal_rank
FROM emp;
```
- **Concept:** Consecutive ranking per department.
- **Key Takeaway:** `DENSE_RANK()` ensures tied salaries share the same rank while the next salary receives the immediate next consecutive integer (1, 1, 2, 3...).

---

### [D25_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY25/D25_Q5.sql) — VIP Customer Highest Purchase with Tie-Breaking
```sql
USE fs;

WITH CustomerOrders AS
(
    SELECT
        order_id,
        customer_id,
        total_amount,
        order_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY total_amount DESC, order_date ASC
        ) AS rn
    FROM Orders
)
SELECT order_id, customer_id, total_amount, order_date
FROM CustomerOrders
WHERE rn = 1;
```
- **Concept:** Deterministic tie-breaking in window functions.
- **Key Takeaway:** If a customer has two orders tied for the highest amount, `ORDER BY total_amount DESC, order_date ASC` guarantees the earliest placed order gets `rn = 1`.

---
---

# DAY 24 — CTE Foundations, Chaining & Date Sequences

### [D24_Q1.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q1.sql) — Basic CTE Aggregation & Threshold Filtering
```sql
USE fs;

WITH CustomerSpending AS
(
    SELECT
        customer_id,
        SUM(total_amount) AS TotalSpent
    FROM Orders
    GROUP BY customer_id
)
SELECT customer_id, TotalSpent
FROM CustomerSpending
WHERE TotalSpent > 500;
```
- **Concept:** Replaces a `HAVING` clause with a clean, readable CTE.
- **Key Takeaway:** Aggregates spending in the CTE and filters with standard `WHERE` in the outer query.

---

### [D24_Q2.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q2.sql) — Filtered Aggregation CTE with Customer Join
```sql
USE fs;

WITH CustomerSpending AS
(
    SELECT
        customer_id,
        SUM(total_amount) AS Delivered_Spent
    FROM Orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.first_name,
    cs.Delivered_Spent
FROM Customers c
JOIN CustomerSpending cs ON c.customer_id = cs.customer_id
WHERE cs.Delivered_Spent > 500;
```
- **Concept:** Pre-filtering rows (`status = 'Delivered'`) before aggregating, then enriching with dimension tables.
- **Key Takeaway:** Keeps aggregation isolated in the CTE and joins with `Customers` to retrieve `first_name`.

---

### [D24_Q3.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q3.sql) — Above-Average Departmental Salaries (Chained CTEs)
```sql
USE fs;

WITH davg AS
(
    SELECT deptno, AVG(sal) AS avgs
    FROM emp
    GROUP BY deptno
),
aavg AS
(
    SELECT e.empno, e.ename, e.sal, e.deptno
    FROM emp e
    JOIN davg d ON e.deptno = d.deptno
    WHERE e.sal > d.avgs
)
SELECT empno, ename, sal, deptno
FROM aavg;
```
- **Concept:** Chained CTEs (`CTE1, CTE2`).
- **Key Takeaway:** `davg` calculates each department's average salary. The subsequent CTE `aavg` immediately references `davg` to filter employees who earn more than their department's average.

---

### [D24_Q4.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q4.sql) — Category Revenue Distribution across Delivered Orders
```sql
USE fs;

WITH categrev AS
(
    SELECT 
        f.category,
        SUM(o.total_amount) AS tr
    FROM Orders o
    JOIN FoodItems f ON o.food_id = f.food_id
    WHERE o.status = 'Delivered'
    GROUP BY f.category
)
SELECT category, tr AS total_revenue
FROM categrev
WHERE tr > 500;
```
- **Concept:** Multi-table join inside CTE with aggregate filtering.
- **Key Takeaway:** Combines fact table (`Orders`) and dimension table (`FoodItems`), filters by status, groups by category, and filters total revenue $> 500$.

---

### [D24_Q5.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q5.sql) — Non-Equi Joins across Salary Grades
```sql
USE fs;

WITH Salg AS
(
    SELECT s.grade, e.sal
    FROM emp e
    JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal
),
grades AS
(
    SELECT
        grade,
        COUNT(*) AS employee_count,
        SUM(sal) AS total_grade_sal
    FROM Salg
    GROUP BY grade
)
SELECT * FROM grades
WHERE total_grade_sal > 5000;
```
- **Concept:** Non-equi join (`BETWEEN ... AND ...`) inside a CTE chain.
- **Key Takeaway:** `ON e.sal BETWEEN s.losal AND s.hisal` maps continuous salaries to discrete salary grades without requiring an exact ID match.

---

### [D24_Q6.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q6.sql) — Modular Formatting with String Concatenation
```sql
USE fs;

WITH CustomerOrderDetails AS
(
    SELECT
        CONCAT(c.first_name, ' ', c.last_name) AS full_name,
        f.name AS food_item,
        o.total_amount
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN FoodItems f ON o.food_id = f.food_id
)
SELECT full_name, food_item, total_amount
FROM CustomerOrderDetails
WHERE total_amount >= 300;
```
- **Concept:** 3-table join with field formatting inside a CTE.
- **Key Takeaway:** `CONCAT(c.first_name, ' ', c.last_name)` formats the customer's full name cleanly in the CTE projection.

---

### [D24_Q7.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q7.sql) — Bottom-Up Management Hierarchy (SMITH to Top Boss)
```sql
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    -- Anchor: Frontline worker SMITH (7369)
    SELECT empno, ename, job, mgr
    FROM emp
    WHERE empno = 7369

    UNION ALL

    -- Recursive: find the manager of the person above
    SELECT e.empno, e.ename, e.job, e.mgr
    FROM emp e
    JOIN EmployeeHierarchy eh ON e.empno = eh.mgr
)
SELECT empno, ename, job, mgr
FROM EmployeeHierarchy;
```
- **Concept:** Bottom-up recursive tree traversal.
- **Key Takeaway:** Contrast with top-down! Here the join condition is:
  `ON e.empno = eh.mgr`
  (Find the employee record whose ID equals the current person's manager ID). Climbs from SMITH $\rightarrow$ FORD $\rightarrow$ JONES $\rightarrow$ KEVIN (President).

---

### [D24_Q8.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q8.sql) — Hierarchy Path String & Level Generation
```sql
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    -- Anchor: Top management
    SELECT
        empno,
        ename,
        1 AS lvl,
        ename AS path
    FROM emp
    WHERE mgr IS NULL

    UNION ALL

    -- Recursive: build path string and increment level
    SELECT
        e.empno,
        e.ename,
        eh.lvl + 1,
        CONCAT(eh.path, ' -> ', e.ename)
    FROM emp e
    JOIN EmployeeHierarchy eh ON e.mgr = eh.empno
)
SELECT empno, ename, lvl, path
FROM EmployeeHierarchy;
```
- **Concept:** Breadcrumb / path tracking in trees.
- **Key Takeaway:** `CONCAT(eh.path, ' -> ', e.ename)` continually appends the subordinate's name to the cumulative path string from root to leaf.

---

### [D24_Q9.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q9.sql) — Direct and Indirect Subordinates of a Manager (JONES, 7566)
```sql
USE fs;

WITH RECURSIVE EmployeeHierarchy AS
(
    -- Anchor: Direct reports of JONES
    SELECT empno, ename, mgr
    FROM emp
    WHERE mgr = 7566

    UNION ALL

    -- Recursive: indirect reports
    SELECT e.empno, e.ename, e.mgr
    FROM emp e
    JOIN EmployeeHierarchy eh ON e.mgr = eh.empno
)
SELECT empno, ename, mgr
FROM EmployeeHierarchy;
```
- **Concept:** Subtree extraction excluding the manager himself.
- **Key Takeaway:** Notice the anchor condition: `WHERE mgr = 7566` (starts with JONES's direct reports, leaving out JONES himself).

---

### [D24_Q10.sql](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/DAY24/D24_Q10.sql) — Date Sequence Generation & Missing Date Detection
```sql
USE fs;

WITH RECURSIVE DateSequence AS
(
    -- Anchor: Start date
    SELECT DATE('2026-07-10') AS order_date

    UNION ALL

    -- Recursive: add 1 day until reaching end date
    SELECT DATE_ADD(order_date, INTERVAL 1 DAY)
    FROM DateSequence
    WHERE order_date < '2026-07-17'
)
SELECT d.order_date
FROM DateSequence d
LEFT JOIN Orders o ON d.order_date = o.order_date
WHERE o.order_date IS NULL;
```
- **Concept:** Calendar table generation and anti-joins.
- **Key Takeaway:**
  - `DATE_ADD(order_date, INTERVAL 1 DAY) ... WHERE order_date < '2026-07-17'` generates a consecutive calendar series without needing a physical calendar table.
  - `LEFT JOIN ... WHERE o.order_date IS NULL` (anti-join pattern) reliably finds dates with zero activity.

---
---

## 💡 Top 5 Exam Traps & Rules of Thumb

1. **`LAST_VALUE()` Pitfall:** Never use `LAST_VALUE()` with `ORDER BY` without specifying `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Otherwise, it only looks up to `CURRENT ROW`!
2. **Median Calculation:** When picking the middle row with `ROW_NUMBER()`, always use `FLOOR((cnt + 1) / 2)` or `CEIL(cnt / 2)`. Never write `FLOOR(cnt / 2)` because single-row groups will produce `0` and vanish!
3. **Recursive CTE Direction:**
   - **Top-Down:** Anchor `WHERE mgr IS NULL`; Join `ON e.mgr = eh.empno`.
   - **Bottom-Up:** Anchor `WHERE empno = <id>`; Join `ON e.empno = eh.mgr`.
4. **`NTILE()` Bucket Allocation:** If $N$ does not divide evenly by $k$, extra rows are distributed to the first buckets (e.g. 5 rows with `NTILE(2)` $\rightarrow$ bucket 1 gets 3 rows, bucket 2 gets 2 rows).
5. **Anti-Joins for Missing Values:** To find dates/entities with no events, generate the master list (e.g. via recursive CTE) and `LEFT JOIN` the event table `WHERE event.id IS NULL`.
