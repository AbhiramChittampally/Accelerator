## Problem 5: Pandas vs Polars Eager Processing Engine Evaluation
"""
Problem Statement:
A financial data migration specialist needs to contrast Pandas core DataFrame 
operations directly against the modern high-performance alternative Polars. 
The team wants to ensure both engines execute identical basic calculations with exact numeric tracking symmetry.

The application must execute the following operations:
1.Parse an account balance tracking ledger using Pandas, calculate the total summation of all balances,
 and print the output.
2.Parse the exact same file using Polars in eager mode via pl.read_csv(), calculate the 
total summation of all balances, and print the output.

Requirements:
-------------
1.Implement and match Pandas execution and Polars (pl) execution workflows.
2.Return validated, matching aggregated outputs.

Input File:
-------------
balances.csv

Output Format:
-------------
Pandas Execution Engine Total
...
Polars Execution Engine Total
...

Sample balances.csv:
-----------------------
AccountID,Holder,Balance
ACC1,Ram,45000.50
ACC2,Sita,72000.75
ACC3,Ganesh,12500.00

Test Case:
case=1
output=
Pandas Execution Engine Total
129501.25

Polars Execution Engine Total
129501.25
"""
import pandas as pd
import polars as pl
pand=pd.read_csv("balances.csv")
pdtotal=pand["Balance"].sum()
pola=pl.read_csv("balances.csv")
pltotal=pola["Balance"].sum()

print("Pandas Execution Engine Total")
print(pdtotal)
print("\nPolars Execution Engine Total")
print(pltotal)

