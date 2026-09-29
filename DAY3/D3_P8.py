"""
Problem Statement:

A browser stores a website URL. Create a class that initializes
the URL using a constructor and extracts:

1. Protocol
2. Domain Name
3. Top-Level Domain

Input Format:
URL

Output Format:
Protocol
Domain
Extension

Sample Input:
https://www.google.com

Sample Output:
Protocol: https
Domain: google
Extension: com
"""
from dataclasses import dataclass

@dataclass
class URL:
    
    protocol:str
    domain:str
    extension:str
    
    def __init__(self,uri):
        parts=uri.split("://")
        self.protocol=parts[0]
        self.domain=parts[1].split(".")[1]
        self.extension=parts[1].split(".")[2]
    def __str__(self):
        return f"Protocol: {self.protocol}\nDomain: {self.domain}\nExtension:{self.extension}"
    
uri=input()
print(URL(uri))