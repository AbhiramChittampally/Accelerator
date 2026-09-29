"""
Problem Statement:

A university stores student records containing student names and marks.
The administration requires the following operations:

1. When a student object is printed, its details should appear in a
   readable format.

2. The number of characters in a student's name should be obtained
   using the built-in len() function.

3. Two students should be considered equal if they have the same marks.

4. One student should be considered smaller than another student if
   his/her marks are lower.

Input Format:
Student1 Name
Student1 Marks
Student2 Name
Student2 Marks

Output Format:
Display both students.
Display the length of the first student's name.
Check whether both students have equal marks.
Check whether the first student has fewer marks than the second student.

Sample Input:
Ravi
85
Priya
92

Sample Output:
Student(name='Ravi', marks=85)
Student(name='Priya', marks=92)
4
False
True



"""
class Student:
    def __init__(self,name,marks):
        self.name=name
        self.marks=marks
    def __str__(self):
        return f"Student(name='{self.name}', marks={self.marks})"
    def __len__(self):
        return len(self.name)
    def __eq__(self, other):
        return self.marks==other.marks
    def __lt__(self, other):
        return self.marks<other.marks


s1n=input()
s1m=int(input())
s2n=input()
s2m=int(input())

Stu1=Student(s1n,s1m)
Stu2=Student(s2n,s2m)
print(Stu1)
print(Stu2)
print(len(Stu1))
print(Stu1==Stu2)
print(Stu1<Stu2)