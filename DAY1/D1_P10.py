"""
Problem Statement:
Create a Person class and inherit it in Employee class.

Input Format:
Employee name 

Output Format:
Display employee name.

Sample Input:
Ravi

Sample Output:
Employee: Ravi
"""
class Person:
    def __init__(self,name):
        self.name=name
class Employee(Person):
    def display(self):
        print(f"Employee: {self.name}")
emp=Employee(input())
emp.display()
    
