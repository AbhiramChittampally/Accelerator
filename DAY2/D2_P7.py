"""
Problem Title: Function Execution Logger

Problem Statement:

A software company wants to maintain logs whenever a function
is executed. Before running a function, the system should display
a message indicating that the function execution has started.
After the function completes, another message should indicate that
the execution has finished.

Design a decorator to implement this logging mechanism and apply
it to a function that greets a customer.

Requirements:
1. Use a decorator without arguments.
2. Preserve the original function metadata using functools.wraps.

Input Format:
Customer Name

Output Format:
Display the start message, greeting message, and completion message.

Sample Input:
Ravi

Sample Output:
Function Execution Started
Hello Ravi
Function Execution Completed
"""

from functools import wraps

name=input()



def logger(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Function Execution Started")
        
        func(*args,**kwargs)
        
        print("Function Execution Completed")
        
        
    return wrapper    
    
@logger
def greet(name):
    print(f"Hello {name}")
greet(name)