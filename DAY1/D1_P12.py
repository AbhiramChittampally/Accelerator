"""
Problem Statement:
Overload the + operator to add pages of two books.

Input Format:
Pages in first book
Pages in second book

Output Format:
Print total pages.

Sample Input:
100
150

Sample Output:
250
"""
class Book:
    def __init__(self,pages):
        self.pages=pages
    def __add__(self,other):
        if isinstance(other,Book):
            return self.pages + other.pages
        return NotImplemented    
p1=Book(int(input()))   
p2=Book(int(input()))     
print(p1+p2)