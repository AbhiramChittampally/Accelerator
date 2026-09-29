"""
Problem Statement:

A bank maintains customer account records for monitoring daily
transactions.

Each customer record consists of:

Account Number
Customer Name
Available Balance

The bank performs two transaction audits every day:

1. Morning Audit
2. Evening Audit

Before generating each audit report, the system should display:

Generating Transaction Report...

using a decorator.

The audit process should automatically execute for both
Morning and Evening sessions using a decorator with arguments.

Customer details should be stored in a dictionary where:

Account Number → (Customer Name, Available Balance)

The account information should be generated one customer
at a time using a generator function.

After generating the report, every generated record should
be verified one by one using an iterator.

If the available balance is less than ₹1000,
display:

Low Balance Alert

Requirements:
1. Use a dictionary.
2. Use a tuple.
3. Use a generator function.
4. Use the yield statement.
5. Use an iterator using iter() and next().
6. Use a decorator.
7. Use a decorator with arguments.
8. Preserve function metadata using functools.wraps.

Input Format:
First line contains the number of customer accounts.

Next N sets of input contain:

Account Number
Customer Name
Available Balance

Output Format:

Morning Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Evening Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

If the number of accounts is less than or equal to zero,
display:

Invalid Number of Accounts

If the balance is negative,
display:

Invalid Balance

Sample Input:
2
ACC101
Ravi
15000
ACC102
Priya
800

Sample Output:
Morning Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Evening Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)


Test cases:
---------------
case=1
input=
2
ACC101
Ravi
15000
ACC102
Priya
800

output=
Morning Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Evening Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 15000
ACC102 -> Priya -> Balance : 800 (Low Balance Alert)

case=2
input=
1
ACC201
Kiran
25000

output=
Morning Audit
Generating Transaction Report...
ACC201 -> Kiran -> Balance : 25000

Verified Records:
ACC201 -> Kiran -> Balance : 25000

Evening Audit
Generating Transaction Report...
ACC201 -> Kiran -> Balance : 25000

Verified Records:
ACC201 -> Kiran -> Balance : 25000

case=3
input=
3
ACC101
Ravi
500
ACC102
Anu
950
ACC103
Rahul
18000

output=
Morning Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 500 (Low Balance Alert)
ACC102 -> Anu -> Balance : 950 (Low Balance Alert)
ACC103 -> Rahul -> Balance : 18000

Verified Records:
ACC101 -> Ravi -> Balance : 500 (Low Balance Alert)
ACC102 -> Anu -> Balance : 950 (Low Balance Alert)
ACC103 -> Rahul -> Balance : 18000

Evening Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 500 (Low Balance Alert)
ACC102 -> Anu -> Balance : 950 (Low Balance Alert)
ACC103 -> Rahul -> Balance : 18000

Verified Records:
ACC101 -> Ravi -> Balance : 500 (Low Balance Alert)
ACC102 -> Anu -> Balance : 950 (Low Balance Alert)
ACC103 -> Rahul -> Balance : 18000

case=4
input=
0

output=
Invalid Number of Accounts

case=5
input=
-2

output=
Invalid Number of Accounts

case=6
input=
2
ACC101
Ravi
-500
ACC102
Priya
1500

output=
Invalid Balance

case=7
input=
2
ACC101
Ravi
1000
ACC102
Priya
999

output=
Morning Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 1000
ACC102 -> Priya -> Balance : 999 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 1000
ACC102 -> Priya -> Balance : 999 (Low Balance Alert)

Evening Audit
Generating Transaction Report...
ACC101 -> Ravi -> Balance : 1000
ACC102 -> Priya -> Balance : 999 (Low Balance Alert)

Verified Records:
ACC101 -> Ravi -> Balance : 1000
ACC102 -> Priya -> Balance : 999 (Low Balance Alert)

"""
from functools import wraps


def logger(func):
    @wraps(func)
    def wrapper(account,balances):
        print("Generating Transaction Report...")
        return func(account,balances)
    return wrapper    

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(account,balances):
            for i in range(1,times+1):
                if i==1:
                    print("Morning Audit")
                else:
                    print("Evening Audit")
                record=list(func(account,balances))
                for rec in record:
                    print(rec)
                print();
                print("Verified Records:")
                it=iter(record)
                while True:
                    try:
                        print(next(it))
                    except StopIteration:
                        break
                if i!=times:
                    print()
        return wrapper
    return decorator
@repeat(2)
@logger
def accounts(account,balances):
    i=0
    for acc,name in account.items():
        if balances[i]<1000:
            yield f"{acc} -> {name} -> Balance : {balances[i]} (Low Balance Alert)"
            
        else:
            yield f"{acc} -> {name} -> Balance : {balances[i]}"
        i+=1    

n=int(input())
if n<=0:
    print("Invalid number of Accounts")
else:
    account={}
    valid=True
    balances=[]
    
    for _ in range(n):
        acc=input()
        name=input()
        bal=int(input())
        
        if bal<0:
            valid=False
        account[acc]=name
        balances.append(bal)
    if not valid:
        print("Invalid Balance")
    else:
        accounts(account,balances)

