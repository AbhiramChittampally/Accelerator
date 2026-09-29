"""


Problem Statement:

A smart restaurant receives food orders from multiple
customers.

Whenever order processing starts, the system should
automatically establish an order processing session.

After processing all customer orders, the session should
automatically close irrespective of whether the processing
completes successfully or an exception occurs.

Each customer order contains:

Order ID
Customer Name
Food Item
Quantity
Price Per Item

Customer orders should be stored using a dictionary where:

Order ID → (Customer Name, Food Item, Quantity, Price)

The total bill for every customer should be calculated using
a function.

Create a decorator named:

@restaurant_log

The decorator should display:

Restaurant Session Started...

before executing the billing function and

Restaurant Session Completed...

after the function execution.

Create another decorator factory named:

@discount(percentage)

which applies the given discount percentage to the final bill.

The billing function should accept variable positional
arguments (*args) and keyword arguments (**kwargs).

After calculating all bills, generate the customer bills
one by one using a generator.

The generated bills should then be verified one by one
using an iterator.

If quantity is less than or equal to zero,
display:

Invalid Quantity

If price is less than or equal to zero,
display:

Invalid Price

Requirements:

1. Create a Context Manager using __enter__() and __exit__().
2. Create a decorator.
3. Create a decorator with arguments.
4. Use *args.
5. Use **kwargs.
6. Store records using a dictionary.
7. Generate bills using a generator.
8. Verify bills using an iterator.
9. Use raise and try-except.
10. Automatically close the restaurant session.

Input Format:

First line contains the number of customer orders.

Next N sets contain:

Order ID
Customer Name
Food Item
Quantity
Price Per Item

Output Format:

Opening Restaurant Session...

Restaurant Session Started...

Customer Bills:

O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Completed...

Verified Bills:

O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Closed

If the number of orders is less than or equal to zero,
display:

Invalid Number of Orders

If quantity is invalid,
display:

Invalid Quantity

If price is invalid,
display:

Invalid Price

Sample Input:

3
O101
Ravi
Pizza
2
400
O102
Priya
Burger
3
200
O103
Rahul
Pasta
2
200

Sample Output:

Opening Restaurant Session...

Restaurant Session Started...

Customer Bills:

O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Completed...

Verified Bills:

O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Closed

case=1
input=3
O101
Ravi
Pizza
2
400
O102
Priya
Burger
3
200
O103
Rahul
Pasta
2
200

output=
Opening Restaurant Session...

Restaurant Session Started...

Customer Bills:
O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Completed...

Verified Bills:
O101 -> Ravi -> ₹720
O102 -> Priya -> ₹540
O103 -> Rahul -> ₹360

Restaurant Session Closed

case=2
input=2
O201
Anu
Sandwich
1
150
O202
Kiran
Coffee
2
100

output=
Opening Restaurant Session...

Restaurant Session Started...

Customer Bills:
O201 -> Anu -> ₹135
O202 -> Kiran -> ₹180

Restaurant Session Completed...

Verified Bills:
O201 -> Anu -> ₹135
O202 -> Kiran -> ₹180

Restaurant Session Closed


case=3
input=1
O301
Mahesh
Biryani
4
250

output=
Opening Restaurant Session...

Restaurant Session Started...

Customer Bills:
O301 -> Mahesh -> ₹900

Restaurant Session Completed...

Verified Bills:
O301 -> Mahesh -> ₹900

Restaurant Session Closed

case=4
input=2
O401
Swetha
Pizza
0
300
O402
Ajay
Burger
2
150

output=
Opening Restaurant Session...
Restaurant Session Closed
Invalid Quantity


case=5
input=1
O601
Pooja
Pizza
2
0

output=
Opening Restaurant Session...
Restaurant Session Closed
Invalid Price
"""
from functools import wraps

class Restaurant:
    def __enter__(self):
        print("Opening Restaurant Session...")
        return self
    def __exit__(self,a,b,c):
        print("Restaurant Session Closed")

def discount(percent):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            bill = func(*args, **kwargs)
            return int(bill - bill * percent / 100)

        return wrapper

    return decorator

def restaurant_log(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print()
        print("Restaurant Session Started...")
        print()
        result = func(*args, **kwargs)
        print()
        print("Restaurant Session Completed...")
        return result

    return wrapper

@restaurant_log
def calculate(order):
    print("Customer Bills:")
    
    bills=[]
    for oid,value in order.items():
        name,item,quant,price=value
        @discount(10)
        def bill(*args,**kwargs):
            return quant*price
        total=bill(quant,price=price)
        print(f"{oid} -> {name} -> ₹{total}")
        bills.append((oid,name,total))
    return bills    


def generate(bills):

    for bill in bills:
        yield bill


n=int(input())
if n<=0:
    print("Invalid Number of Orders")
else:
    order={}
    for _ in range(n):
        
        oid=input()
        name=input()
        item=input()
        quant=int(input())
        price=int(input())
        order[oid]=(name,item,quant,price)
    try:
        with Restaurant():
            for val in order.values():
                if val[2]<=0:
                    raise ValueError

                if val[3]<=0:
                    raise TypeError
            bills=calculate(order)     
            print()
            print("Verified Bills:")
            gen=generate(bills)
            it = iter(gen)

            while True:
                try:
                    oid, name, total = next(it)
                    print(f"{oid} -> {name} -> ₹{total}")
                except StopIteration:
                    break
    except ValueError:
            print("Invalid Quantity")
    except TypeError:
            print("Invalid Price")

