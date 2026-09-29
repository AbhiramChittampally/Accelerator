"""


Problem Statement:

A company calculates salaries in different ways.

Implement calculate_salary() using *args.

Cases:

1 value → Basic Salary

2 values → Basic Salary + Bonus

3 values → Basic Salary + Bonus + Incentive

Input Format:
Number of Values
Salary Components

Output Format:
Display total salary.

Sample Input:
3
30000
5000
2000

Sample Output:
Total Salary = 37000

case=1
input= 1
30000

output=
Total Salary = 30000

case=2
input= 2
30000
5000

output=
Total Salary = 35000

case=3
input= 3
30000
5000
2000

output=
Total Salary = 37000

case=4
input=2
45000
10000

output=
Total Salary = 55000


case=5
input=3
25000
0
3000

output=
Total Salary = 28000
"""
n=int(input())
values=[]
for _ in range(n):
    values.append(int(input()))
def totals(*args):
    return sum(args)

print(f"Total Salary = {totals(*values)}")