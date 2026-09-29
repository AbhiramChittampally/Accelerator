"""

Problem Statement:

Given a string, identify all unique characters and
store the positions at which each character appears.

Input Format:
A string

Output Format:
Dictionary containing character positions.

Sample Input:
banana

Sample Output:
{'b': [0], 'a': [1, 3, 5], 'n': [2, 4]}
"""
name=input()
mydict={}
i=0
for ch in name:
    if ch not in mydict:
        mydict[ch]=[]
    mydict[ch].append(i)
    i+=1
print(mydict)