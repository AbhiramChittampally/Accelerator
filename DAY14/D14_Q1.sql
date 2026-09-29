/*
Problem Description:

The HR and Finance departments want to analyze employee compensation metrics across specific regional offices. 
Write an SQL query to retrieve the department name, the total salary distribution, and the average salary of employees for each department. 
Filter the records to only include departments located in Dallas or Chicago, and 
ensure that only departments with an average salary greater than 1,000 are displayed.
Sort the final output in descending order of the total salary expenditure.


case=1
output=
department_name	total_salary	average_salary
Research	11825.00	1970.833333
Sales	5600.00	1866.666667

*/

USE fs;

SELECT
    d.dname AS department_name,
    SUM(e.sal) AS total_salary,
    AVG(e.sal) AS average_salary
FROM emp e
JOIN dept d
    ON e.deptno = d.deptno
WHERE d.location IN ('Dallas', 'Chicago')
GROUP BY d.deptno, d.dname
HAVING AVG(e.sal) > 1000
ORDER BY total_salary DESC;