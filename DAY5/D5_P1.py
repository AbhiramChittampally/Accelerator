"""


Problem Statement:

A bank ATM dispenses cash using the available denominations
₹500, ₹200 and ₹100.

Given a withdrawal amount, generate the currency notes
one by one using a generator.

The ATM should always dispense the highest denomination first.

If the withdrawal amount is less than or equal to zero,
display:

Invalid Withdrawal Amount

If the withdrawal amount is positive but less than the
smallest available denomination (₹100), display:

No Cash Dispensed

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate currency notes one by one.
4. Validate the withdrawal amount.

Input Format:
First line contains the withdrawal amount.

Output Format:
Display the dispensed currency notes.

If the withdrawal amount is invalid, display:

Invalid Withdrawal Amount

If no currency note can be dispensed, display:

No Cash Dispensed

Sample Input 1:
1800

Sample Output 1:
500
500
500
200
100

Sample Input 2:
50

Sample Output 2:
No Cash Dispensed

Sample Input 3:
0

Sample Output 3:
Invalid Withdrawal Amount

Sample Input 4:
-500

Sample Output 4:
Invalid Withdrawal Amount

case=1
input=1800

output=
500
500
500
200
100

case=2
input=1000

output=
500
500

case=3
input=700

output=
500
200

case=4
input=100

output=
100

case=5
input=2500

output=
500
500
500
500
500

case=6
input=50

output=
No Cash Dispensed

case=7
input=99

output=
No Cash Dispensed

"""

def atm(amount):
    notes=[500,200,100]
    for note in notes:
        while amount>=note:
            yield note
            amount-=note
            
amount=int(input())
if amount<=0:
    print("Invalid Withdrawal Amount")
elif amount < 100:
    print("No Cash Dispensed")
else:
    for note in atm(amount):
        print(note)