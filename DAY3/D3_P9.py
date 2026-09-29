"""

Problem Statement:

A DNA sequence contains characters A, T, G and C.

Create a class that stores the sequence using a constructor and
displays:

1. Length of sequence
2. Count of A
3. Count of G

Input Format:
DNA Sequence

Output Format:
Length
Count of A
Count of G

Sample Input:
ATGCGATAA

Sample Output:
9
4
2
"""
from dataclasses import dataclass

@dataclass
class Sequence:
    name:str
    lenth:int
    lena:int
    leng:int
    def __str__(self):
        return f"{self.lenth}\n{self.lena}\n{self.leng}"
seq=input()
a=0
g=0
for i in seq:
    if i=="A":
        a+=1
    if i=="G":
        g+=1
sequence=Sequence(seq,len(seq),a,g)
print(sequence)
