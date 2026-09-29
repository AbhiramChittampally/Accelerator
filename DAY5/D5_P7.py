"""
Problem Statement:

A network monitoring system receives a continuous stream of
encrypted data packets.

For efficient transmission, the data stream must be divided
into fixed-size packets before sending them to the destination.

Instead of creating all packets at once, the system should
generate one packet at a time using a generator function.

If the packet size is less than or equal to zero, display:

Invalid Packet Size

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate one packet (chunk) at a time.
4. Use string slicing.
5. Validate the packet size.

Input Format:
First line contains the encrypted data.

Second line contains the packet size.

Output Format:
Display one packet per line.

If the packet size is invalid, display:

Invalid Packet Size

Sample Input 1:
ABCDEFGHIJKLMNOPQRSTUVWXYZ
5

Sample Output 1:
ABCDE
FGHIJ
KLMNO
PQRST
UVWXY
Z

Sample Input 2:
HELLOWORLD
3

Sample Output 2:
HEL
LOW
ORL
D

Sample Input 3:
PYTHON
0

Sample Output 3:
Invalid Packet Size

case=1
input=ABCDEFGHIJKLMNOPQRSTUVWXYZ
5

output=
ABCDE
FGHIJ
KLMNO
PQRST
UVWXY
Z


case=2
input=HELLOWORLD
3

output=
HEL
LOW
ORL
D

case=3
input=PYTHONPROGRAMMING
4

output=
PYTH
ONPR
OGRA
MMIN
G

case=4
input=DATASTREAM
20

output=
DATASTREAM

case=5
input=NETWORK
1

output=
N
E
T
W
O
R
K
"""
def packets(s,size):
    l=0
    i=size
    while i<=len(s)+size:
        yield f"{s[l:i]}"
        l=i
        i+=size


s=input()
size=int(input())
if size<=0:
    print("Invalid Packet Size")
else:
    for pack in packets(s,size):
        print(pack)