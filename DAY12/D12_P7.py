## Problem 7: High-Frequency Store Analytics Benchmarking 
"""
Problem Statement:
A corporate operations team needs to choose between standard Pandas data models or a 
migrate-to-Polars optimization blueprint. To help them decide, you must construct a benchmarking logic 
layout wrapper that runs structural data grouping and aggregation transformations under both architectures. 

The program must execute the following operations:
1.Read a transactions CSV file.
2.Group records by StoreCode and aggregate the mathematical mean value of Sales using Pandas.
3.Group records by StoreCode and aggregate the mathematical mean value of Sales using 
  Polars Lazy API (.lazy()), resolving it immediately via .collect(). 
4.Output the aggregated result format blocks to verify that they match.

Requirements:
1.Process parallel pipelines across pd and pl.
2.Guarantee structural execution parity.

Input File:sales.csv
Output Format:
Pandas Aggregated Performance Metrics
...
Polars Aggregated Performance Metrics
...
Sample sales.csv:
-----------------
StoreID,StoreCode,Sales
STR1,HYD,50000
STR2,BOM,85000
STR3,HYD,60000
STR4,BOM,40000

Test Case:
case=1
output=
Pandas Aggregated Performance Metrics
BOM 62500.0
HYD 55000.0

Polars Aggregated Performance Metrics
BOM 62500.0
HYD 55000.0

"""
import pandas as pd
import polars as pl
pandf=pd.read_csv("sales.csv")
pdresult=pandf.groupby("StoreCode")["Sales"].mean().astype(float)
print("Pandas Aggregated Performance Metrics")
print(pdresult.rename_axis(None).to_string())

poldf=pl.read_csv("sales.csv")
plresult=(
    poldf.lazy()
    .group_by("StoreCode")
    .agg(pl.col("Sales").mean())
    .sort("Sales",descending=True)
    .collect()
)
print("\nPolars Aggregated Performance Metrics")
for row in plresult.iter_rows():
    print(*row)