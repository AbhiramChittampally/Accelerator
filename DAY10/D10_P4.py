"""
A smart city continuously monitors environmental conditions using IoT sensors installed across the city.

Due to temporary network failures, some sensor readings are missing.

The city administration wants to recover the missing sensor values before generating analytical reports.

Each sensor record contains:

Sensor ID
Location
Date
Temperature

The program should perform the following operations.

Step 1:Load the sensor dataset using Pandas.
Step 2:Display the complete sensor dataset.
Step 3:Display the missing values using isnull().
Step 4:Convert the Date column into Datetime format using pd.to_datetime().
Step 5:Recover the missing temperature values using interpolate().
Step 6:Display the recovered sensor dataset.
Step 7:Display the average temperature after interpolation.

Requirements
Read sensors.csv.
Create a Pandas DataFrame.
Use isnull().
Use pd.to_datetime().
Use interpolate().
Display the average temperature.


Input File:sensors.csv
-----------

SensorID,Location,Date,Temperature
S101,Hyderabad,2025-01-01,30
S102,Hyderabad,2025-01-02,
S103,Hyderabad,2025-01-03,34
S104,Hyderabad,2025-01-04,
S105,Hyderabad,2025-01-05,38


case=1
output=
Sensor Dataset
S101 Hyderabad 2025-01-01 30.0
S102 Hyderabad 2025-01-02 nan
S103 Hyderabad 2025-01-03 34.0
S104 Hyderabad 2025-01-04 nan
S105 Hyderabad 2025-01-05 38.0

Missing Values
False False False False
False False False True
False False False False
False False False True
False False False False

Recovered Sensor Dataset
S101 Hyderabad 2025-01-01 30.0
S102 Hyderabad 2025-01-02 32.0
S103 Hyderabad 2025-01-03 34.0
S104 Hyderabad 2025-01-04 36.0
S105 Hyderabad 2025-01-05 38.0

Average Temperature

34.0
"""
import pandas as pd
print("Sensor Dataset")
df=pd.read_csv("sensors.csv")
print(df.to_string(index=False,header=False))

print("\nMissing Values")
print(df.isnull().to_string(index=False,header=False))
df["Date"]=pd.to_datetime(df["Date"])
print("\nRecovered Sensor Dataset")
print(df.interpolate(method="linear").to_string(index=False,header=False))
print("\nAverage Temperature\n")
print(df["Temperature"].mean())