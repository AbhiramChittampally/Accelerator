"""

Problem Statement:
A university considers marks greater than or equal to 40 as passing marks.
Print only the passing marks using lambda and filter().

Input Format:
Space-separated integers representing marks.

Output Format:
Print the passing marks.

Sample Input:
35 60 25 80 40

Sample Output:
[60, 80, 40]
"""
nums=list(map(int,input().split()))
ans=list(filter(lambda x:x>=40,nums))
print(ans)

