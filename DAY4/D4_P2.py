"""


Problem Statement:

A hospital manages billing information for patients.

Create a base class Patient containing patient name and bill amount.

Create two derived classes:

1. InPatient
   - Additional room charge = ₹2000

2. OutPatient
   - Consultation charge = ₹500

Override the bill calculation method in both classes.

The patient type should be accepted irrespective of letter case.
For example:

InPatient
inpatient
INPATIENT
Inpatient

should all be treated as InPatient.

Similarly,

OutPatient
outpatient
OUTPATIENT
Outpatient

should all be treated as OutPatient.

If the bill amount entered is negative, display:

Invalid Bill Amount

If an invalid patient type is entered, display:

Invalid Patient Type

Requirements:
1. Use constructors.
2. Use inheritance.
3. Use method overriding.
4. Use exception handling.
5. Validate user input.
6. Accept patient type irrespective of letter case.

Input Format:
First line contains the patient type
(InPatient or OutPatient).

Second line contains the patient name.

Third line contains the bill amount.

Output Format:
Display the final bill amount.

Sample Input 1:
InPatient
Ravi
5000

Sample Output 1:
Final Bill = 7000

Sample Input 2:
outpatient
Priya
3000

Sample Output 2:
Final Bill = 3500

Sample Input 3:
INPATIENT
John
4500

Sample Output 3:
Final Bill = 6500

Sample Input 4:
Doctor
Ravi
5000

Sample Output 4:
Invalid Patient Type

Sample Input 5:
OutPatient
Kiran
-1000

Sample Output 5:
Invalid Bill Amount
"""
from dataclasses import dataclass

@dataclass
class Patient:
    name:str
    bill:int
    def calculate_bill(self):
        return self.bill
class inPatient(Patient):
    def calculate_bill(self):
        return self.bill+2000
class outPatient(Patient):
    def calculate_bill(self):
        return self.bill+500
        
try:
    pat=input().lower()
    name=input()
    bill=int(input())
    if bill<0:
        raise ValueError
    elif pat=="inpatient":
        p=inPatient(name,bill)
    elif pat=="outpatient":
        p=outPatient(name,bill)
        
    else:
        raise TypeError
    print(f"Final Bill = {p.calculate_bill()}")
except ValueError:
    print("Invalid Bill Amount")
except TypeError:
    print("Invalid Patient Type")
except:
    print("Something went Wrong")
    



