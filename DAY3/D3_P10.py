"""

Problem Statement:

A research organization stores citation counts of published papers.
Duplicate citation counts may exist.

The system should:

1. Remove duplicate citation counts.
2. Calculate the total citation count.
3. Sort citation counts in descending order.
4. Display report information using a class.

Requirements:
1. Use list operations and sets.
2. Use *args to compute total citations.
3. Use lambda while sorting.
4. Display object information using __repr__().

Input Format:
Number of Papers
Citation Counts

Output Format:
ResearchReport(total=?, citations=?)

Sample Input:
6
20
15
20
10
40
15

Sample Output:
ResearchReport(total=85, citations=[40, 20, 15, 10])
"""


from dataclasses import dataclass

@dataclass
class Report:
    total:int
    citations:list
    def __repr__(self):
        return f"ResearchReport(total={self.total}, citations={self.citations})"
    
    
    
def tot(*args):
    return sum(args)
num=int(input())
cits=[]
for _ in range(num):
    n=int(input())
    cits.append(n)
cits=list(set(cits))    
cits.sort(key=lambda x: -x)    
total=tot(*cits)
print(Report(total,cits))





