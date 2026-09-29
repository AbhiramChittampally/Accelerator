USE fs;

EXPLAIN
SELECT *
FROM emp
WHERE deptno = 20;

CREATE INDEX idx_emp_dept
ON emp(deptno);

EXPLAIN
SELECT *
FROM emp
WHERE deptno = 20;

SELECT *
FROM emp
WHERE deptno = 20;