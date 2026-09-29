"""
Problem Title: Smart Library Book Lending System

Problem Statement:

A digital library maintains records of books issued to members.

Every day, the library management system performs two report
generation cycles:

1. Morning Report
2. Evening Report

During each report generation, the system should display all
currently issued books.

Instead of displaying all issued books together, the system
should generate one issued book record at a time using a
generator function.

After generating the report, the librarian wants to verify
each generated record one by one using an iterator.

Before generating every report, the system should display:

Generating Library Report...

using a decorator.

The report generation should automatically execute twice
(Morning and Evening) using a decorator with arguments.

Requirements:
1. Use a dictionary to store Book ID and Student Name.
2. Use a generator function with yield.
3. Use an iterator using iter() and next().
4. Use a decorator.
5. Use a decorator with arguments.
6. Preserve function metadata using functools.wraps.

Input Format:
First line contains the number of issued books.

Next N sets of input contain:

Book ID
Student Name

Output Format:

Morning Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

Evening Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

Sample Input:
2
Book101
Ravi
Book102
Priya

Sample Output:
Morning Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

Evening Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

case=1
input=2
Book101
Ravi
Book102
Priya

output=
Morning Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

Evening Report
Generating Library Report...
Book101 -> Ravi
Book102 -> Priya

Verified Records:
Book101 -> Ravi
Book102 -> Priya

case=2
input=1
Book201
Kiran

output=
Morning Report
Generating Library Report...
Book201 -> Kiran

Verified Records:
Book201 -> Kiran

Evening Report
Generating Library Report...
Book201 -> Kiran

Verified Records:
Book201 -> Kiran


case=3
input=3
B101
Ravi
B102
Anu
B103
Rahul

output=
Morning Report
Generating Library Report...
B101 -> Ravi
B102 -> Anu
B103 -> Rahul

Verified Records:
B101 -> Ravi
B102 -> Anu
B103 -> Rahul

Evening Report
Generating Library Report...
B101 -> Ravi
B102 -> Anu
B103 -> Rahul

Verified Records:
B101 -> Ravi
B102 -> Anu
B103 -> Rahul

case=4
input=0

output=
Invalid Number of Books

case=5
input=-2

output=
Invalid Number of Books

case=6
input=2
Python101
Swetha
Java102
Mahesh

output=
Morning Report
Generating Library Report...
Python101 -> Swetha
Java102 -> Mahesh

Verified Records:
Python101 -> Swetha
Java102 -> Mahesh

Evening Report
Generating Library Report...
Python101 -> Swetha
Java102 -> Mahesh

Verified Records:
Python101 -> Swetha
Java102 -> Mahesh
"""
from functools import wraps


def logger(func):
    @wraps(func)
    def wrapper(books):
        print("Generating Library Report...")
        return func(books)
    return wrapper    



def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(books):
            for i in range(1,times+1):
                if i==1:
                    print("Morning Report")
                else:
                    print("Evening Report")
                records=list(func(books))    
                for rec in records:
                    print(rec)
                print()    
                print("Verified Records:")
                it=iter(records)
                while True:
                    try:
                        print(next(it))
                    except StopIteration:
                        break
                if i!=times:
                    print()
        return wrapper
    return decorator    



@repeat(2)
@logger
def libr(books):
    for book,student in books.items():
        yield f"{book} -> {student}"


    
n=int(input())
if n<=0:
    print("Invalid Number of Books")
else:
    books={}
    for _ in range(n):
        book=input()
        name=input()
        books[book]=name
    libr(books)



