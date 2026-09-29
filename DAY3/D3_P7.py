"""
Problem Statement:

Given N words, convert all words to lowercase and determine
how many times each word appears.

Display the words sorted according to:
1. Frequency (descending)
2. Alphabetical order (ascending) when frequencies are equal.

Input Format:
First line contains an integer N.
Next N lines contain words.

Output Format:
Display a list of tuples containing:
(word, frequency)

Sample Input:
7
Apple
banana
apple
Orange
banana
APPLE
orange

Sample Output:
[('apple', 3), ('banana', 2), ('orange', 2)]
"""
num=int(input())
mydict={}
for i in range(num):
    name=input().lower()
    
    if name not in mydict:
        mydict[name]=0
    mydict[name]=mydict[name]+1
result=sorted(mydict.items(), key=lambda x:(-x[1],x[0]))
print(result)    