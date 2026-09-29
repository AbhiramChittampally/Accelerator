/*
Topic: Chained CTEs across Non-Equi Joins

Statement: Categorize employees by salary grade, compute total salary spent per grade, and list grades accounting for more than ₹5,000 in salary payout. Display grade, employee_count, and total_grade_sal.

case=1
output=

grade	employee_count	total_grade_sal
1	8	9750.00
3	7	17375.00
2	10	21175.00
4	6	19275.00


*/
use fs;
with Salg as
(
    select
        s.grade,
        e.sal
    from emp e
    join salgrade s
    on e.sal between s.losal and s.hisal
    
),
grades as
(
    select
        grade,
        count(*) as employee_count,
        sum(sal) as total_grade_sal
    from Salg
    group by grade
)
select * from grades
where total_grade_sal>5000