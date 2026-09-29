"""

Problem Statement:

A digital library stores issued book details in a file.

Whenever the librarian starts updating the issued book
records, the system should automatically open the file.

After all records are updated, the system should
automatically close the file.

The system should also display appropriate messages
when entering and exiting the context.

If the number of books is less than or equal to zero,
display:

Invalid Number of Books

Requirements:
1. Create a Context Manager using __enter__() and __exit__().
2. Open the file inside __enter__().
3. Close the file inside __exit__().
4. Store Book ID and Student Name.
5. Write records to the file.

Input Format:
First line contains the number of issued books.

Next N sets contain:

Book ID
Student Name

Output Format:

Opening Library File...
Book Records Updated Successfully
Closing Library File...

If the number of books is invalid, display:

Invalid Number of Books

Sample Input:
2
B101
Ravi
B102
Priya

Sample Output:
Opening Library File...
Book Records Updated Successfully
Closing Library File...

case=1
input=2
B101
Ravi
B102
Priya

output=
Opening Library File...
Book Records Updated Successfully
Closing Library File...

case=2
input=1
B201
Anu

output=
Opening Library File...
Book Records Updated Successfully
Closing Library File...

case=3
input=3
B101
Ravi
B102
Priya
B103
Rahul

output=
Opening Library File...
Book Records Updated Successfully
Closing Library File...

case=4
input=0

output=
Invalid Number of Books

case=5
input=-2

output=
Invalid Number of Books

"""
class Library:
    def __enter__(self):
        print("Opening Library File...")
        return self
    def __exit__(self,a,b,c):
        print("Closing Library File...")

n=int(input())
if n<=0:
    print("Invalid Number of Books")
else:
    for _ in range(n):
        book=input()
        student=input()
    with Library():
        
        print("Book Records Updated Successfully")