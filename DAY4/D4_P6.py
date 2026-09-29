"""

Problem Statement:

An insurance company provides policies for:

1. Car
2. Bike

Both inherit from Vehicle.

Override premium calculation methods.

Car Premium = Vehicle Cost × 5%

Bike Premium = Vehicle Cost × 3%

If vehicle cost is negative, display:

Invalid Vehicle Cost

Input Format:
Vehicle Type (Car / Bike)
Vehicle Cost

Output Format:
Display premium amount.

Sample Input:
Car
500000

Sample Output:
Premium = 25000.0

case=1
input=Car
500000

output=
Premium = 25000.0

case=2
input=Bike
100000

output=
Premium = 3000.0

case=3
input=Car
250000

output=
Premium = 12500.0

case=4
input=Bike
75000

output=
Premium = 2250.0

case=5
input=Car
-50000

output=
Invalid Vehicle Cost
"""
from dataclasses import dataclass

@dataclass
class Vehicle:
    vehicle:str
    cost:int
class Car(Vehicle):
    
    def disp(self):
        return f"Premium = {self.cost*0.05}"
class Bike(Vehicle):
    def disp(self):
        return f"Premium = {self.cost*0.03}"
try:
    typ=input().lower()
    cost=int(input())
    
    if cost<0:
        raise ValueError
    if typ=="car":
        obj=Car(typ,cost)
    elif typ=="bike":
        obj=Bike(typ,cost)
    else:
        print("Error")
    print(obj.disp())    
except ValueError:
    print("Invalid Vehicle Cost")
except Exception as e:
    print(f"{e}")