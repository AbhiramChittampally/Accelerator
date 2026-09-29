"""
Problem Statement:

A software company maintains application logs generated
from multiple servers.

Each log entry contains:

• Log ID
• Log Level
• Module Name

The Log Level can be one of the following:

INFO
WARNING
ERROR

The system should analyze the application logs using
two different methods.

Method 1:
Count the frequency of each Log Level using a traditional
if-else approach.

Method 2:
Count the frequency of each Log Level using Python's
dictionary get() method.

Instead of measuring execution time, compare the
efficiency of both methods by counting the number of
operations performed.

Assume the following:

• Method 1 performs one operation for processing each
  log record.

• Method 2 uses dictionary.get() and is considered an
  optimized approach.

• For evaluation purposes:

      If only one log record exists,
      Method 2 performs 1 operation.

      Otherwise,
      Method 2 performs 3 operations
      (one optimized operation for each valid log level:
      INFO, WARNING and ERROR).

Store all log records using a list.

The log analysis functions should use Python Type Hints.

After processing all log records:

• Display the frequency of each Log Level.

• Display the most frequently occurring Log Level.

• Display the number of operations performed by each
  method.

• Display the better performing method.

Requirements:
-------------
1. Store log records using a list.
2. Use Python Type Hints.
3. Implement Method 1 using if-else statements.
4. Implement Method 2 using dictionary get().
5. Count the number of operations.
6. Display the frequency of each Log Level.
7. Display the most frequent Log Level.
8. Display the better performing method.

Input Format:
-------------
First line contains the number of log records N.

Next N sets contain:

Log ID
Log Level
Module Name

Output Format:
--------------
Log Summary:

INFO : 2
WARNING : 1
ERROR : 3

Most Frequent Log Level : ERROR

Method 1 Operations : 6

Method 2 Operations : 3

Better Performing Method : Method 2

If N <= 0 display

Invalid Number of Log Records

If Log Level is not one of

INFO
WARNING
ERROR

display

Invalid Log Level

Sample Input:
-------------
6
L101
INFO
Login
L102
ERROR
Database
L103
WARNING
Memory
L104
INFO
Logout
L105
ERROR
Server
L106
ERROR
Network

Sample Output:
--------------
Log Summary:
INFO : 2
WARNING : 1
ERROR : 3

Most Frequent Log Level : ERROR

Method 1 Operations : 6

Method 2 Operations : 3

Better Performing Method : Method 2

Test Cases
----------

case=1
input=6
L101
INFO
Login
L102
ERROR
Database
L103
WARNING
Memory
L104
INFO
Logout
L105
ERROR
Server
L106
ERROR
Network
output=
Log Summary:
INFO : 2
WARNING : 1
ERROR : 3

Most Frequent Log Level : ERROR

Method 1 Operations : 6

Method 2 Operations : 3

Better Performing Method : Method 2


case=2
input=4
L201
WARNING
Disk
L202
WARNING
CPU
L203
INFO
Login
L204
WARNING
Memory

output=
Log Summary:
INFO : 1
WARNING : 3
ERROR : 0

Most Frequent Log Level : WARNING

Method 1 Operations : 4

Method 2 Operations : 3

Better Performing Method : Method 2


case=3
input=1
L301
INFO
Home
output=
Log Summary:
INFO : 1
WARNING : 0
ERROR : 0

Most Frequent Log Level : INFO

Method 1 Operations : 1

Method 2 Operations : 1

Better Performing Method : Both Methods


case=4
input=0
output=
Invalid Number of Log Records


case=5
input=2
L401
SUCCESS
Login
L402
INFO
Logout

output=
Invalid Log Level
"""

def m1(logs : list[str]):
    info=0
    warn=0
    error=0
    op=0
    
    for lvl in logs:
        op+=1
        if lvl=="INFO":
            info+=1
        elif lvl=="WARNING":
            warn+=1;
        else:
            error+=1
    return info,warn,error,op        

def m2(logs : list[str]):
    freq={}
    for lvl in logs:
        freq[lvl]=freq.get(lvl,0)+1
    if "INFO"    not in freq:
        freq["INFO"]=0
    if "WARNING"    not in freq:
        freq["WARNING"]=0
    if "ERROR"    not in freq:
        freq["ERROR"]=0
    if len(logs)==1:
        op=1
    else:
        op=3
    return freq,op

n=int(input())

if n<=0:
    print("Invalid Number of Log Records")
else:
    logs=[]
    valid = True
    for _ in range(n):
        lid=input()
        lvl=input()
        mod=input()
        if lvl not in ["INFO","WARNING","ERROR"]:
            valid = False
        logs.append(lvl)
    if not valid:
        print("Invalid Log Level")
    else:
        info,warn,error,op1=m1(logs)
        freq,op2=m2(logs)
            
        print("Log Summary:")
        print(f"INFO : {info}")
        print(f"WARNING : {warn}")
        print(f"ERROR : {error}")
        print()
            
        if info >= warn and info >=error:
            most="INFO"
        elif warn >= error:
            most = "WARNING"
        else:
            most="ERROR"
        print(f"Most Frequent Log Level : {most}")
        print()
        print(f"Method 1 Operations : {op1}")
        print()
        print(f"Method 2 Operations : {op2}")
        print()    
        if op1 < op2:
            print("Better Performing Method : Method 1")
        elif op2 < op1:
            print("Better Performing Method : Method 2")
        else:
            print("Better Performing Method : Both Methods")