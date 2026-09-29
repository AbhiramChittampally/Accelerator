"""

Problem Statement:
Write a function that accepts any number of integers and returns
their sum using *args.

Sample Input:
10 20 30 40

Sample Output:
100
"""

def add(*args):
    return sum(args)
nums=list(map(int,input().split()))    
print(add(*nums))
    
    
