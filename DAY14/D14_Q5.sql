/*

Problem Description:
The HR department needs a clear view of the management reporting hierarchy to update their internal directory. 
Write an SQL query to retrieve the names of all employees alongside the names of their direct managers. 
The output should display the employee's number, employee's name, and the manager's name under the alias manager_name. 
Exclude any employees who do not report to anyone, and sort the list alphabetically by the manager's name.


case=1
output=
employee_id	employee_name	manager_name
7499	ALLEN	BLAKE
7521	ALLEN	BLAKE
7654	MARTIN	BLAKE
7844	KEVIN	BLAKE
7900	JAMES	BLAKE
7934	FORD	CLARK
7369	SMITH	FORD
7788	SCOTT	JONES
7902	FORD	JONES
7566	JONES	KEVINa
7698	BLAKE	KEVIN
7782	CLARK	KEVIN
7876	KEVIN	SCOTT
*/
use fs;
select
    e.empno as employee_id,
    e.ename as employee_name,
    m.ename as manager_name
from emp e
join emp m 
    on e.mgr=m.empno
order by manager_name ASC 