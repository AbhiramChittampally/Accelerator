"""

Problem Statement:

An API gateway receives a large number of client request IDs
from different users.

To reduce server load and improve processing efficiency,
the gateway processes client requests in fixed-size batches.

Instead of creating all batches at once, design a generator
function to generate one batch at a time.

If the number of requests is less than or equal to zero,
display:

Invalid Number of Requests

If the batch size is less than or equal to zero,
display:

Invalid Batch Size

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate one batch at a time.
4. Use list slicing.
5. Validate the number of requests.
6. Validate the batch size.

Input Format:
First line contains the number of requests.

Next N lines contain the request IDs.

Last line contains the batch size.

Output Format:
Display one batch of request IDs per line.

If the number of requests is invalid, display:

Invalid Number of Requests

If the batch size is invalid, display:

Invalid Batch Size

Sample Input 1:
7
REQ101
REQ102
REQ103
REQ104
REQ105
REQ106
REQ107
3

Sample Output 1:
['REQ101', 'REQ102', 'REQ103']
['REQ104', 'REQ105', 'REQ106']
['REQ107']

Sample Input 2:
0

Sample Output 2:
Invalid Number of Requests

Sample Input 3:
4
REQ101
REQ102
REQ103
REQ104
0

Sample Output 3:
Invalid Batch Size

case=1
input=7
REQ101
REQ102
REQ103
REQ104
REQ105
REQ106
REQ107
3

output=
['REQ101', 'REQ102', 'REQ103']
['REQ104', 'REQ105', 'REQ106']
['REQ107']

case=2
input=5
R1
R2
R3
R4
R5
2

output=
['R1', 'R2']
['R3', 'R4']
['R5']

case=3
input=4
A
B
C
D
5

output=
['A', 'B', 'C', 'D']

case=4
input=1
REQ101
1

output=
['REQ101']

case=5
input=0

output=
Invalid Number of Requests

case=6
input=-5

output=
Invalid Number of Requests

case=7
input=3
REQ1
REQ2
REQ3
0

output=
Invalid Batch Size

case=8
input=2
REQ1
REQ2
-2

output=
Invalid Batch Size
"""
num=int(input())

api=[]

def apis(api,size):
    l=0
    i=size
    while i<len(api)+size:
        yield f"{api[l:i]}"
        l=i
        i+=size

if num<=0:
    print("Invalid Number of Requests")
    
else:

    for _ in range(num):
        api.append(input())
    size=int(input())
    if size<=0:
        print("Invalid Batch Size")
    else:
        for ap in apis(api,size):
            print(ap)
    