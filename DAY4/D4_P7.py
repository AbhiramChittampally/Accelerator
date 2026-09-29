"""


Problem Statement:

A blood donation camp wants to determine whether a person
is eligible to donate blood based on age.

The eligibility rules are:

1. If age is less than 18 years,
   the person is not eligible to donate blood.
   Raise a custom exception and display:

   Not Eligible for Blood Donation

2. If age is between 18 and 44 years (inclusive),
   display:

   Eligible for Blood Donation

3. If age is greater than 44 years,
   raise a custom exception and display:

   Crossed Eligibility Age

Requirements:
1. Create a user-defined exception.
2. Use raise keyword.
3. Use try-except block.
4. Use if-elif-else conditions.

Input Format:
Age

Output Format:
Display the eligibility status.

Sample Input 1:
16

Sample Output 1:
Not Eligible for Blood Donation

Sample Input 2:
25

Sample Output 2:
Eligible for Blood Donation

Sample Input 3:
50

Sample Output 3:
Crossed Eligibility Age


case=1
input=16

output=
Not Eligible for Blood Donation

case=2
input=18

output=
Eligible for Blood Donation

case=3
input=44

output=
Eligible for Blood Donation

case=4
input=45

output=
Crossed Eligibility Age
"""
class NotEligible(Exception):
    pass
class CrossedAge(Exception):
    pass
try:
    age=int(input())
    if age<18:
        raise NotEligible
    elif age>=18 and age<=44:
        print("Eligible for Blood Donation")
    else:
        raise CrossedAge
except NotEligible:
    print("Not Eligible for Blood Donation")
except CrossedAge:
    print("Crossed Eligibility Age")
except:
    print("error")