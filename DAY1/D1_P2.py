"""
Problem Statement:
Given the ages of students, print only the ages of students eligible
to vote (age >= 18) using list comprehension.

Input Format:
Space-separated integers representing ages.

Output Format:
Print the list of eligible ages.

Sample Input:
16 20 18 15 22

Sample Output:
[20, 18, 22]
"""
nums=list(map(int,input().split()))
ans=[x for x in nums if x>=18]
print(ans)
