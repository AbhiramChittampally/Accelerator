"""


Problem Statement:

An online coding platform stores participant names and their
contest scores.

To prepare the final leaderboard, the platform should:

1. Accept multiple participant scores.
2. Remove duplicate scores.
3. Arrange scores in descending order.
4. Calculate the total score of unique entries.
5. Generate a contest report object.
6. Display report information in a readable format.
7. Log when report generation starts and ends.
8. Retry report generation two times.

Requirements:
1. Use lists, sets and lambda functions.
2. Use *args to calculate the total score.
3. Use __repr__() to display object information.
4. Use decorators and decorator with arguments.
5. Preserve metadata using functools.wraps.

Input Format:
Number of Participants

Participant Name
Participant Score

Output Format:
Display contest reports for each retry attempt.

Sample Input:
5
Ravi
90
Priya
85
Kiran
90
John
70
David
95

Sample Output:
Attempt 1
Report Generation Started
ContestReport(scores=[95, 90, 85, 70], total=340)
Report Generation Finished

Attempt 2
Report Generation Started
ContestReport(scores=[95, 90, 85, 70], total=340)
Report Generation Finished
"""
from dataclasses import dataclass
from functools import wraps
num=int(input())

def totals(*args):
    return sum(args)

@dataclass(order=True)
class Scores:
    mark:list
    total:int
    
    def __repr__(self):
        return f"ContestReport(scores={self.mark}, total={self.total})"


marks=set()
for _ in range(num):
    name=input()
    score=int(input())
    marks.add(score)
    
    

l=list(marks)
l.sort(reverse=True)

def logger(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Report Generation Started")
        result=func(*args,**kwargs)
        print(result)
        print("Report Generation Finished")
        return result
    return wrapper    

def retry(attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for i in range (1,attempts+1):
                print(f"Attempt {i}")
                func(*args,**kwargs)
                
            
        return wrapper
    return decorator    

@retry(2)
@logger
def generate_report():
    total=totals(*l)
    return Scores(l,total)
generate_report()
   
    

