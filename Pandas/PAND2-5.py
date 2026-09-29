import pandas as pd

df = pd.DataFrame({
    "Name":["Ram","Rahul","Priya"],
    "Age":[20,21,22],
    "City":["Delhi","Mumbai","Hyderabad"]
})

# Memory used by each column
print(df.memory_usage())

# Memory including strings
print(df.memory_usage(deep=True))

# Total memory
print(df.memory_usage(deep=True).sum())

# Memory in KB
print(df.memory_usage(deep=True).sum()/1024)

# Memory in MB
print(df.memory_usage(deep=True).sum()/1024/1024)

# DataFrame summary
df.info()

# Deep memory summary
df.info(memory_usage="deep")


#Memory flow diagram
# CSV File
#       │
#       ▼
#    DataFrame
#       │
#       ▼
# memory_usage()
#       │
#       ▼
# Memory Used Per Column
#       │
#       ▼
# memory_usage(deep=True)
#       │
#       ▼
# True Memory Including Strings






#downcasting
# CSV File
#       │
#       ▼
#    DataFrame
#       │
#       ▼
# memory_usage()
#       │
#       ▼
# Memory Used Per Column
#       │
#       ▼
# memory_usage(deep=True)
#       │
#       ▼
# True Memory Including Strings

import pandas as pd

def reduce_memory(df):
    for col in df.columns:

        if df[col].dtype == "int64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="integer"
            )

        elif df[col].dtype == "float64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="float"
            )

    return df




#category dtype
import pandas as pd

def reduce_memory(df):
    for col in df.columns:

        if df[col].dtype == "int64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="integer"
            )

        elif df[col].dtype == "float64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="float"
            )

    return df


#prof example
import pandas as pd

df = pd.read_csv("employees.csv")

for col in df.columns:

    if df[col].dtype == "object":

        unique_ratio = df[col].nunique() / len(df)

        if unique_ratio < 0.5:

            df[col] = df[col].astype("category")
#Memory Trick
# Repeated Text

# ↓

# Store Once

# ↓

# Replace with Numbers

# ↓

# Less RAM

# ↓

# Faster GroupBy

# ↓

# Faster Sorting

# ↓

# Faster Filtering            




#chunksss
import pandas as pd

chunks = pd.read_csv(
    "students.csv",
    chunksize=1000
)

for chunk in chunks:

    print(chunk)
    
#prof boilerplate
import pandas as pd

total = 0

count = 0

chunks = pd.read_csv(
    "employees.csv",
    chunksize=10000
)

for chunk in chunks:

    total += chunk["Salary"].sum()

    count += len(chunk)

average = total / count

print(average)

#pattern
# chunks = pd.read_csv(
#     "file.csv",
#     chunksize=100000
# )

# for chunk in chunks:

#     # Filter

#     # Clean

#     # Aggregate

#     # Save

#     # Delete automatically
    
    
    
    
#readcsv methods
import pandas as pd

df = pd.read_csv(
    "students.csv",
    usecols=["Name","Marks"],
    dtype={
        "Marks":"float32"
    }
)

print(df.head())

# prof boilerplate
import pandas as pd

chunks = pd.read_csv(
    "employees.csv",
    usecols=[
        "Department",
        "Salary",
        "JoiningDate"
    ],
    dtype={
        "Department":"category",
        "Salary":"float32"
    },
    parse_dates=["JoiningDate"],
    chunksize=10000
)

for chunk in chunks:

    print(chunk.head())


#readcsv master boilerplate
import pandas as pd

df = pd.read_csv(
    "data.csv",

    # Read only required columns
    usecols=["Col1","Col2"],

    # Set data types
    dtype={
        "Col1":"int32",
        "Col2":"float32"
    },

    # Parse dates
    parse_dates=["Date"],

    # Use existing index
    index_col=None,

    # Read only first rows
    nrows=None,

    # Skip unwanted rows
    skiprows=0
)

print(df.head())



#vectorization vs loops vs apply vs broadcasting
#beginner bp
import pandas as pd

df = pd.read_csv(
    "data.csv",

    # Read only required columns
    usecols=["Col1","Col2"],

    # Set data types
    dtype={
        "Col1":"int32",
        "Col2":"float32"
    },

    # Parse dates
    parse_dates=["Date"],

    # Use existing index
    index_col=None,

    # Read only first rows
    nrows=None,

    # Skip unwanted rows
    skiprows=0
)

print(df.head())



#apply() bp
import pandas as pd

df = pd.DataFrame({
    "Salary":[10000,20000,30000]
})

def increase(x):
    return x * 1.10

df["Salary"] = df["Salary"].apply(
    increase
)

print(df)



#rowwise apply() bp
import pandas as pd

df = pd.DataFrame({
    "Maths":[80,90],
    "Science":[70,95]
})

df["Total"] = df.apply(
    lambda row: row["Maths"] + row["Science"],
    axis=1
)

print(df)



#map() boilerplate
import pandas as pd

df = pd.DataFrame({
    "Grade":["A","B","A","C"]
})

mapping = {
    "A":"Excellent",
    "B":"Good",
    "C":"Average"
}

df["Result"] = df["Grade"].map(
    mapping
)

print(df)



#prof decisiontree
# Need arithmetic?

# ↓

# Use Vectorization

# --------------------

# Need custom function?

# ↓

# Use apply()

# --------------------

# Need row-wise logic?

# ↓

# apply(axis=1)

# --------------------

# Need value replacement?

# ↓

# map()






#performance profiling and benchmarking
import pandas as pd
import time

start = time.time()

df = pd.read_csv("employees.csv")

end = time.time()

print(end-start)



#measuring vectorization
import pandas as pd
import time

df = pd.DataFrame({
    "Salary":range(1000000)
})

start = time.time()

df["Salary"] *= 1.10

end = time.time()

print(end-start)




#measuring loop
start = time.time()

for i in range(len(df)):
    df.loc[i,"Salary"] *= 1.10

end = time.time()

print(end-start)


# prof workflow
# Write Code

# ↓

# Measure

# ↓

# Find Slow Step

# ↓

# Optimize

# ↓

# Measure Again

# ↓

# Compare




#beginner boilerplate
import time

start=time.time()

for i in range(100000):
    x=i*i

end=time.time()

print("Time:",end-start)



# Comparing Loop vs Vectorization
import pandas as pd
import time

df=pd.DataFrame({
    "Marks":range(100000)
})

# Vectorized
start=time.time()

df["Marks"]+=5

print("Vectorized:",time.time()-start)





# Professional Benchmark Template
import time

start=time.time()

# Your Code Here

end=time.time()

print("Execution Time:",end-start,"seconds")



# Benchmarking Multiple Steps
import time

start=time.time()
# Read CSV
print("Read:",time.time()-start)

start=time.time()
# Cleaning
print("Cleaning:",time.time()-start)

start=time.time()
# GroupBy
print("GroupBy:",time.time()-start)

start=time.time()
# Save CSV
print("Save:",time.time()-start)






#Performance Optimization Checklist ⭐
# Is my CSV huge?

# ↓

# Use chunksize

# ----------------

# Many repeated strings?

# ↓

# Use category

# ----------------

# Wrong datatypes?

# ↓

# Downcast

# ----------------

# Using loops?

# ↓

# Vectorize

# ----------------

# Still slow?

# ↓

# Profile

# ↓

# Measure

# ↓

# Optimize