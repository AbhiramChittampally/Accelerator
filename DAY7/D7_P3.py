
"""
Problem Statement:

A university maintains student records in a list.

To search for a particular student mark, two different
search methods are used.

Method 1:
Linear Search

Method 2:
Binary Search

The program should determine whether the given mark is
present using both methods.

Instead of measuring execution time, compare the
performance by counting the number of comparisons
performed by each method.

The search functions should use Python Type Hints.

After searching, display:

• Search Result
• Number of comparisons made by Method 1
• Number of comparisons made by Method 2
• Faster Search Method

Requirements:
-------------
1. Create two search functions.
2. Use Python Type Hints.
3. Method 1 should implement Linear Search.
4. Method 2 should implement Binary Search.
5. Count the number of comparisons performed.
6. Display the faster search method.

Input Format:
-------------
First line contains the number of student marks N.

Next N lines contain the marks.

Last line contains the search key.

Output Format:
--------------
Search Result : Found

Method 1 Comparisons : <count>

Method 2 Comparisons : <count>

Fastest Method : <Method Name>

If the mark is not found:

Search Result : Not Found

Sample Input:
-------------
5
60
75
80
90
95
90

Sample Output:
--------------
Search Result : Found
Method 1 Comparisons : 4
Method 2 Comparisons : 2
Fastest Method : Method 2

Test Cases:
-----------

case=1
input=5
60
75
80
90
95
90

output=
Search Result : Found
Method 1 Comparisons : 4
Method 2 Comparisons : 2
Fastest Method : Method 2

case=2
input=6
10
20
30
40
50
60
25

output=
Search Result : Not Found
Method 1 Comparisons : 6
Method 2 Comparisons : 3
Fastest Method : Method 2

case=3
input=1
100
100

output=
Search Result : Found
Method 1 Comparisons : 1
Method 2 Comparisons : 1
Fastest Method : Both Methods

case=4
input=0

output=
Invalid Number of Students

case=5
input=3
50
-10
80

output=
Invalid Marks
"""

def linear(marks: list[int], ans: int)->tuple[bool,int]:
    count=0;
    for m in marks:
        count+=1
        if m==ans:
            return True,count
    return False,count        
def binary(marks : list[int], ans : int) -> tuple[bool,int]:
    low=0
    high=len(marks)-1
    count=0;
    while low<=high:
        count += 1
        mid = (low + high) // 2
        if marks[mid] == ans:
            return True, count
        elif ans < marks[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return False, count
        
n=int(input())

if n<=0:
    print("Invalid Number of Students")
else:
    marks=[]
    valid=True
    for _ in range(n):
        mark=int(input())
        if mark<0:
            valid=False
        marks.append(mark)    
    if not valid:
        print("Invalid Marks")
    else:
        marks.sort()
        ans=int(input())
        f1,com1=linear(marks,ans)
        f2,com2=binary(marks,ans)
        if f1:
            print("Search Result : Found")
        else:
            print("Search Result : Not Found")
        print(f"Method 1 Comparisons : {com1}")
        print(f"Method 2 Comparisons : {com2}")
        if com1 < com2:
            print("Fastest Method : Method 1")
        elif com2 < com1:
            print("Fastest Method : Method 2")
        else:
            print("Fastest Method : Both Methods")