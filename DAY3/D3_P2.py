"""

Problem Statement:

Given a list of integers, group numbers based on
their last digit.

Input Format:
Number of integers
Integers

Output Format:
Dictionary where key = last digit
value = list of numbers having that digit

Sample Input:
6
12
25
32
45
18
28

Sample Output:
{2: [12, 32], 5: [25, 45], 8: [18, 28]}
"""

num=int(input())
mydict={}
for _ in range(num):
    n=int(input())
    r=n%10
    
    if r not in mydict:
        mydict[r]=[]
    mydict[r].append(n)   
        
    
    
print(mydict)
