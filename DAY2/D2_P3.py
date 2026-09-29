"""
Problem Statement:

A company's Human Resources department wants to generate a salary report
for its employees. To simplify analysis, the employees should be arranged
in ascending order of their salaries.

Create employee records containing employee name and salary and display
the employees sorted according to salary.

Requirements:
1. Use Python Dataclasses to represent employee records.
2. Employee objects should support automatic comparison and sorting.
3. Accept any number of employees dynamically.

Input Format:
First line contains an integer N representing the number of employees.

Next N sets of inputs contain:
Employee Name
Employee Salary

Output Format:
Display employee records sorted in ascending order of salary.

Sample Input:
3
Ravi
30000
Priya
45000
Kiran
25000

Sample Output:
Employee(salary=25000, name='Kiran')
Employee(salary=30000, name='Ravi')
Employee(salary=45000, name='Priya')
"""
from dataclasses import dataclass

@dataclass(order=True)
class Employee:
    salary:int
    name:str
    
        
n=int(input())
employees=[]
for _ in range (n):
    
    name=input()
    sal=int(input())
    employees.append(Employee(sal,name))
employees.sort()
for emp in employees:
    print(emp)
   

