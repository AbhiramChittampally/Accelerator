"""


Problem Statement:

An online examination system maintains a question bank for
conducting competitive examinations.

Instead of loading all questions at once, the examination
system generates one question at a time whenever a student
moves to the next question.

Design a generator function to generate questions one by one.

If the number of questions is less than or equal to zero,
display:

Invalid Number of Questions

Requirements:
1. Use a generator function.
2. Use the yield statement.
3. Generate one question at a time.
4. Display the question number along with the question.
5. Validate the number of questions.

Input Format:
First line contains the number of questions.

Next N lines contain the question statements.

Output Format:
Display each generated question with its question number.

If the number of questions is invalid, display:

Invalid Number of Questions

Sample Input 1:
4
What is Python?
Define Generator.
What is yield?
Explain Decorators.

Sample Output 1:
Question 1 : What is Python?
Question 2 : Define Generator.
Question 3 : What is yield?
Question 4 : Explain Decorators.

Sample Input 2:
0

Sample Output 2:
Invalid Number of Questions


case=1
input=4
What is Python?
Define Generator.
What is yield?
Explain Decorators.

output=
Question 1 : What is Python?
Question 2 : Define Generator.
Question 3 : What is yield?
Question 4 : Explain Decorators.

case=2
input=3
HTML
CSS
JavaScript

output=
Question 1 : HTML
Question 2 : CSS
Question 3 : JavaScript

case=3
input=1
Explain OOP Concepts.

output=
Question 1 : Explain OOP Concepts.

case=4
input=5
Question A
Question B
Question C
Question D
Question E

output=
Question 1 : Question A
Question 2 : Question B
Question 3 : Question C
Question 4 : Question D
Question 5 : Question E

case=5
input=0

output=
Invalid Number of Questions

case=6
input=-3

output=
Invalid Number of Questions
"""

def questions(quest):
    i=1
    for q in quest:
        yield f"Question {i} : {q}"
        i+=1
    
num=int(input())
quest=[]
if num <= 0:
    print("Invalid Number of Questions")
else:
    for _ in range(num):
        quest.append(input())
    for q in questions(quest):
        print(q)
    
