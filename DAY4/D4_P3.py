"""


Problem Statement:

A railway department maintains passenger records.

Create a base class Passenger.

Create two derived classes:

1. SleeperClass
   - Fare = Distance × ₹2

2. ACClass
   - Fare = Distance × ₹4

Override the fare calculation method.

If distance is negative, display:

Invalid Distance

Input Format:
Class Type (Sleeper / AC)
Passenger Name
Distance

Output Format:
Display fare amount.

Sample Input:
AC
Priya
100

Sample Output:
Fare = 400
"""
from dataclasses import dataclass

@dataclass
class Passenger:
    name:str
    distance:int
class SleeperClass(Passenger):
    
    def dispfare(self):
        return self.distance*2
class ACClass(Passenger):
    def dispfare(self):
        return self.distance*4


try:
    ct=input().lower()
    name=input()
    distance=int(input())
    if distance<0:
        raise ValueError
    if ct=="ac":
        pasgr=ACClass(name,distance)
    elif ct=="sleeper":
        pasgr=SleeperClass(name,distance)
    else:
        raise TypeError
    print(f"Fare = {pasgr.dispfare()}")    
except ValueError:
    print("Invalid Distance")
except TypeError:
    print("Invalid Class Type")
except Exception as e:
    print(f"{e}")