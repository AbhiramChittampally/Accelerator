"""
Problem Statement:

A software company receives different types of input data from
multiple applications.

The system should validate the given values using a single
generic function instead of creating separate validation
functions for each data type.

The program should support the following data types:

• Integer
• Float
• String

Validation Rules:

For Integer:
The value must be greater than zero.

For Float:
The value must be greater than zero.

For String:
The value should not be empty and must contain only
alphabetical characters.

The program should use TypeVar to create a generic validation
function that works for all the above data types.

The program should also use Python Type Hints.

Requirements:
-------------
1. Create a generic type using TypeVar.
2. Create a generic validation function.
3. Use Python Type Hints.
4. Validate Integer values.
5. Validate Float values.
6. Validate String values.
7. Display whether the value is Valid or Invalid.

Input Format:
-------------
First line contains the data type.

Possible values:
int
float
string

Second line contains the value.

Output Format:
--------------
Valid Data

OR

Invalid Data

Sample Input:
-------------
int
25

Sample Output:
--------------
Valid Data

Test Cases:
-----------

case=1
input=int
25

output=
Valid Data

case=2
input=int
-15

output=
Invalid Data

case=3
input=float
25.75

output=
Valid Data

case=4
input=float
0

output=
Invalid Data

case=5
input=string
Python

output=
Valid Data

case=6
input=string
Python123

output=
Invalid Data

case=7
input=string

output=
Invalid Data
"""

from typing import TypeVar

T = TypeVar("T", int, float, str)
def validate(data : T)->bool:
    if isinstance(data,int):
        return data>0
    if isinstance(data,float):
        return data>0
    if isinstance(data,str):
        return data != "" and data.isalpha()
        
dtype=input()

if dtype=="int":
    data=int(input())
elif dtype=="float":
    data=float(input())
elif dtype=="string":
    data=input()
else:
    data=None

if validate(data):
    print("Valid Data")
else:
    print("Invalid Data")