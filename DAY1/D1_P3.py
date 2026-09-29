"""
Problem Statement:
Generate a dictionary where numbers from 1 to N are mapped to their cubes
using dictionary comprehension.

Input Format:
A single integer N.

Output Format:
Print the dictionary.

Sample Input:
4

Sample Output:
{1: 1, 2: 8, 3: 27, 4: 64}
"""


n=int(input())
if n<=0:
    print({0:0})
else:
    ans={x:x**3 for x in range(1,n+1)}
    print(ans)
