"""

Problem Statement:

A social media company collects hashtags used in user posts.
Since users may enter hashtags in different letter cases,
the company wants to standardize all hashtags by converting
them to lowercase.

The analytics team also wants to identify all unique hashtags
and determine how many times each hashtag was used.

For consistent reporting, the unique hashtags and frequency
information should be displayed in alphabetical order.

Requirements:
1. Convert all hashtags to lowercase.
2. Identify unique hashtags.
3. Count the frequency of each hashtag.
4. Display hashtags in alphabetical order.

Input Format:
First line contains an integer N representing the number of hashtags.

Next N lines contain hashtag names.

Output Format:
Print the list of unique hashtags in alphabetical order.
Print the dictionary containing hashtag frequencies in alphabetical order.

Sample Input:
6
Python
AI
python
ML
AI
Data

Sample Output:
['ai', 'data', 'ml', 'python']
{'ai': 2, 'data': 1, 'ml': 1, 'python': 2}
"""
n=int(input())
mydict={}
w=set()
for _ in range(n):
    word=input().lower()
    
    w.add(word)
    if word not in mydict:
        mydict[word]=1
    else:
        mydict[word]=mydict[word]+1
w=sorted(w)
mydict=dict(sorted(mydict.items()))
print(w)
print(mydict)