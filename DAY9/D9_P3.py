"""
Problem Title:
Smart Monthly Sales Pivot Dashboard using Pandas

Problem Statement:

A retail company maintains monthly sales records of
its employees in a CSV file.

The management wants to generate a monthly sales
dashboard using Pandas Pivot Tables.

Each sales record contains:

Employee ID
Employee Name
Department
Month
Sales Amount

The program should perform the following operations.

Step 1:Load the sales dataset using Pandas.
Step 2:Display the complete sales dataset.
Step 3:Create a Pivot Table showing the total sales of each department for every month.
Step 4:Display the department generating the highest total sales.
Step 5:Display the month generating the highest overall sales.

Requirements
------------
1. Read sales.csv.
2. Create a Pandas DataFrame.
3. Use pivot_table().
4. Use aggfunc='sum'.
5. Use fill_value=0.
6. Display highest revenue department.
7. Display highest revenue month.

Input File
----------
sales.csv

Output Format
-------------
Sales Dataset
...
Department-wise Monthly Sales
...
Highest Revenue Department
...
Highest Revenue Month
...

Sample sales.csv
----------------
EmployeeID,EmployeeName,Department,Month,Sales
E101,Ravi,Electronics,January,60000
E102,Priya,Fashion,January,30000
E103,Rahul,Electronics,February,70000
E104,Anu,Fashion,February,40000
E105,Kiran,Grocery,January,25000
E106,Ajay,Grocery,February,35000


case=1
output=
Sales Dataset
E101 Ravi Electronics January 60000
E102 Priya Fashion January 30000
E103 Rahul Electronics February 70000
E104 Anu Fashion February 40000
E105 Kiran Grocery January 25000
E106 Ajay Grocery February 35000

Department-wise Monthly Sales

Month         February  January
Department
Electronics      70000    60000
Fashion          40000    30000
Grocery          35000    25000

Highest Revenue Department

Electronics 130000

Highest Revenue Department

February 145000
"""
import pandas as pd
df=pd.read_csv("sales.csv")
df=df.sort_values("EmployeeID")
print("Sales Dataset")
print(df.to_string(index=False, header=False))

piv=pd.pivot_table(
    df,
    index="Department",
    columns="Month",
    values="Sales",
    aggfunc="sum",
    fill_value=0)
print("\nDepartment-wise Monthly Sales\n")    
print(piv)

dpt=piv.sum(axis=1)
print("\nHighest Revenue Department\n")
print(dpt.idxmax(),dpt.max())
rm=piv.sum(axis=0)
print("\nHighest Revenue Month\n")
print(rm.idxmax(),rm.max())