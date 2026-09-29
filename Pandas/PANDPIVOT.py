#1
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "Student": ["Rahul","Rahul","Priya","Priya","Rahul","Priya"],
    "Subject": ["Math","Science","Math","Science","Math","Math"],
    "Class": ["A","A","A","A","B","B"],
    "Marks": [90,80,95,88,85,91]
})

print(df)

# ==================================================
# 1. Basic Pivot Table
# ==================================================

pivot1 = pd.pivot_table(
    df,
    values="Marks",
    index="Student"
)

print("\nBasic Pivot")
print(pivot1)

# ==================================================
# 2. Rows + Columns
# ==================================================

pivot2 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject"
)

print("\nRows and Columns")
print(pivot2)

# ==================================================
# 3. Using Sum
# ==================================================

pivot3 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc="sum"
)

print("\nSum")
print(pivot3)

# ==================================================
# 4. Using Count
# ==================================================

pivot4 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc="count"
)

print("\nCount")
print(pivot4)

# ==================================================
# 5. Using Maximum
# ==================================================

pivot5 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc="max"
)

print("\nMaximum")
print(pivot5)

# ==================================================
# 6. Using Minimum
# ==================================================

pivot6 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc="min"
)

print("\nMinimum")
print(pivot6)

# ==================================================
# 7. Multiple Aggregations
# ==================================================

pivot7 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc=["mean","sum","count"]
)

print("\nMultiple Aggregations")
print(pivot7)

# ==================================================
# 8. Multiple Row Indexes
# ==================================================

pivot8 = pd.pivot_table(
    df,
    values="Marks",
    index=["Class","Student"],
    columns="Subject"
)

print("\nMultiple Row Indexes")
print(pivot8)

# ==================================================
# 9. Multiple Columns
# ==================================================

pivot9 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns=["Class","Subject"]
)

print("\nMultiple Columns")
print(pivot9)

# ==================================================
# 10. Multiple Rows + Multiple Columns
# ==================================================

pivot10 = pd.pivot_table(
    df,
    values="Marks",
    index=["Class","Student"],
    columns=["Subject"]
)

print("\nMultiple Rows and Columns")
print(pivot10)

# ==================================================
# 11. Fill Missing Values
# ==================================================

pivot11 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    fill_value=0
)

print("\nFill Missing Values")
print(pivot11)

# ==================================================
# 12. Grand Totals
# ==================================================

pivot12 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    margins=True
)

print("\nGrand Totals")
print(pivot12)

# ==================================================
# 13. Grand Totals with Custom Name
# ==================================================

pivot13 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    margins=True,
    margins_name="Total"
)

print("\nCustom Total Name")
print(pivot13)

# ==================================================
# 14. Fill Missing + Sum + Totals
# ==================================================

pivot14 = pd.pivot_table(
    df,
    values="Marks",
    index="Student",
    columns="Subject",
    aggfunc="sum",
    fill_value=0,
    margins=True
)

print("\nEverything Together")
print(pivot14)



#2
