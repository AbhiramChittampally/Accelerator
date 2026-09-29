"""
Problem Title: Smart Employee Salary Analytics using NumPy Arrays

Problem Statement:

A software company wants to analyze the monthly salaries
of its employees using NumPy.

The HR department stores the salaries of all employees
in a NumPy array.

The company wants to generate the following salary
statistics:

• Average Salary
• Highest Salary
• Lowest Salary

The management also decides to increase every employee's
salary by 10%.

The salary increment should be performed using
NumPy Vectorization without using loops.

Requirements:
-------------
1. Store salaries in a NumPy array.
2. Use Vectorization to increase salary by 10%.
3. Display Average Salary.
4. Display Highest Salary.
5. Display Lowest Salary.
6. Display Updated Salaries.

Input Format:
-------------
First line contains the number of employees N.

Next N lines contain employee salaries.

Output Format:
--------------
Average Salary : <average>

Highest Salary : <highest>

Lowest Salary : <lowest>

Updated Salaries:
<salary1>
<salary2>
...

If N <= 0 display

Invalid Number of Employees

If salary <= 0 display

Invalid Salary

Sample Input:
-------------
5
25000
30000
45000
40000
35000

Sample Output:
--------------
Average Salary : 35000.0

Highest Salary : 45000

Lowest Salary : 25000

Updated Salaries:
27500.0
33000.0
49500.0
44000.0
38500.0


Test Cases
----------

case=1
input=
5
25000
30000
45000
40000
35000
output=
Average Salary : 35000.0
Highest Salary : 45000
Lowest Salary : 25000
Updated Salaries:
27500.0
33000.0
49500.0
44000.0
38500.0


case=2
input=
3
50000
60000
70000
output=
Average Salary : 60000.0
Highest Salary : 70000
Lowest Salary : 50000
Updated Salaries:
55000.0
66000.0
77000.0

case=3
input=
1
45000
output=
Average Salary : 45000.0
Highest Salary : 45000
Lowest Salary : 45000
Updated Salaries:
49500.0

case=4
input=
0
output=
Invalid Number of Employees


case=5
input=
3
25000
-5000
30000
output=
Invalid Salary
"""
import numpy as np
n=int(input())
if n<=0:
    print("Invalid Number of Employees")
else:
    nums=[]
    valid=True
    for _ in range(n):
        num=int(input())
        nums.append(num)
        if num<=0:
            valid=False
    if not valid:
        print("Invalid Salary")
        
    else:
        arr=np.array(nums) 
        print(f"Average Salary : {np.mean(arr)}")
        print(f"Highest Salary : {np.max(arr)}")
        print(f"Lowest Salary : {np.min(arr)}")
        print("Updated Salaries:")
        uarr=arr*1.10
        for num in uarr:
            print(f"{num:.1f}")