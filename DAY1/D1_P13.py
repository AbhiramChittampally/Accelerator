"""
Problem Statement:
A company wants to store employee information efficiently.
Create an Employee class using __slots__ to restrict attributes
to employee ID, name, and salary.

Input Format:
Employee ID
Employee Name
Employee Salary

Output Format:
Display employee details.

Sample Input:
101
Ravi
50000

Sample Output:
Employee ID: 101
Employee Name: Ravi
Employee Salary: 50000
"""
from dataclasses import dataclass

@dataclass(slots=True)
class Employee:
    ID:int
    name:str
    salary:int
    
    def display(self):
        print(f"Employee ID: {self.ID}")
        print(f"Employee Name: {self.name}")
        print(f"Employee Salary: {self.salary}")
    
    
id1=int(input())
name=input()
salary=int(input())
Emp=Employee(id1,name,salary)
Emp.display()
