"""
Problem Title: User Login Retry System

Problem Statement:

A banking application allows users to retry login attempts
multiple times before blocking access.

The system should retry the login function three times with
a delay of one second between attempts.

Input Format:
User Name

Output Format:
Display login attempts.

Sample Input:
Ravi

Sample Output:
Attempt 1
Login failed for Ravi
Attempt 2
Login failed for Ravi
Attempt 3
Login failed for Ravi
"""
from functools import wraps
import time


name=input()


def retry(attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for i in range (1,attempts+1):
                print(f"Attempt {i}")
                func(*args,**kwargs)
                if i!=attempts:
                    time.sleep(1)
        return wrapper    
    return decorator


@retry(3)
def login(name):
    print(f"Login failed for {name}")
login(name)
