WEEK 4 — DAY 16
PROBLEM 1 — SMART EMPLOYEE ATTENDANCE PREDICTION

Difficulty: Medium
Platform: Google Colab
Language: Python
Libraries: Pandas
Submission: Google Colab Notebook

Problem Statement

A company wants to predict whether an employee is likely to arrive late to work. The company has collected historical employee attendance information containing distance from home, travel time, previous late arrivals, weather condition, transport type, and whether the employee actually arrived late.

Currently, the company uses manually written rules to identify employees who may be late. For example, an employee may be considered likely to be late if the distance from home is greater than 15 km and the travel time is greater than 60 minutes.

The company wants to understand how a Machine Learning approach can learn patterns from historical data instead of depending only on manually written rules.

You are required to prepare the dataset, analyze the available information, apply a simple rule-based prediction, and explain how the same problem could later be solved using Machine Learning.

Sample Input
--------------
Employee_ID,Distance_KM,Travel_Time_Min,Previous_Late_Count,Weather,Transport,Late
E101,5,20,1,Clear,Bus,No
E102,18,65,5,Rain,Bus,Yes
E103,7,30,0,Clear,Car,No
E104,22,75,7,Rain,Bus,Yes
E105,10,40,2,Cloudy,Bike,No


TASK 1 — Create the Dataset

Create the above dataset using Pandas.

Expected Output
---------------
  Employee_ID  Distance_KM  Travel_Time_Min  Previous_Late_Count Weather Transport Late
0       E101            5               20                    1   Clear       Bus   No
1       E102           18               65                    5    Rain       Bus  Yes
2       E103            7               30                    0   Clear       Car   No
3       E104           22               75                    7    Rain       Bus  Yes
4       E105           10               40                    2  Cloudy      Bike   No


TASK 2 — Display Dataset Information

Display the number of rows, columns, and column names.

Expected Output
----------------
Number of Rows    : 5
Number of Columns : 7

Columns:
Employee_ID
Distance_KM
Travel_Time_Min
Previous_Late_Count
Weather
Transport
Late


TASK 3 — Identify Features and Target
Identify which columns are input features and which column is the target.
Expected Output
----------------
Features:
Distance_KM
Travel_Time_Min
Previous_Late_Count
Weather
Transport

Target:
Late

Employee_ID should not be treated as a meaningful predictive feature.


TASK 4 — Count Late and Non-Late Employees

Calculate the number of employees who arrived late and who did not arrive late.

Expected Output
----------------
Late
No     3
Yes    2

or:

Late Employees     : 2
Not Late Employees : 3



TASK 5 — Calculate Average Travel Time
--------------------------------------
Calculate the average travel time separately for employees who were late and employees who were not late.

Expected Output
----------------
Average Travel Time

Late Employees:
70.0 minutes

Not Late Employees:
30.0 minutes


TASK 6 — Apply a Rule-Based Prediction
-------
The company currently uses the following rule:
IF Distance_KM > 15 AND Travel_Time_Min > 60
THEN Prediction = Yes
ELSE Prediction = No

Apply this rule to every employee.

Expected Output
---------------
Employee_ID    Actual    Prediction
E101           No        No
E102           Yes       Yes
E103           No        No
E104           Yes       Yes
E105           No        No


TASK 7 — Calculate Rule Accuracy
-------
Compare the rule-based prediction with the actual result and calculate the accuracy.

Expected Output
----------------
Correct Predictions : 5
Total Predictions   : 5

Rule-Based Accuracy : 100%


TASK 8 — Predict for a New Employee
------------------------------------
A new employee provides the following information:
Distance_KM = 20
Travel_Time_Min = 70
Previous_Late_Count = 3
Weather = Rain
Transport = Bus

Apply the company's existing rule.


TASK 9 — Test Another New Employee
-----------------------------------
A second employee provides:
Distance_KM = 12
Travel_Time_Min = 55
Previous_Late_Count = 6
Weather = Rain
Transport = Bus

Apply the same rule.

Expected Output
---------------
Employee Distance : 12 KM
Travel Time       : 55 Minutes

Prediction: No

Employee is predicted as not late by the current rule.

Question: Does this necessarily mean the employee will actually be on time?
---------

Expected Answer:
---------------


TASK 10 — Rule-Based System vs Machine Learning
----------------
Print or display the following comparison.

Expected Output
-----------------
RULE-BASED SYSTEM
-----------------
Programmer manually defines conditions.
Example:
Distance > 15 AND Travel Time > 60 → Late

MACHINE LEARNING SYSTEM
-----------------------
Model learns patterns from historical data.
The programmer provides data and the expected outcome,
and the model learns relationships from the data.


Final Question

The company now has 50 additional attributes such as:
Day_of_Week
Traffic_Level
Weather
Transport
Previous_Late_Count
Sleep_Hours
Distance_KM
Travel_Time_Min

Question: Why may a Machine Learning approach become more useful than writing hundreds of rules manually?
----------

Expected Output:
----------------



FINAL EXPECTED OUTPUT
----------------------
At the end of the notebook, you should display:

========== EMPLOYEE ATTENDANCE ANALYSIS ==========

Total Employees        : 5

Late Employees         : 2
Not Late Employees     : 3

Average Travel Time
Late                   : 70.0 minutes
Not Late               : 30.0 minutes

Rule-Based Accuracy    : 100%

New Employee 1
Prediction             : Late

New Employee 2
Prediction             : Not Late

Conclusion:
A rule-based system depends on manually defined conditions.
A Machine Learning system can learn patterns from historical data
and use multiple features to make predictions.