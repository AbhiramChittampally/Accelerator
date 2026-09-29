"""

Problem Statement:

A cyber security company wants to analyze passwords created
by users.

For each password:
1. Determine its length.
2. Count the number of vowels present.
3. Display passwords sorted according to their length.

Requirements:
1. Read multiple passwords.
2. Analyze each password.
3. Display password information in ascending order of length.

Input Format:
First line contains an integer N representing the number of passwords.

Next N lines contain password strings.

Output Format:
Display a list containing:
(Password, Length, Number of Vowels)

Sample Input:
3
Python123
Admin@456
AI2025

Sample Output:
[('AI2025', 6, 2), ('Python123', 9, 1), ('Admin@456', 9, 3)]
"""
from dataclasses import dataclass,field

@dataclass(order=True)
class Passwords:
    length:int
    password:str=field(compare=False)
    vowel:int=field(compare=False)
n=int(input())
passes=[]
for _ in range(n):
    
    name=input()
    vowels=0;
    for i in name:
        if i in "aeiouAEIOU":
            
            vowels+=1
    passes.append(Passwords(len(name),name,vowels))
passes.sort();


results=[]
for pss in passes:
    results.append((pss.password, pss.length, pss.vowel))

print(results)
    
    
    
    
