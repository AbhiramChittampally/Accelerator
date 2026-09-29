USE fs;

CREATE VIEW v_dept_payroll_analytics AS
SELECT
    d.deptno,
    d.dname,
    COUNT(e.empno) AS total_employees,
    IFNULL(SUM(e.sal), 0) AS total_salary_spend
FROM dept d
LEFT JOIN emp e
ON d.deptno = e.deptno
GROUP BY
    d.deptno,
    d.dname;

-- View the result
SELECT * FROM v_dept_payroll_analytics;