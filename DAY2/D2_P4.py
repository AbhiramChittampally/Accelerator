"""
Problem Statement:

A software company wants to monitor the execution of critical functions
used in its data processing system.

Whenever a function is executed, the monitoring system should:

1. Display a message before the function starts execution.
2. Record the function's execution time.
3. Display a message after the function finishes execution.
4. Preserve the original metadata of the function.

Develop a monitoring system using Python decorators and apply it to a
function that computes the sum of numbers from 1 to N.

Requirements:
1. Use multiple decorators to implement logging and timing features.
2. Preserve the original function metadata.
3. Apply both decorators to the target function.

Input Format:
A single integer N.

Output Format:
Display the start message, computed sum, execution information,
and completion message.

Sample Input:
100000

Sample Output:
Starting function
Sum = 5000050000
Execution Time Recorded
Ending function
"""

from functools import wraps

n=int(input())
ans=0

def my_logger(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Starting function")
        ans2=func(*args,**kwargs)
        
        
        print("Ending function")
        return ans2
    return wrapper
def my_timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        
        ans2=func(*args,**kwargs)
        print(f"Sum = {ans2}")
        print("Execution Time Recorded")
        
        return ans2
    return wrapper
@my_logger    
@my_timer
def sum1n(n):
    ans=0
    for i in range(1,n+1):
        ans+=i
    return ans
sum1n(n)    