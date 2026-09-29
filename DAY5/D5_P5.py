"""

Problem Statement:

A smart water tank receives water continuously during
each filling cycle.

The system should generate and display the water level
after every filling cycle until the tank becomes full.

If the water added during a filling cycle exceeds the
remaining tank capacity, the water level should be
adjusted to the maximum tank capacity.

When the tank becomes full, display:

Tank Full

If the tank capacity is less than or equal to zero,
display:

Invalid Tank Capacity

If the amount of water added per cycle is less than
or equal to zero, display:

Invalid Water Addition Value

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate water levels one by one.
4. Validate the tank capacity.
5. Validate the water addition value.

Input Format:
First line contains the tank capacity.

Second line contains the amount of water added during
each filling cycle.

Output Format:
Display the water level after every filling cycle.

When the tank becomes full, display:

Tank Full

If the tank capacity is invalid, display:

Invalid Tank Capacity

If the water addition value is invalid, display:

Invalid Water Addition Value


case=1
input=100
25

output=
25
50
75
100
Tank Full

case=2
input=100
40

output=
40
80
100
Tank Full

case=3
input=100
0

output=
Invalid Water Addition Value

case=4
input=100
-10

output=
Invalid Water Addition Value

case=5
input=80
30

output=
30
60
80
Tank Full

case=6
input=0
20

output=
Invalid Tank Capacity

case=7
input=-100
20

output=
Invalid Tank Capacity
"""
capac=int(input())
add=int(input())

def capacity(capac,add):
    tank=0
    while tank<capac:
        tank+=add
        if tank>capac:
            tank=capac
            
        yield tank
    print("Tank Full")

if capac<=0:
    print("Invalid Tank Capacity")
elif add<=0:
    print("Invalid Water Addition Value")
else:
    for cap in capacity(capac,add):
        print(cap)
    