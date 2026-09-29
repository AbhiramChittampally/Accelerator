"""

Problem Statement:

A library supports two membership categories:

1. Student Member
   - Maximum books allowed = 3

2. Faculty Member
   - Maximum books allowed = 5

Override the borrow limit method.

If requested books exceed the limit, display:

Borrow Limit Exceeded

Input Format:
Member Type (Student / Faculty)
Member Name
Number of Books

Output Format:
Display borrowing status.

Sample Input:
Student
Ravi
2

Sample Output:
Books Issued Successfully

case=1
input= Student
Ravi
2

output=
Books Issued Successfully

case=2
input= Student
Priya
3

output=
Books Issued Successfully

case=3
input=Student
John
4

output=
Borrow Limit Exceeded

case=4
input=Faculty
Kiran
5

output=
Books Issued Successfully

case=5
input=Faculty
Swetha
6

output=
Borrow Limit Exceeded

case=6
input=Faculty
David
0

output=
Books Issued Successfully


case=7
input=Student
Anu
1

output=
Books Issued Successfully
"""
from dataclasses import dataclass

@dataclass
class Member:
    name:str
    books:int
class Student(Member):
    def disp(self):
        if self.books<=3:
            return "Books Issued Successfully"
        return "Borrow Limit Exceeded"
class Faculty(Member):
    def disp(self):
        if self.books<=5:
            return "Books Issued Successfully"
        return "Borrow Limit Exceeded"
stat=input().strip().lower()
name=input().strip()
books=int(input())
if stat=="faculty" :
    obj=Faculty(name,books)
    print(f"{obj.disp()}")
elif stat=="student":
    obj=Student(name,books)
    print(f"{obj.disp()}")
else:
    exit()