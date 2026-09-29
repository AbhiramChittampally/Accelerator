## Problem 10: Municipal Smart Grid Network Telemetry System
"""
Problem Statement:A municipal green-energy smart grid logs hourly distribution utilization metrics across
regional substations using distinct logger profiles. During integration sweeps, specific intervals
exhibit transmission gaps, collection dropouts, and redundant sensor snapshots.
 
To process this critical stream effectively without running into system OOM crashes, engineers require
an automated evaluation program to restructure execution profiles, impute dropped metrics, apply scaling 
multipliers, downcast data containers, and optimize queries using lazy data frame parsing.

The program should perform the following operations:
1.Load three data assets containing grid configurations.
2.Intersect all tables securely by performing an inner structural merge over StationID.
3.Display the raw imported smart grid telemetry matrix.
4.Locate tracking omissions via isnull().
5.Interpolate incomplete LoadFactor sequences over missing arrays safely using interpolate().
6.Fill remaining vacant numeric attributes using the computed system average through fillna().
7.Eliminate redundant recording duplicates via drop_duplicates().
8.Parse raw log sequences into recognized runtime objects with pd.to_datetime().
9.Assign the timeline elements into a structured DatetimeIndex.
10.Group and evaluate monthly average utilization trends using resample().
11.Compute aggregate structural loads across different facilities via groupby().
12.Transpose the operational grid variables into an executive layout using pivot_table().
13.Rearrange the data columns into flat rows using melt().
14.Restore the structured layout mapping back to verify operational properties via pivot().
15.Filter out specific active allocations for 'Zone-A' grids using .loc[] constraints.
16.Extract the terminal two network tracking lines with positional .iloc[] boundaries.
17.Apply NumPy structural arrays vectorization formulas to evaluate load adjustments ($PeakLoad \times 8\%$).
18.Compute an aggregate total load representation using NumPy data broadcasting ($PeakLoad + SecondaryLoad$).
19.Downcast metrics features to lower bit allocations via pd.to_numeric() to enforce memory boundaries.
20.Construct an efficient Polars Lazy execution graph using .lazy(), filter for critical threshold overshoots, and call .collect().

Requirements:
1.Read three CSV files.
2.Perform multi-stage frame joins.Call isnull(), fillna(), interpolate(), and drop_duplicates().
3.Manage pd.to_datetime(), DatetimeIndex, and resample().
4.Formulate data matrices using groupby(), pivot_table(), melt(), and pivot().
5.Apply conditional filters with .loc[] and .iloc[].
6.Run high-efficiency operations using NumPy array vectorization and broadcasting properties.
7.Execute structural variable compression using pd.to_numeric(..., downcast=...).
8.Extract target parameters under Polars lazy processing structures with .lazy().collect().

Input Files:
-------------
stations.csv
--------------
StationID,StationName,Zone
ST10,Sub_Alpha,Zone-A
ST20,Sub_Beta,Zone-B
ST30,Sub_Gamma,Zone-A
ST40,Sub_Delta,Zone-C
ST40,Sub_Delta,Zone-C

loads.csv
-----------
StationID,PeakLoad,SecondaryLoad
ST10,4800,320
ST20,5200,410
ST30,3100,280
ST40,6400,550

telemetry.csv
--------------
StationID,Timestamp,LoadFactor,VoltageDrop
ST10,2026-04-01,0.85,1.2
ST20,2026-04-15,,1.5
ST30,2026-05-02,0.72,
ST40,2026-05-20,0.91,2.1

Test Case:
---------
case=1
output=
Raw Imported Smart Grid Telemetry Matrix
ST10 Sub_Alpha Zone-A 4800 0.85 1.2
ST20 Sub_Beta Zone-B 5200 nan 1.5
ST30 Sub_Gamma Zone-A 3100 0.72 nan
ST40 Sub_Delta Zone-C 6400 0.91 2.1
ST40 Sub_Delta Zone-C 6400 0.91 2.1

Tracking Omissions Analysis Layout
False False False False False False
False False False False True False
False False False False False True
False False False False False False
False False False False False False

Fully Cleansed Temporal Grid Datetime Index
ST10 Sub_Alpha Zone-A 0.85 1.2
ST20 Sub_Beta Zone-B 0.785 1.5
ST30 Sub_Gamma Zone-A 0.72 1.8
ST40 Sub_Delta Zone-C 0.91 2.1

Monthly Average Telemetry Metrics
2026-04 0.8175
2026-05 0.815

Aggregate Load Across Facilities
Zone-A 7900.0
Zone-B 5200.0
Zone-C 6400.0

Executive Transposed Pivot Layout
Timestamp  2026-04  2026-05
Zone                       
Zone-A      4800.0   3100.0
Zone-B      5200.0       0.0
Zone-C         0.0   6400.0

Rearranged Melt Long Format
ST10 Sub_Alpha PeakLoad 4800.0
ST20 Sub_Beta PeakLoad 5200.0
ST30 Sub_Gamma PeakLoad 3100.0
ST40 Sub_Delta PeakLoad 6400.0
ST10 Sub_Alpha SecondaryLoad 320.0
ST20 Sub_Beta SecondaryLoad 410.0
ST30 Sub_Gamma SecondaryLoad 280.0
ST40 Sub_Delta SecondaryLoad 550.0

Reconstructed Verification Matrix
  StationID    StationName  PeakLoad  SecondaryLoad
0      ST10      Sub_Alpha    4800.0          320.0
1      ST20       Sub_Beta    5200.0          410.0
2      ST30      Sub_Gamma    3100.0          280.0
3      ST40      Sub_Delta    6400.0          550.0

Zone-A Facility Target Subsets
ST10 Sub_Alpha 4800.0
ST30 Sub_Gamma 3100.0

Terminal Positional Data Records
ST30 Sub_Gamma Zone-A
ST40 Sub_Delta Zone-C

NumPy Vectorized Load Variance Adjustments
384.0
416.0
248.0
512.0

NumPy Broadcasting Compound Grid Inferences
5504.0
5966.0
3558.0
7342.0

Downcasted Matrix Columns Configuration
PeakLoad         int16
SecondaryLoad    int16
dtype: object

Polars Query Graph Critical Anomalies Evaluation
ST40 Zone-C 6400
"""
import pandas as pd
import numpy as np
import polars as pl


