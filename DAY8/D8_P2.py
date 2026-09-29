"""
Problem Title: Smart Employee Project Allocation Analyzer using Pandas

Problem Statement:

A software company maintains two CSV files.

The first CSV file stores employee details.

The second CSV file stores project details assigned
to employees.

The HR department wants to generate a project allocation
report using Pandas.

Employee File contains:

Employee ID
Employee Name
Department

Project File contains:

Employee ID
Project Name
Project Duration (Months)

The program should perform the following operations.

Step 1:Load both CSV files using Pandas.

Step 2:Merge both datasets using Employee ID.

Step 3:Display the complete merged dataset.

Step 4: Using loc[], display all employees working in the Development department.

Step 5: Using groupby(), display the average project duration of each department.

Requirements
------------

1. Read employee.csv.
2. Read project.csv.
3. Merge both DataFrames.
4. Use merge().
5. Use loc().
6. Use groupby().

Input Files
-----------

employees.csv

projects.csv

Output Format
-------------

Merged Employee Project Dataset

...

Development Employees

...

Average Project Duration Department Wise

...

Sample employees.csv
--------------------

EmployeeID,EmployeeName,Department
E101,Ravi,Development
E102,Priya,Testing
E103,Rahul,Development
E104,Anu,HR

Sample projects.csv
-------------------

EmployeeID,ProjectName,Duration
E101,E-Commerce,8
E102,Hospital,6
E103,Banking,10
E104,Payroll,4

Sample Output:
---------------
Merged Employee Project Dataset

EmployeeID EmployeeName Department ProjectName Duration
E101 Ravi Development E-Commerce 8
E102 Priya Testing Hospital 6
E103 Rahul Development Banking 10
E104 Anu HR Payroll 4

Development Employees

E101 Ravi Development E-Commerce 8
E103 Rahul Development Banking 10

Average Project Duration Department Wise

Development 9.0
HR 4.0
Testing 6.0



case=1
output=
Merged Employee Project Dataset
E101 Ravi Development E-Commerce 8
E102 Priya Testing Hospital 6
E103 Rahul Development Banking 10
E104 Anu HR Payroll 4

Development Employees
E101 Ravi Development E-Commerce 8
E103 Rahul Development Banking 10

Average Project Duration Department Wise
Development 9.0
HR 4.0
Testing 6.0
"""
import pandas as pd
df1=pd.read_csv("employees.csv")
df2=pd.read_csv("projects.csv")

inner=pd.merge(df1,df2,
                on="EmployeeID",
                how="inner")
print("Merged Employee Project Dataset\n") 
print(inner.to_string(index=False,header=False))
print("\nDevelopment Employees\n")
print(inner.loc[inner["Department"]=="Development"].to_string(index=False,header=False))
print("\nAverage Project Duration Department Wise\n")
print(inner.groupby("Department")["Duration"].mean().rename_axis(None).to_string(header=False))