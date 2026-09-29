"""
Problem Statement:

A university provides merit scholarships to eligible students
based on their academic performance.

The scholarship committee receives applications from multiple
students and processes them during a scholarship evaluation session.

Whenever the evaluation starts, the system should automatically
establish a scholarship evaluation session.

After processing all student applications, the evaluation
session should automatically close irrespective of whether
the evaluation completes successfully or an exception occurs.

Each student application contains:

Student ID
Student Name
CGPA
Annual Family Income

Student information should be stored using a dataclass.

The dataclass should use __slots__ to optimize memory usage.

All student records should be stored in a list.

The scholarship score is calculated as:

Scholarship Score = (CGPA × 10) − (Annual Income / 100000)

Students should be ranked according to the scholarship score
using a lambda expression.

After ranking, eligible students should be generated one by
one using a generator function.

The generated students should then be verified one by one
using an iterator.

Eligibility Criteria:

CGPA >= 8.0

Annual Family Income <= 500000

If CGPA is less than 0 or greater than 10,
raise a custom exception and display:

Invalid CGPA

If Annual Family Income is less than or equal to zero,
display:

Invalid Annual Income

Requirements:

1. Create a dataclass using @dataclass(slots=True).
2. Create a Context Manager using __enter__() and __exit__().
3. Store student details using a list.
4. Rank students using a lambda expression.
5. Generate eligible students using a generator.
6. Verify generated students using an iterator.
7. Create a custom exception.
8. Use raise and try-except.
9. Automatically close the evaluation session.

Input Format:

First line contains the number of students.

Next N sets contain:

Student ID
Student Name
CGPA
Annual Family Income

Output Format:

Opening Scholarship Evaluation Session...

Scholarship Ranking:

S101 -> Ravi -> 9.6 -> 300000
S102 -> Priya -> 9.3 -> 250000
S103 -> Rahul -> 8.9 -> 450000

Eligible Students:

S101 -> Ravi
S102 -> Priya
S103 -> Rahul

Scholarship Evaluation Session Closed

If the number of students is less than or equal to zero,
display:

Invalid Number of Students

If CGPA is invalid, display:

Invalid CGPA

If Annual Family Income is invalid, display:

Invalid Annual Income

Sample Input:

3
S101
Ravi
9.6
300000
S102
Priya
9.3
250000
S103
Rahul
8.9
450000

Sample Output:

Opening Scholarship Evaluation Session...

Scholarship Ranking:

S101 -> Ravi -> 9.6 -> 300000
S102 -> Priya -> 9.3 -> 250000
S103 -> Rahul -> 8.9 -> 450000

Eligible Students:

S101 -> Ravi
S102 -> Priya
S103 -> Rahul

Scholarship Evaluation Session Closed

Test cases:
----------
case=1
input=3
S101
Ravi
9.6
300000
S102
Priya
9.3
250000
S103
Rahul
8.9
450000

output=
Opening Scholarship Evaluation Session...

Scholarship Ranking:
S101 -> Ravi -> 9.6 -> 300000
S102 -> Priya -> 9.3 -> 250000
S103 -> Rahul -> 8.9 -> 450000

Eligible Students:
S101 -> Ravi
S102 -> Priya
S103 -> Rahul

Scholarship Evaluation Session Closed


case=2
input=2
S201
Anu
8.5
400000
S202
Kiran
7.8
300000

output=
Opening Scholarship Evaluation Session...

Scholarship Ranking:
S201 -> Anu -> 8.5 -> 400000
S202 -> Kiran -> 7.8 -> 300000

Eligible Students:
S201 -> Anu

Scholarship Evaluation Session Closed

case=3
input=1
S401
Ajay
10.5
200000

output=
Opening Scholarship Evaluation Session...
Scholarship Evaluation Session Closed
Invalid CGPA

case=4
input=1
S601
Pooja
9.2
0

output=
Opening Scholarship Evaluation Session...
Scholarship Evaluation Session Closed
Invalid Annual Income

case=5
input=-2

output=
Invalid Number of Students

"""
from dataclasses import dataclass

def eligible(students):
    for s in students:
        if s.cgpa >= 8.0 and s.income <= 500000:
            yield s


@dataclass(slots=True)
class Student:
    sid:str
    name:str
    cgpa:float
    income:int
class CGPAError(Exception):
    pass
class Scholarship:
    def __enter__(self):
        print("Opening Scholarship Evaluation Session...")
        return self
    def __exit__(self,a,b,c):
        print("Scholarship Evaluation Session Closed")

n=int(input())
if n<=0:
    print("Invalid Number of Students")
else:
    students=[]
    for _ in range(n):
        sid=input()
        name=input()
        cgpa=float(input())
        income=int(input())
        
        students.append(Student(sid,name,cgpa,income))
    try:
        with Scholarship():
            for s in students:
                if s.cgpa<0 or s.cgpa>10:
                    raise CGPAError
                if s.income<=0:
                    raise ValueError
            students.sort(key=lambda s:(s.cgpa*10)-(s.income/100000),reverse=True)        
            print()
            print("Scholarship Ranking:")
            
            for s in students:
                print(f"{s.sid} -> {s.name} -> {s.cgpa} -> {s.income}")
                
            print()
            print("Eligible Students:")
                
            gen=eligible(students)
                
            it=iter(gen)
                
            while True:
                try:
                    s=next(it)
                    print(f"{s.sid} -> {s.name}")
                except StopIteration:
                    break
    except CGPAError:
        print("Invalid CGPA")
    except ValueError:
        print("Invalid Annual Income")