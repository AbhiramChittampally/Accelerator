"""

Problem Statement:

A hospital issues token numbers to patients waiting for
consultation.

Instead of storing all token numbers in a list, the hospital
wants to generate token numbers one by one whenever required.

Design a generator function to generate token numbers.

If the number of patients is less than or equal to zero,
display:

Invalid Number of Patients

Requirements:
1. Use a generator function.
2. Use yield statement.
3. Display token numbers using a loop.
4. Validate the number of patients.

Input Format:
First line contains the number of patients.

Output Format:
Display generated token numbers.

If the number of patients is invalid, display:

Invalid Number of Patients

Sample Input 1:
5

Sample Output 1:
Token-1
Token-2
Token-3
Token-4
Token-5

Sample Input 2:
0

Sample Output 2:
Invalid Number of Patients

Sample Input 3:
-3

Sample Output 3:
Invalid Number of Patie


case=1
input=5

output=
Token-1
Token-2
Token-3
Token-4
Token-5

case=2
input=1

output=
Token-1

case=3
input=3

output=
Token-1
Token-2
Token-3

case=4
input=0

output=
Invalid Number of Patients

case=5
input=-5

output=
Invalid Number of Patients
"""


def token_generator(n):
    for i in range(1,n+1):
        yield f"Token-{i}"

n=int(input())
if n<=0:
    print("Invalid Number of Patients")
else:
    for t in token_generator(n):
        print(t)


