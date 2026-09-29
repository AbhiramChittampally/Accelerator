"""

Problem Statement:

Given N words, identify all unique words and display
them in descending order of their length.

Input Format:
First line contains N.
Next N lines contain words.

Output Format:
Sorted list of unique words.

Sample Input:
6
python
java
python
database
sql
machine

Sample Output:
['database', 'machine', 'python', 'java', 'sql']
"""
from dataclasses import dataclass,field

@dataclass(order=True)
class Words:
    length:int
    name:str
n=int(input())
uwords=set()
for _ in range(n):
    uwords.add(input())
words=[]    
for word in uwords:
    
    length=len(word)
    words.append(Words(length,word))
words.sort(reverse=True)
results=[]
for word in words:
    results.append(word.name)
  
print(results)