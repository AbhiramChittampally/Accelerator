"""


Problem Statement:

A bank establishes a secure transaction session whenever
a customer performs banking operations.

When the transaction session starts, the system should
automatically establish a secure connection.

After all customer transactions are completed, the system
should automatically terminate the session.

The system should display appropriate messages while
opening and closing the transaction session.

Each customer record contains:

Account Number
Customer Name
Transaction Amount

Store the customer details using a dictionary.

If the number of customer records is less than or equal to zero,
display:

Invalid Number of Customers

If the transaction amount is less than or equal to zero,
display:

Invalid Transaction Amount

Requirements:
1. Create a Context Manager using __enter__() and __exit__().
2. Use the with statement.
3. Store customer records using a dictionary.
4. Display all customer transactions.
5. Validate the transaction amount.

Input Format:
First line contains the number of customers.

Next N sets contain:

Account Number
Customer Name
Transaction Amount

Output Format:

Establishing Secure Banking Session...
Customer Transactions:
ACC101 -> Ravi -> 5000
ACC102 -> Priya -> 3000
Banking Session Closed Successfully

If the number of customers is invalid, display:

Invalid Number of Customers

If the transaction amount is invalid, display:

Invalid Transaction Amount

Sample Input:
2
ACC101
Ravi
5000
ACC102
Priya
3000

Sample Output:
Establishing Secure Banking Session...
Customer Transactions:
ACC101 -> Ravi -> 5000
ACC102 -> Priya -> 3000
Banking Session Closed Successfully

case=1
input=
2
ACC101
Ravi
5000
ACC102
Priya
3000

output=
Establishing Secure Banking Session...
Customer Transactions:
ACC101 -> Ravi -> 5000
ACC102 -> Priya -> 3000
Banking Session Closed Successfully


case=2
input=
1
ACC201
Kiran
15000

output=
Establishing Secure Banking Session...
Customer Transactions:
ACC201 -> Kiran -> 15000
Banking Session Closed Successfully


case=3
input=
3
ACC101
Ravi
1000
ACC102
Anu
2500
ACC103
Rahul
4000

output=
Establishing Secure Banking Session...
Customer Transactions:
ACC101 -> Ravi -> 1000
ACC102 -> Anu -> 2500
ACC103 -> Rahul -> 4000
Banking Session Closed Successfully

case=4
input=
0

output=
Invalid Number of Customers

case=5
input=
-2

output=
Invalid Number of Customers

case=6
input=
2
ACC101
Ravi
-500
ACC102
Priya
3000

output=
Invalid Transaction Amount
"""
class Bank:
    def __enter__(self):
        print("Establishing Secure Banking Session...")
    def __exit__(self,a,b,c):
        print("Banking Session Closed Successfully")
n=int(input())
if n<=0:
    print("Invalid Number of Customers")
else:
    customers={}
    valid=True
    for _ in range(n):
        acc=input()
        name=input()
        amount=int(input())
        if amount<=0:
            valid = False
        customers[acc]=(name,amount)
    if not valid:
        print("Invalid Transaction Amount")
    else:
        with Bank():
            print("Customer Transactions")
            for acc,dets in customers.items():
                print(f"{acc} -> {dets[0]} -> {dets[1]}")