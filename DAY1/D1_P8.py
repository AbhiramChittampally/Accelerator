"""
Problem Statement:
Write a function that accepts student information using **kwargs
and displays all key-value pairs.

Input Format:
Student name
Student age
Student branch

Output Format:
Display all student details.

Sample Input:
Ravi
20
CSE

Sample Output:
name : Ravi
age : 20
branch : CSE
"""

def info(**kwargs):
    for key,value in kwargs.items():
        print(key+" "+ ":"+" " +value)
name=input()
age=input()
branch=input()
info(name=name, age=age, branch=branch)

