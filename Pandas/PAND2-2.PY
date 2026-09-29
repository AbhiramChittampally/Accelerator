#1
# import pandas as pd

# df = pd.DataFrame({
#     "Column1":[],
#     "Column2":[],
#     "Column3":[]
# })

# print(df)



#2
import pandas as pd

df = pd.DataFrame({
    "Name": ["Ram", "Rahul", "Priya"],
    "Age": [21, 22, 20],
    "Marks": [90, 75, 99]
})

# One column
print(df["Marks"])

# Multiple columns
print(df[["Name", "Marks"]])

# Row by label
print(df.loc[1])

# Row by position
print(df.iloc[1])

# Specific value by label
print(df.loc[2, "Marks"])

# Specific value by position
print(df.iloc[2, 2])




#3
import pandas as pd

df = pd.DataFrame({
    "Name":["Ram","Rahul","Priya","Anu"],
    "Age":[21,22,20,19],
    "Marks":[90,75,99,81]
})

# One condition
print(df[df["Marks"] > 80])

# AND
print(df[(df["Marks"] > 80) & (df["Age"] > 20)])

# OR
print(df[(df["Marks"] > 90) | (df["Age"] < 20)])

# NOT
print(df[~(df["Marks"] > 80)])

# Between
print(df[df["Marks"].between(70,90)])

# isin
print(df[df["Name"].isin(["Ram","Anu"])])

# String contains
print(df[df["Name"].str.contains("a", case=False)])



#4
import pandas as pd

df = pd.DataFrame({
    "Department":["HR","IT","HR","IT"],
    "Salary":[40000,60000,50000,70000]
})

print(df.groupby("Department")["Salary"].mean())

print(df.groupby("Department")["Salary"].sum())

print(df.groupby("Department")["Salary"].count())

print(df.groupby("Department")["Salary"].max())

print(df.groupby("Department")["Salary"].min())

print(df.groupby("Department")["Salary"].agg(
    ["mean","sum","count","max","min"]
))



#5
import pandas as pd

# -------------------------------
# DataFrame 1
# -------------------------------
employees = pd.DataFrame({
    "ID": [101, 102, 103],
    "Name": ["Ram", "Rahul", "Priya"],
    "Department": ["HR", "IT", "HR"]
})

# -------------------------------
# DataFrame 2
# -------------------------------
salary = pd.DataFrame({
    "ID": [102, 103, 104],
    "Salary": [50000, 60000, 55000]
})

print("Employees")
print(employees)

print("\nSalary")
print(salary)

# ===================================
# 1. INNER MERGE
# ===================================

print("\nINNER MERGE")
inner = pd.merge(employees, salary,
                 on="ID",
                 how="inner")
print(inner)

# ===================================
# 2. LEFT MERGE
# ===================================

print("\nLEFT MERGE")
left = pd.merge(employees, salary,
                on="ID",
                how="left")
print(left)

# ===================================
# 3. RIGHT MERGE
# ===================================

print("\nRIGHT MERGE")
right = pd.merge(employees, salary,
                 on="ID",
                 how="right")
print(right)

# ===================================
# 4. OUTER MERGE
# ===================================

print("\nOUTER MERGE")
outer = pd.merge(employees, salary,
                 on="ID",
                 how="outer")
print(outer)

# ===================================
# 5. MERGE USING DIFFERENT COLUMN NAMES
# ===================================

employee2 = pd.DataFrame({
    "EmpID": [101,102,103],
    "Name": ["Ram","Rahul","Priya"]
})

salary2 = pd.DataFrame({
    "EmployeeID":[101,102,103],
    "Salary":[50000,60000,55000]
})

print("\nMERGE USING DIFFERENT COLUMN NAMES")

result = pd.merge(employee2,
                  salary2,
                  left_on="EmpID",
                  right_on="EmployeeID")

print(result)

# ===================================
# 6. MERGE USING MULTIPLE COLUMNS
# ===================================

df1 = pd.DataFrame({
    "ID":[101,102,103],
    "Department":["HR","IT","HR"],
    "Name":["Ram","Rahul","Priya"]
})

df2 = pd.DataFrame({
    "ID":[101,102,103],
    "Department":["HR","IT","HR"],
    "Salary":[50000,60000,55000]
})

print("\nMERGE USING MULTIPLE COLUMNS")

multi = pd.merge(df1,
                 df2,
                 on=["ID","Department"])

print(multi)

# ===================================
# 7. SELECT SPECIFIC COLUMNS AFTER MERGE
# ===================================

print("\nSELECT SPECIFIC COLUMNS")

print(inner[["Name","Salary"]])



























































