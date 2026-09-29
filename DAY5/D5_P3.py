"""

Problem Statement:

A college maintains attendance records for students.

Instead of displaying the complete attendance sheet at once,
the system should generate one student's attendance record
at a time using a generator.

Each attendance record consists of:

Student Name
Attendance Percentage

If the number of students is less than or equal to zero,
display:

Invalid Number of Students

If the attendance percentage is less than 0 or greater than 100,
display:

Invalid Attendance Percentage

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate one attendance record at a time.
4. Validate the number of students.
5. Validate attendance percentage.

Input Format:
First line contains the number of students.

Next N sets of input contain:

Student Name
Attendance Percentage

Output Format:
Display each student's attendance record.

Sample Input 1:
3
Ravi
92
Priya
85
Rahul
76

Sample Output 1:
Ravi - 92%
Priya - 85%
Rahul - 76%

Sample Input 2:
0

Sample Output 2:
Invalid Number of Students

Sample Input 3:
2
Ravi
105
Priya
80

Sample Output 3:
Invalid Attendance Percentage

case=1
input=
3
Ravi
92
Priya
85
Rahul
76

output=
Ravi - 92%
Priya - 85%
Rahul - 76%

case=2
input=
2
Anu
100
Ram
98

output=
Anu - 100%
Ram - 98%

case=3
input=
1
Vishal
80

output=
Vishal - 80%

case=4
input=
0

output=
Invalid Number of Students

case=5
input=
-2

output=
Invalid Number of Students

case=6
input=
2
Ravi
105
Priya
90

output=
Invalid Attendance Percentage

case=7
input=
2
Ravi
-5
Priya
90

output=
Invalid Attendance Percentage
"""


def students(stud):
    for key,value in stud.items():
        yield f"{key} - {value}%"
num=int(input())
stud={}


if num<=0:
    print("Invalid Number of Students")
else:
    valid = True
    for _ in range(num):
        name=input()
        perc=int(input())
        stud[name]=perc
        if perc<0 or perc>100:
            valid = False
    if not valid:
        print("Invalid Attendance Percentage")
    else:
        for stu in students(stud):
            print(stu)