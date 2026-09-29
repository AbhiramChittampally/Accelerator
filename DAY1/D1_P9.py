"""
Problem Statement:
Perform addition or subtraction using a dispatcher dictionary.

Input Format:
Operation name (add/sub)
First integer
Second integer

Output Format:
Print the result.

Sample Input:
add
10
20

Sample Output:
30
"""
def add(a,b):
    return a+b
def sub(a,b):
    return a-b  
dispatcher={
    "add":add,
    "sub":sub
}

operation=input().strip()
num1=int(input().strip())
num2=int(input().strip())

print(dispatcher[operation](num1,num2))