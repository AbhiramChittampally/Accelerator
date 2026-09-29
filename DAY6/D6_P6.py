"""
Problem Statement:

A railway reservation system processes passenger ticket bookings.

Whenever a passenger books a ticket, the system should
automatically establish a reservation session.

After processing all passenger bookings, the reservation
session should automatically close, irrespective of whether
the booking is successful or an exception occurs.

Each passenger record contains:

Passenger ID
Passenger Name
Coach Number
Number of Seats Requested

Passenger details should be stored using a dictionary where:

Passenger ID → (Passenger Name, Coach Number, Seats Requested)

The railway supports only the following coaches:

S1
S2
B1
B2

If an invalid coach number is entered, display:

Invalid Coach Number

If the requested seats are less than or equal to zero,
display:

Invalid Seat Count

A passenger can reserve a maximum of 6 seats.

If the requested seats exceed 6, raise a custom exception
and display:

Seats Not Available

Requirements:
1. Create a Context Manager using __enter__() and __exit__().
2. Create a custom exception.
3. Use raise keyword.
4. Use try-except block.
5. Store passenger details using a dictionary.
6. Store passenger information using tuples.
7. Automatically close the reservation session.

Input Format:
First line contains the number of passengers.

Next N sets contain:

Passenger ID
Passenger Name
Coach Number
Seats Requested

Output Format:

Opening Reservation Session...
Reservation Details:
P101 -> Ravi -> S1 -> 2 Seat(s)
P102 -> Priya -> B2 -> 4 Seat(s)
Reservation Session Closed

If the number of passengers is invalid, display:

Invalid Number of Passengers

If the coach number is invalid, display:

Invalid Coach Number

If the seat count is invalid, display:

Invalid Seat Count

If the requested seats exceed 6, display:

Seats Not Available

Sample Input:
2
P101
Ravi
S1
2
P102
Priya
B2
4

Sample Output:
Opening Reservation Session...
Reservation Details:
P101 -> Ravi -> S1 -> 2 Seat(s)
P102 -> Priya -> B2 -> 4 Seat(s)
Reservation Session Closed

case=1
input=2
P101
Ravi
S1
2
P102
Priya
B2
4

output=
Opening Reservation Session...
Reservation Details:
P101 -> Ravi -> S1 -> 2 Seat(s)
P102 -> Priya -> B2 -> 4 Seat(s)
Reservation Session Closed

case=2
input=1
P201
Anu
S2
5

output=
Opening Reservation Session...
Reservation Details:
P201 -> Anu -> S2 -> 5 Seat(s)
Reservation Session Closed

case=3
input=2
P101
Ravi
A1
2
P102
Priya
S1
3

output=
Opening Reservation Session...
Reservation Session Closed
Invalid Coach Number

case=4
input=2
P101
Ravi
S1
0
P102
Priya
B2
2

output=
Opening Reservation Session...
Reservation Session Closed
Invalid Seat Count


case=5
input=2
P101
Ravi
S2
8
P102
Priya
B1
3

output=
Opening Reservation Session...
Reservation Session Closed
Seats Not Available

case=6
input=0

output=
Invalid Number of Passengers

case=7
input=-2

output=
Invalid Number of Passengers
"""

class CoachError(Exception):
    pass
class NotAvailable(Exception):
    pass
class SeatsError(Exception):
    pass

class Passenger:
    def __enter__(self):
        print("Opening Reservation Session...")
        return self
    def __exit__(self,a,b,c):
        print("Reservation Session Closed")
n=int(input())
if n<=0:
    print("Invalid Number of Passengers")
else:
    
    passenger={}
    for _ in range(n):
        ide=input()
        name=input()
        coach=input().lower()
        seats=int(input())
        passenger[ide]=(name,coach,seats)
    try:
        with Passenger():
            for key,value in passenger.items():
                if value[1] not in ["s1","s2","b1","b2"]:
                    raise CoachError
                elif value[2]>6:
                    raise NotAvailable
                elif value[2]<=0:
                    raise SeatsError
            print("Reservation Details:")  
            for key,value in passenger.items():
                print(f"{key} -> {value[0]} -> {value[1].upper()} -> {value[2]} Seat(s)")
    except CoachError:
        print("Invalid Coach Number")
    except NotAvailable:
        print("Seats Not Available")
    except SeatsError:
        print("Invalid Seat Count")