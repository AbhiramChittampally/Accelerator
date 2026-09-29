""" 
Problem Statement:

An IoT-based weather monitoring station continuously records
temperature readings from sensors installed across a city.

Instead of storing all temperature readings in memory,
the monitoring system should generate one reading at a time.

If a temperature reading exceeds 45°C, the system should
generate an alert message instead of the temperature.

If the number of readings is less than or equal to zero,
display:

Invalid Number of Readings

If any temperature is less than -20°C or greater than 60°C,
display:

Invalid Temperature

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate one reading at a time.
4. Use conditional yield.
5. Validate the number of readings.
6. Validate temperature values.

Input Format:
First line contains the number of temperature readings.

Next N lines contain the temperature values.

Output Format:
Display each generated reading.

If the temperature is greater than 45°C, display:

ALERT : <temperature>

Otherwise display the temperature.

case=1
input=6
30
35
40
48
50
25

output=
30
35
40
ALERT : 48
ALERT : 50
25

case=2
input=5
46
47
48
49
50

output=
ALERT : 46
ALERT : 47
ALERT : 48
ALERT : 49
ALERT : 50

case=3
input=5
20
25
30
35
40

output=
20
25
30
35
40

case=4
input=4
45
46
44
47

output=
45
ALERT : 46
44
ALERT : 47

case=5
input=1
60

output=
ALERT : 60

case=6
input=1
-20

output=
-20

case=7
input=0

output=
Invalid Number of Readings


case=8
input=3
20
-25
30

output=
Invalid Temperature

case=9
input=4
25
61
30
40

output=
Invalid Temperature
"""

def temperature(temps):
    for temp in temps:
        if temp>45:
            yield f"ALERT : {temp}"
        else:
            yield temp
    
num=int(input())
temps=[]
valid=True
if num<=0:
    print("Invalid Number of Readings")
else:
    for _ in range(num):
        t=int(input())
        if t<-20 or t>60:
            
            valid=False
        temps.append(t)    
    if not valid:
        print("Invalid Temperature")
    else:
        for temp in temperature(temps):
            print(temp)
        