USE fs;

CREATE VIEW v_senior_staff_directory AS
SELECT
    e.empno,
    e.ename AS employee_name,
    e.job,
    e.sal AS salary,
    s.grade AS salary_grade,
    d.dname AS department_name
FROM emp e
JOIN dept d
ON e.deptno = d.deptno
JOIN salgrade s
ON e.sal BETWEEN s.losal AND s.hisal
WHERE s.grade IN (4, 5);

-- View the result
SELECT * FROM v_senior_staff_directory;