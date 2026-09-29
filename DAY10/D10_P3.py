"""
Problem Title:Smart Employee Missing Salary Analyzer using Pandas

Problem Statement:
------------------
A software company maintains employee details in a CSV file.

During data collection, some employee salary values
were accidentally left empty.

The HR department wants to clean the dataset before
performing salary analysis.

Each employee record contains:
------------------------------
Employee ID
Employee Name
Department
Salary

The program should perform the following operations.

Step 1:Load the employee dataset using Pandas.
Step 2:Display the complete employee dataset.
Step 3:Display the missing values using isnull().
Step 4:Replace the missing salary values with the average salary of all available employees using fillna().
Step 5:Display the updated dataset.

Requirements
------------
1. Read employees.csv.
2. Create a Pandas DataFrame.
3. Use isnull().
4. Use fillna().
5. Display the updated dataset.

Input File
----------
employees.csv

Output Format
-------------
Employee Dataset
...
Missing Values
...
Updated Employee Dataset
...

Sample employees.csv
--------------------
EmployeeID,EmployeeName,Department,Salary
E101,Ravi,Development,60000
E102,Priya,Testing,
E103,Rahul,Development,70000
E104,Anu,HR,50000
E105,Kiran,Testing,

case=1
output=
Employee Dataset

E101 Ravi Development 60000.0
E102 Priya Testing nan
E103 Rahul Development 70000.0
E104 Anu HR 50000.0
E105 Kiran Testing nan

Missing Values

False False False False
False False False True
False False False False
False False False False
False False False True

Updated Employee Dataset

E101 Ravi Development 60000.0
E102 Priya Testing 60000.0
E103 Rahul Development 70000.0
E104 Anu HR 50000.0
E105 Kiran Testing 60000.00
"""

import pandas as pd
df=pd.read_csv("employees.csv")
print("Employee Dataset\n")
print(df.to_string(index=False,header=False))
print("\nMissing Values\n")
print(df.isnull().to_string(index=False,header=False))
print("\nUpdated Employee Dataset\n")
df["Salary"]=df["Salary"].fillna(df["Salary"].mean())
print(df.to_string(index=False,header=False))