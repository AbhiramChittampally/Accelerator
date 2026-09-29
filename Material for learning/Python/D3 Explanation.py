//Example without decorator

def greet():
    print("Hello")

greet()

Output:

Hello

//
Suppose we want:

Before Function
Hello
After Function


//One way (not reusable)
------------------------
def greet():

    print("Before Function")

    print("Hello")

    print("After Function")

//But then every function must contain these statements:

def add():

    print("Before Function")

    print("Adding")

    print("After Function")


//This causes code duplication.


Wrapper's job
---------------

The wrapper surrounds the original function.
-----------------------------------------------

def logger(func):

    def wrapper():

        print("Before Function")

        func()

        print("After Function")

    return wrapper

@logger
def greet():

    print("Hello")


//Python internally does:

greet = logger(greet)


//Suppose both functions need the same statements:
def greet():

    print("Before Function")

    print("Hello")

    print("After Function")


def add():

    print("Before Function")

    print("10 + 20 =", 10 + 20)

    print("After Function")

//Instead, we write them once inside the wrapper:

def logger(func):

    def wrapper():

        print("Before Function")

        func()          # Execute whichever function was passed

        print("After Function")

    return wrapper

//Now apply the same decorator to multiple functions:

@logger
def greet():

    print("Hello")


@logger
def add():

    print("10 + 20 =", 10 + 20)


greet()

add()


Output
---------
Before Function
Hello
After Function

Before Function
10 + 20 = 30
After Function




Importing Your Own Function
---------------------------
functions.py
---------------
def wrapper():
    print("Hello")

Then another file can do:

main.py
-------------
from functions import wrapper

wrapper()

Output:

Hello

Here:

wrapper is your own function.
Python is importing it from functions.py.