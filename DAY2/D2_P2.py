"""
Problem Statement:

A company wants to maintain employee payroll records in a secure manner.
Once an employee record is created, its details should remain unchanged
to avoid accidental modifications.

Create an employee record containing the employee's name and salary and
display the employee information.

Requirements:
1. Use Python Dataclasses to create the Employee class.
2. Ensure that employee objects become immutable after creation.

Input Format:
Employee Name
Employee Salary

Output Format:
Display the employee details.

Sample Input:
Ravi
50000

Sample Output:
Employee(name='Ravi', salary=50000)
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Employee:
    name:str
    salary:int
    
    def __str__(self):
        return f"Employee(name='{self.name}', salary={self.salary})"
name=input()
salary=int(input())

Emp=Employee(name,salary)

print(Emp)

