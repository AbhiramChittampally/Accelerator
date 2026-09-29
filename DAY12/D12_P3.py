## Problem 3: Memory-Bounded Categorical Optimization 
"""
Problem Statement:
An enterprise customer support desk logs hundreds of thousands of tickets every single day. 
The Status and Priority labels represent structural repeating patterns with 
high unique-string memory overhead. A script is needed to automatically optimize 
string objects to lighter memory footprints.

The application must execute the following operations:
Parse the support tickets log dataset.
Calculate and display the memory footprint of the string text columns (Status and Priority) combined.
Convert these columns from the default object data type to the optimized Pandas category type.
Calculate and display the new optimized memory footprint.
Provide a summary breakdown showing the category codes map.

Requirements:
Use astype('category').
Compare column .memory_usage(deep=True).

Input File:
--------------------
tickets.csv

Output Format:
--------------------
Unoptimized String Memory: ... Bytes
Optimized Category Memory: ... Bytes
Status Codes Mapping
...

Sample tickets.csv:
--------------------
TicketID,Status,Priority
T1,Open,High
T2,Closed,Low
T3,Open,Medium
T4,Open,High
T5,Closed,Low
Test Case:


case=1
output=
Unoptimized String Memory: 614 Bytes
Optimized Category Memory: 534 Bytes
Status Codes Mapping
Closed : 0
Open : 1



"""
import pandas as pd
df=pd.read_csv("tickets.csv")
before=df[["Status", "Priority"]].memory_usage(index=False, deep=True).sum()
df["Status"] = df["Status"].astype("category")
df["Priority"] = df["Priority"].astype("category")
after = df[["Status", "Priority"]].memory_usage(index=False, deep=True).sum()
print(f"Unoptimized String Memory: {before} Bytes")
print(f"Optimized Category Memory: {after} Bytes")
print("Status Codes Mapping")
for i,value in enumerate(df["Status"].cat.categories):
    print(f"{value} : {i}")