# Read Data

# ↓

# Check Missing Values

# ↓

# Convert Wrong Data Types

# ↓

# Handle Missing Values

# ↓

# Remove Duplicates

# ↓

# Verify Clean Data

# ↓

# Analyze Data

import pandas as pd
import numpy as np

# Read Data
df = pd.read_csv("data.csv")

# View Data
print(df.head())

# Data Types
print(df.dtypes)

# Missing Values
print(df.isna().sum())

# Missing Percentage
print(df.isna().mean()*100)

# Convert Text to Numeric
df["Column"] = pd.to_numeric(
    df["Column"],
    errors="coerce"
)

# Fill Missing Values
df["Column"] = df["Column"].fillna(
    df["Column"].mean()
)

# Fill Text Columns
df["City"] = df["City"].fillna(
    "Unknown"
)

# Remove Duplicates
df = df.drop_duplicates()

# Final Check
print(df.isna().sum())

# Clean Dataset
print(df)


# trick
# Dirty Data

# ↓

# isna()

# ↓

# Count Missing

# ↓

# to_numeric()

# ↓

# fillna()

# ↓

# interpolate()

# ↓

# drop_duplicates()

# ↓

# Clean Data

