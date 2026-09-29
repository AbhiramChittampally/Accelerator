"""

Problem Statement:
Given visitor IDs containing duplicates, print only unique IDs
using set comprehension.

Input Format:
Space-separated integers.

Output Format:
Print the set of unique IDs.

Sample Input:
101 102 101 103 102 104

Sample Output:
{101, 102, 103, 104}
"""
n=list(map(int,input().split()))
ans={x for x in n}
print(ans)

