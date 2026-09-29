"""
Problem Title: Smart API Request Session Manager

Problem Statement:

A cloud-based application receives API requests from clients.

Before processing client requests, the application should
automatically establish an API session.

After processing all requests, the API session should be
closed automatically.

Instead of creating a Context Manager using __enter__()
and __exit__(), create it using the @contextmanager
decorator provided by the contextlib module.

Each API request contains:

Request ID
Client Name

If the number of requests is less than or equal to zero,
display:

Invalid Number of Requests

Requirements:
1. Use the contextmanager decorator from contextlib.
2. Use the yield statement.
3. Display opening and closing session messages.
4. Store request details using a dictionary.
5. Display all requests inside the context manager.

Input Format:
First line contains the number of API requests.

Next N sets contain:

Request ID
Client Name

Output Format:

Opening API Session...
Processing API Requests:
REQ101 -> Ravi
REQ102 -> Priya
Closing API Session...

If the number of requests is invalid, display:

Invalid Number of Requests

Sample Input:
2
REQ101
Ravi
REQ102
Priya

Sample Output:
Opening API Session...
Processing API Requests:
REQ101 -> Ravi
REQ102 -> Priya
Closing API Session...

case=1
input=2
REQ101
Ravi
REQ102
Priya

output=
Opening API Session...
Processing API Requests:
REQ101 -> Ravi
REQ102 -> Priya
Closing API Session...

case=2
input=1
REQ201
Kiran

output=
Opening API Session...
Processing API Requests:
REQ201 -> Kiran
Closing API Session...

case=3
input=3
REQ101
Ravi
REQ102
Anu
REQ103
Rahul

output=
Opening API Session...
Processing API Requests:
REQ101 -> Ravi
REQ102 -> Anu
REQ103 -> Rahul
Closing API Session...

case=4
input=
0

output=
Invalid Number of Requests
"""
from contextlib import contextmanager

@contextmanager
def Req():
    
    print("Opening API Session...")
    
    yield
    
    print("Closing API Session...")



n=int(input())
if n<=0:
    print("Invalid Number of Requests")
else:
    request={}
    for _ in range(n):
        req=input()
        name=input()
        request[req]=name
    with Req():
        print("Processing API Requests:")
        for key,value in request.items():
            print(f"{key} -> {value}")