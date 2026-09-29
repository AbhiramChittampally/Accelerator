"""

Problem Statement:

An e-commerce company wants to recommend the best products
to its customers based on customer ratings.

Each product record contains:

Product ID
Product Name
Product Price
Customer Rating

The product price may be either an integer or a
floating-point value.

The recommendation system evaluates products using two
different methods.

Method 1:
Find the highest rated product using a traditional
for loop.

Method 2:
Find the highest rated product using Python's built-in
max() function.

Instead of measuring execution time, compare the
performance by counting the number of operations
performed by each method.

Store all product records using a dictionary where

Product ID → (Product Name, Product Price, Rating)

The functions should use Python Type Hints.

The product price should use Union[int, float].

After processing all products:

• Display products sorted in descending order of rating.

• Display the highest rated product using both methods.

• Display the number of operations performed by each method.

• Display the better performing method.

Requirements:
-------------
1. Store product records using a dictionary.
2. Use Python Type Hints.
3. Use Union[int, float].
4. Implement Method 1 using a for loop.
5. Implement Method 2 using max().
6. Sort products using a lambda expression.
7. Count the number of operations.
8. Display the better performing method.

Input Format:
-------------
First line contains the number of products N.

Next N sets contain:

Product ID
Product Name
Product Price
Customer Rating

Output Format:
--------------
Recommended Products:

P101 -> Laptop -> 65000 -> 4.9
P103 -> Camera -> 35000 -> 4.8
P102 -> Mobile -> 25000 -> 4.5

Method 1 Highest Rating : 4.9

Method 2 Highest Rating : 4.9

Method 1 Operations : 3

Method 2 Operations : 1

Better Performing Method : Method 2

Sample Input:
-------------
3
P101
Laptop
65000
4.9
P102
Mobile
25000
4.5
P103
Camera
35000
4.8

Sample Output:
--------------
Recommended Products:
P101 -> Laptop -> 65000 -> 4.9
P103 -> Camera -> 35000 -> 4.8
P102 -> Mobile -> 25000 -> 4.5

Method 1 Highest Rating : 4.9

Method 2 Highest Rating : 4.9

Method 1 Operations : 3

Method 2 Operations : 1

Better Performing Method : Method 2

Test Cases:
-----------

case=1
input=
3
P101
Laptop
65000
4.9
P102
Mobile
25000
4.5
P103
Camera
35000
4.8

output=
Recommended Products:
P101 -> Laptop -> 65000 -> 4.9
P103 -> Camera -> 35000 -> 4.8
P102 -> Mobile -> 25000 -> 4.5

Method 1 Highest Rating : 4.9

Method 2 Highest Rating : 4.9

Method 1 Operations : 3

Method 2 Operations : 1

Better Performing Method : Method 2


case=2
input=
2
P201
Keyboard
1200
4.3
P202
Mouse
800
4.7

output=
Recommended Products:
P202 -> Mouse -> 800 -> 4.7
P201 -> Keyboard -> 1200 -> 4.3

Method 1 Highest Rating : 4.7

Method 2 Highest Rating : 4.7

Method 1 Operations : 2

Method 2 Operations : 1

Better Performing Method : Method 2


case=3
input=
1
P301
Monitor
15000
4.8

output=
Recommended Products:
P301 -> Monitor -> 15000 -> 4.8

Method 1 Highest Rating : 4.8

Method 2 Highest Rating : 4.8

Method 1 Operations : 1

Method 2 Operations : 1

Better Performing Method : Both Methods


case=4
input=
0

output=
Invalid Number of Products


case=5
input=
2
P401
Printer
12000
4.5
P402
Scanner
9000
5.5

output=
Invalid Rating
"""
from typing import Union, Dict, Tuple


def method1(products: Dict[str, Tuple[str, Union[int, float], float]]) -> Tuple[float, int]:
    high = -1.0
    operations = 0

    for value in products.values():
        operations += 1
        if value[2] > high:
            high = value[2]

    return high, operations


def method2(products: Dict[str, Tuple[str, Union[int, float], float]]) -> Tuple[float, int]:
    high = max(products.values(), key=lambda x: x[2])[2]
    return high, 1


n = int(input())

if n <= 0:
    print("Invalid Number of Products")

else:
    products: Dict[str, Tuple[str, Union[int, float], float]] = {}
    valid = True
    for _ in range(n):
        pid = input()
        name = input()
        price: Union[int, float] = float(input())
        if price == int(price):
            price = int(price)
        rating = float(input())
        if rating < 0 or rating > 5:
            valid = False

        products[pid] = (name, price, rating)

    if not valid:
        print("Invalid Rating")

    else:
        print("Recommended Products:")

        sproducts = sorted(
            products.items(),
            key=lambda x: x[1][2],
            reverse=True
        )

        for pid, (name, price, rating) in sproducts:
            print(f"{pid} -> {name} -> {price} -> {rating}")

        high1, op1 = method1(products)
        high2, op2 = method2(products)
        print()
        print(f"Method 1 Highest Rating : {high1}")
        print()
        print(f"Method 2 Highest Rating : {high2}")
        print()
        print(f"Method 1 Operations : {op1}")
        print()
        print(f"Method 2 Operations : {op2}")
        print()
        if op1 < op2:
            print("Better Performing Method : Method 1")
        elif op2 < op1:
            print("Better Performing Method : Method 2")
        else:
            print("Better Performing Method : Both Methods")