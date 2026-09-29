"""
Problem Statement:

A grayscale image is represented using a NumPy 2D array.

Each element of the array represents the intensity of one pixel.

The pixel intensity ranges from 0 to 255.

An image processing application wants to increase the brightness of every pixel by a given brightness factor.

The brightness increment should be performed using NumPy Broadcasting without using nested loops.

If the updated pixel value becomes greater than 255, it should be clipped to 255.

Requirements:
-------------
1. Store the image using a NumPy array.
2. Convert the input into a matrix using reshape().
3. Increase brightness using Broadcasting.
4. Use np.clip() to maintain pixel values between
   0 and 255.
5. Display the enhanced image.

Input Format:
-------------
First line contains the number of rows R.

Second line contains the number of columns C.

Next R × C lines contain pixel values.

Last line contains the brightness increment.

Output Format:
--------------
Enhanced Image:

<row1>

<row2>

...

If number of rows <= 0 display

Invalid Number of Rows

If number of columns <= 0 display

Invalid Number of Columns

If any pixel value is less than 0 or greater than 255

display

Invalid Pixel Value

If brightness increment is negative

display

Invalid Brightness

Sample Input:
-------------
2
3
100
120
150
200
220
250
20

Sample Output:
--------------
Enhanced Image:
120 140 170
220 240 255


Test Cases
----------

case=1
input=
2
3
100
120
150
200
220
250
20
output=
Enhanced Image:
120 140 170
220 240 255


case=2
input=
3
3
50
60
70
80
90
100
110
120
130
30
output=
Enhanced Image:
80 90 100
110 120 130
140 150 160


case=3
input=
1
4
240
245
250
255
15
output=
Enhanced Image:
255 255 255 255

case=4
input=
0
3
output=
Invalid Number of Rows

case=5
input=
2
2
100
280
150
200
20
output=
Invalid Pixel Value
"""
import numpy as np

n=int(input())
if n<=0:
    print("Invalid Number of Rows")
else:
        
    m=int(input())
    if m<=0:
        print("Invalid Number of Columns")
    else:
        valid=True
        pixs=[]
        for _ in range(n*m):
            p=int(input())
            if p<0 or p>255:
                valid=False
            pixs.append(p)
        if not valid:
            print("Invalid Pixel Value")
        else:
            pixs=np.array(pixs)
            pixs=pixs.reshape(n,m)
            bright=int(input())
            pixs+=bright
            pixs=np.clip(pixs,0,255)
            
            print("Enhanced Image:")
            for row in pixs:
                print(*row)