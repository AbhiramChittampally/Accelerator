
#null and nan and none
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Ram", "John", None],
    "Marks": [90, np.nan, 80]
})

print("Original Data")
print(df)

print("\nMissing Values")
print(df.isna())

print("\nNon Missing Values")
print(df.notna())

print("\nUsing isnull()")
print(df.isnull())

print("\nUsing notnull()")
print(df.notnull())




#analzying missing values
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name":["Ram","John","Alice",None],
    "Age":[20,np.nan,22,21],
    "Marks":[90,np.nan,80,np.nan]
})

# Missing values
print(df.isna())

# Missing count
print(df.isna().sum())

# Missing percentage
print(df.isna().mean()*100)

# Rows with missing values
print(df[df.isna().any(axis=1)])

# Rows without missing values
print(df[df.notna().all(axis=1)])

# Columns having missing values
print(df.isna().any())

# Columns completely missing
print(df.isna().all())






#dropna methods
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name":["Ram","Rahul","Priya","John"],
    "Maths":[90,np.nan,80,70],
    "Science":[95,85,np.nan,88]
})

# Default
print(df.dropna())

# Remove columns
print(df.dropna(axis=1))

# Remove if any missing
print(df.dropna(how="any"))

# Remove if all missing
print(df.dropna(how="all"))

# Check only Name
print(df.dropna(subset=["Name"]))

# Check only Maths
print(df.dropna(subset=["Maths"]))

# Keep rows with at least 2 values
print(df.dropna(thresh=2))

# Modify original
df.dropna(inplace=True)
print(df)





#fillna methods
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name":["Ram","Rahul","Priya","John"],
    "Marks":[90,np.nan,80,np.nan],
    "Age":[20,np.nan,22,21]
})

# Fill with constant
print(df.fillna(0))

# Fill one column with mean
df["Marks"] = df["Marks"].fillna(df["Marks"].mean())

# Fill one column with median
df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill with mode
df["Name"] = df["Name"].fillna(df["Name"].mode()[0])

# Fill different columns differently
df = df.fillna({
    "Age":0,
    "Marks":50,
    "Name":"Unknown"
})

# Forward fill
print(df.ffill())

# Backward fill
print(df.bfill())

print(df)





#interpolate methods
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Value":[10,np.nan,np.nan,40,50]
})

# Default linear interpolation
print(df.interpolate())

# Explicit linear interpolation
print(df.interpolate(method="linear"))

# Fill only one missing value
print(df.interpolate(limit=1))

# Modify original DataFrame
df.interpolate(inplace=True)

print(df)






#duplicate methods
import pandas as pd

df = pd.DataFrame({
    "Name":["Ram","Rahul","Priya","Rahul","John"],
    "Marks":[90,85,80,85,70]
})

print("Original")
print(df)

# Identify duplicates
print(df.duplicated())

# Show duplicate rows
print(df[df.duplicated()])

# Remove duplicates
print(df.drop_duplicates())

# Keep last duplicate
print(df.drop_duplicates(keep="last"))

# Remove all duplicates
print(df.drop_duplicates(keep=False))

# Check duplicates using one column
print(df.duplicated(subset=["Name"]))

# Remove duplicates using one column
print(df.drop_duplicates(subset=["Name"]))

# Modify original
df.drop_duplicates(inplace=True)

print(df)



#to numeric, coerce and raise
import pandas as pd

df = pd.DataFrame({
    "Marks":["90","80","Absent","100","N/A"]
})

print("Original")
print(df)

# Convert to numeric
df["Marks"] = pd.to_numeric(
    df["Marks"],
    errors="coerce"
)

print("\nConverted")
print(df)

# Fill missing values
df["Marks"] = df["Marks"].fillna(
    df["Marks"].mean()
)

print("\nAfter Cleaning")
print(df)