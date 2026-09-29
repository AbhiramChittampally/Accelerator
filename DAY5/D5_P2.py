"""

Problem Statement:

A cricket analytics company records runs scored on each ball.

Generate the cumulative score after every ball using a generator.

Requirements:
1. Use yield.
2. Maintain running total.
3. Generate score after each ball.

Input Format:
Number of Balls

Runs scored on each ball

Output Format:
Display cumulative scores.

Sample Input:
6
1
4
0
2
6
1

Sample Output:
1
5
5
7
13
14


case=1
input=6
1
4
0
2
6
1

output=
1
5
5
7
13
14

case=2
input=5
2
2
2
2
2

output=
2
4
6
8
10

case=3
input=4
6
6
6
6

output=
6
12
18
24

case=4
input=3
0
0
0

output=
0
0
0

case=5
input=1
4

output=
4

case=6
input=0

output=
Invalid Number of Balls

case=7
input=-2

output=
Invalid Number of Balls

case=8
input=3
4
-1
2

output=
Invalid Runs
"""
def scoretot(runs):
    total=0;
    for run in runs:
        total+=run
        yield total

n=int(input())
if n<=0:
    print("Invalid Number of Balls")
    
else:
    runs=[]
    valid=True
    for _ in range(n):
        r=int(input())
        if r<0:
            valid=False
        
        runs.append(r)
    if not valid:
        print("Invalid Runs")
    else:
        for s in scoretot(runs):
            print(s)