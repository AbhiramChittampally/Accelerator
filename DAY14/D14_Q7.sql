/*
Problem Description:
The executive committee is preparing the budget for next year and needs to pinpoint departments with heavy payroll allocations.
Write an SQL query to calculate the maximum salary, minimum salary, and total workforce count for each department number in the employee records.
Exclude employees who hold the title of 'PRESIDENT' from this calculation, and filter the groups to show only departments where the maximum salary is greater than 2000.


case=1
output=
deptno	maximum_salary	minimum_salary	total_employees
10	2450.00	1300.00	3
20	3000.00	800.00	6
30	2850.00	1250.00	3

*/
use fs;
select
    deptno,
    MAX(sal) as maximum_salary,
    MIN(sal) as minimum_salary,
    COUNT(*) as total_employees
from emp
where job not IN('PRESIDENT')
group by deptno
having maximum_salary>2000