stations = pd.read_csv("stations.csv")
loads = pd.read_csv("loads.csv")
telemetry = pd.read_csv("telemetry.csv")


df = pd.merge(stations, loads, on="StationID", how="inner")
df = pd.merge(df, telemetry, on="StationID", how="inner")
print("Raw Imported Smart Grid Telemetry Matrix")
print(df.to_string(index=False,header=False))
print("\nTracking Omissions Analysis Layout")
print(df.isna().to_string(header=False,index=False))
df["LoadFactor"] = df["LoadFactor"].interpolate()

df["VoltageDrop"] = df["VoltageDrop"].interpolate()

df = df.fillna(df.mean(numeric_only=True))
df=df.drop_duplicates()
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.set_index("Timestamp")

print("\nFully Cleansed Temporal Grid Datetime Index")

for _, row in df.iterrows():
    print(
        row["StationID"],
        row["StationName"],
        row["Zone"],
        round(row["LoadFactor"],2),
        row["VoltageDrop"]
    )
    
    
    
monthly = df["LoadFactor"].resample("M").mean()
print("\nMonthly Average Telemetry Metrics")
for index,value in monthly.items():
    print(index.strftime("%Y-%m"),round(value,4))
    
print("\nAggregate Load Across Facilities")

grouped = df.groupby("Zone")["PeakLoad"].sum()

for zone, value in grouped.items():
    print(zone, float(value))

print("\nExecutive Transposed Pivot Layout")

temp = df.copy()
temp["Month"] = temp.index.strftime("%Y-%m")

pivot_table = temp.pivot_table(
    index="Zone",
    columns="Month",
    values="PeakLoad",
    aggfunc="sum",
    fill_value=0
)

print(pivot_table.astype(float))

print("\nRearranged Melt Long Format")

melted = pd.melt(
    temp.reset_index(drop=True),
    id_vars=["StationID","StationName"],
    value_vars=["PeakLoad","SecondaryLoad"],
    var_name="LoadType",
    value_name="LoadValue"
)

for _, row in melted.iterrows():
    print(
        row["StationID"],
        row["StationName"],
        row["LoadType"],
        float(row["LoadValue"])
    )
    
    
    
print("\nReconstructed Verification Matrix")
melted = melted.reset_index(drop=True)

reconstructed = melted.pivot(
    index="StationID",
    columns="LoadType",
    values="LoadValue"
).reset_index()

reconstructed = reconstructed.merge(
    stations[["StationID", "StationName"]].drop_duplicates(),
    on="StationID"
)

reconstructed = reconstructed[
    ["StationID", "StationName", "PeakLoad", "SecondaryLoad"]
]

print(reconstructed.to_string())

print("\nZone-A Facility Target Subsets")

zone_a = df.loc[
    df["Zone"] == "Zone-A",
    ["StationID","StationName","PeakLoad"]
]

for _, row in zone_a.iterrows():
    print(
        row["StationID"],
        row["StationName"],
        float(row["PeakLoad"])
    )
print("\nTerminal Positional Data Records")

last_two = df.iloc[-2:]

for _, row in last_two.iterrows():
    print(
        row["StationID"],
        row["StationName"],
        row["Zone"]
    )    
    
    
    
print("\nNumPy Vectorized Load Variance Adjustments")

peak = df["PeakLoad"].to_numpy()

adjustments = peak * 0.08

for value in adjustments:
    print(value)


print("\nNumPy Broadcasting Compound Grid Inferences")

secondary = df["SecondaryLoad"].to_numpy()

compound = peak + secondary + adjustments

for value in compound:
    print(value)  


df["PeakLoad"] = pd.to_numeric(df["PeakLoad"], downcast="integer")
df["SecondaryLoad"] = pd.to_numeric(df["SecondaryLoad"], downcast="integer")

print("\nDowncasted Matrix Columns Configuration")
print(df[["PeakLoad","SecondaryLoad"]].dtypes)


print("\nPolars Query Graph Critical Anomalies Evaluation")

pl_df = pl.from_pandas(df.reset_index())

critical = (
    pl_df
    .lazy()
    .filter(pl.col("PeakLoad") > 6000)
    .select(["StationID","Zone","PeakLoad"])
    .collect()
)

for row in critical.iter_rows():
    print(*row)    