"""
Problem Statement:
A teacher wants to analyze the square of roll numbers from 1 to N.
Given an integer N, generate a list containing the square of each
number using list comprehension.

Input Format:
A single integer N.

Output Format:
Print a list of squares.

Sample Input:
5

Sample Output:
[1, 4, 9, 16, 25]
"""
n=int(input())
ans=[num**2 for num in range(1,n+1)]
print(ans)
