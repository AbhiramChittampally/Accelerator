"""
r

Problem Statement:

A cyber security team receives encrypted messages from
different communication channels.

To analyze the message, the team wants to perform the
following operations:

1. Display each character of the message individually
   using a for-each loop.

2. Display the index position and corresponding character
   using range(n).

3. Extract and display characters between two specified
   positions using range(start, end).

4. Display the complete message in reverse order using
   string slicing.

Requirements:
1. Use a for-each loop.
2. Use range() with one argument.
3. Use range() with two arguments.
4. Use string indexing.
5. Use string slicing.

Input Format:
First line contains the encrypted message.

Second line contains the starting position.

Third line contains the ending position.

Output Format:
Display all characters individually.
Display index positions with characters.
Display characters between the specified positions.
Display the reversed message.

Sample Input:
CYBERSECURITY
2
8

Sample Output:
Characters in Message:
C
Y
B
E
R
S
E
C
U
R
I
T
Y

Index and Character:
0 C
1 Y
2 B
3 E
4 R
5 S
6 E
7 C
8 U
9 R
10 I
11 T
12 Y

Characters Between Positions:
B
E
R
S
E
C

Reversed Message:
YTIRUCESREBYC


case=1
input=CYBERSECURITY
2
8

output=
Characters in Message:
C
Y
B
E
R
S
E
C
U
R
I
T
Y
Index and Character:
0 C
1 Y
2 B
3 E
4 R
5 S
6 E
7 C
8 U
9 R
10 I
11 T
12 Y
Characters Between Positions:
B
E
R
S
E
C
Reversed Message:
YTIRUCESREBYC

case=2
input=PYTHON
1
4

output=
Characters in Message:
P
Y
T
H
O
N
Index and Character:
0 P
1 Y
2 T
3 H
4 O
5 N
Characters Between Positions:
Y
T
H
Reversed Message:
NOHTYP


case=3
input=HELLO
0
5

output=
Characters in Message:
H
E
L
L
O
Index and Character:
0 H
1 E
2 L
3 L
4 O
Characters Between Positions:
H
E
L
L
O
Reversed Message:
OLLEH

case=4
input=PROGRAMMING
3
7

output=
Characters in Message:
P
R
O
G
R
A
M
M
I
N
G
Index and Character:
0 P
1 R
2 O
3 G
4 R
5 A
6 M
7 M
8 I
9 N
10 G
Characters Between Positions:
G
R
A
M
Reversed Message:
GNIMMARGORP

case=5
input=DATA
1
3

output=
Characters in Message:
D
A
T
A
Index and Character:
0 D
1 A
2 T
3 A
Characters Between Positions:
A
T
Reversed Message:
ATAD
"""
mess=input()
st=int(input())
end=int(input())
 
print("Characters in Message:" )
for ch in mess:
    print(ch)
print("Index and Character:")
for i in range (0,len(mess)):
    print(f"{i} {mess[i]}")
print("Characters Between Positions:")    
for i in range(st,end):
    print(mess[i])
print("Reversed Message:")
print(mess[::-1])    