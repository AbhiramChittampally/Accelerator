"""
Problem Statement:

An airport security department verifies passengers before
allowing them to board a flight.

Whenever a passenger enters the security checkpoint,
the system should automatically establish a security
verification session.

After verifying all passengers, the security session
should automatically close, irrespective of whether
verification is successful or an exception occurs.

Each passenger record contains:

Passenger ID
Passenger Name
Passport Number
Security Status

Passenger details should be stored using a dictionary where:

Passenger ID → (Passenger Name, Passport Number, Security Status)

The security status must be either:

CLEARED
HOLD

If the passport number does not start with "PP",
raise a ValueError.

Convert the ValueError into a custom exception
PassportVerificationException using the raise from
statement.

If the security status is not CLEARED or HOLD,
display:

Invalid Security Status

Requirements:
1. Create a Context Manager using __enter__() and __exit__().
2. Create a custom exception.
3. Use raise.
4. Use raise from.
5. Use try-except.
6. Store passenger details using a dictionary.
7. Store passenger information using tuples.
8. Automatically close the security session.

Input Format:
First line contains the number of passengers.

Next N sets contain:

Passenger ID
Passenger Name
Passport Number
Security Status

Output Format:

Opening Security Verification Session...
Passenger Details:
P101 -> Ravi -> PP12345 -> CLEARED
P102 -> Priya -> PP67890 -> HOLD
Security Verification Session Closed

If the number of passengers is less than or equal to zero,
display:

Invalid Number of Passengers

If the passport number is invalid, display:

Invalid Passport Number

If the security status is invalid, display:

Invalid Security Status

Sample Input:
2
P101
Ravi
PP12345
CLEARED
P102
Priya
PP67890
HOLD

Sample Output:
Opening Security Verification Session...
Passenger Details:
P101 -> Ravi -> PP12345 -> CLEARED
P102 -> Priya -> PP67890 -> HOLD
Security Verification Session Closed

case=1
input=2
P101
Ravi
PP12345
CLEARED
P102
Priya
PP67890
HOLD

output=
Opening Security Verification Session...
Passenger Details:
P101 -> Ravi -> PP12345 -> CLEARED
P102 -> Priya -> PP67890 -> HOLD
Security Verification Session Closed


case=2
input=1
P201
Anu
PP99887
CLEARED

output=
Opening Security Verification Session...
Passenger Details:
P201 -> Anu -> PP99887 -> CLEARED
Security Verification Session Closed

case=3
input=2
P101
Ravi
12345
CLEARED
P102
Priya
PP56789
HOLD

output=
Opening Security Verification Session...
Security Verification Session Closed
Invalid Passport Number

case=4
input=2
P101
Ravi
PP12345
WAITING
P102
Priya
PP56789
CLEARED

output=
Opening Security Verification Session...
Security Verification Session Closed
Invalid Security Status

case=5
input=0

output=
Invalid Number of Passengers

case=6
input=-3

output=
Invalid Number of Passengers

case=7
input=1
P501
Kiran
AB12345
CLEARED

output=
Opening Security Verification Session...
Security Verification Session Closed
Invalid Passport Number
"""
class PassError(Exception):
    pass

class Security():
    def __enter__(self):
        print("Opening Security Verification Session...")
        return self
    def __exit__(self,a,b,c):
        print("Security Verification Session Closed")
    
n=int(input())
if n<=0:
    print("Invalid Number of Passengers")
else:
    passenger={}
    for _ in range(n):
        pid=input()
        name=input()
        ppn=input()
        status=input().upper()
        passenger[pid]=(name,ppn,status)
    try:
        with Security():
            for value in passenger.values():
                try:
                    if not value[1].startswith("PP"):
                        raise ValueError
                except ValueError:
                    raise PassError from ValueError
                if value[2] not in ["CLEARED","HOLD"]:
                    raise TypeError
            print("Passenger Details:")        
            for key,value in passenger.items():
                print(f"{key} -> {value[0]} -> {value[1]} -> {value[2]}")

    except PassError:
        print("Invalid Passport Number")
    except TypeError:
        print("Invalid Security Status")
        
        