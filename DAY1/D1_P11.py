"""
Problem Statement:
Override the __str__ method to display object information.

Input Format:
Student name

Output Format:
Display formatted student information.

Sample Input:
Ravi

Sample Output:
Student Name: Ravi
"""

from dataclasses import dataclass

@dataclass
class Student:
    name:str
    def __str__(self):
        print(f"Student Name: {self.name}")

Stu=Student(input())
Stu.__str__()



