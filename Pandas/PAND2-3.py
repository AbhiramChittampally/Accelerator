import pandas as pd

df = pd.DataFrame({
    "Student":["Rahul","Priya"],
    "Math":[90,95],
    "Science":[80,88],
    "English":[85,91]
})

# # Melt
# long = pd.melt(
#     df,
#     id_vars="Student",
#     value_vars=["Math","Science","English"],
#     var_name="Subject",
#     value_name="Marks"
# )

# print(long)

# # Pivot back
# wide = long.pivot(
#     index="Student",
#     columns="Subject",
#     values="Marks"
# )

# print(wide)

# # Stack
# print(wide.stack())

# # Unstack
# print(wide.stack().unstack())




# #Datetime
import pandas as pd

df = pd.DataFrame({
    "Date":["2025-01-01",
            "2025-01-02",
            "2025-01-03"],
    "Sales":[500,700,900]
})

# Convert to datetime
df["Date"] = pd.to_datetime(df["Date"])

# # Extract components
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["MonthName"] = df["Date"].dt.month_name()
df["DayName"] = df["Date"].dt.day_name()

# print(df)

# Set datetime index
df = df.set_index("Date")

# print(df)

# Single date
# print(df.loc["2025-01-02"])

# # Date range
# print(df.loc["2025-01-01":"2025-01-03"])





# #resampling
# import pandas as pd

df = pd.DataFrame({
    "Date":[
        "2025-01-01",
        "2025-01-02",
        "2025-01-03",
        "2025-01-04"
    ],
    "Sales":[100,120,90,110]
})

# # Convert to datetime
df["Date"] = pd.to_datetime(df["Date"])

# # Make Date the index
df = df.set_index("Date")

# # Daily
# print(df.resample("D").sum())

# # Weekly
# print(df.resample("W").sum())

# # Monthly
# print(df.resample("ME").sum())   #("M") or ("ME")

# # Yearly
# print(df.resample("YE").sum())     #("Y") or ("YE")

# # Average
# print(df.resample("M").mean())

# # Maximum
# print(df.resample("M").max())

# # Minimum
# print(df.resample("M").min())

# # Count
# print(df.resample("M").count())

# # Multiple aggregations
# print(
#     df.resample("M").agg(
#         ["sum","mean","count","max","min"]
#     )
# )




# #rolling
# import pandas as pd

# df = pd.DataFrame({
#     "Sales":[100,120,90,110,130]
# })

# # Rolling Mean
# print(df["Sales"].rolling(3).mean())

# # Rolling Sum
# print(df["Sales"].rolling(3).sum())

# # Rolling Maximum
# print(df["Sales"].rolling(3).max())

# # Rolling Minimum
# print(df["Sales"].rolling(3).min())

# # Rolling Count
# print(df["Sales"].rolling(3).count())

# # Rolling Mean without NaN
# print(
#     df["Sales"].rolling(
#         window=3,
#         min_periods=1
#     ).mean()
# )




# #shift,diff,pct
# import pandas as pd

# df = pd.DataFrame({
#     "Sales":[100,120,90,110,150]
# })

# # Previous value
# df["Previous"] = df["Sales"].shift(1)

# # Next value
# df["Next"] = df["Sales"].shift(-1)

# # Difference
# df["Difference"] = df["Sales"].diff()

# # Difference with two rows before
# df["Difference2"] = df["Sales"].diff(2)

# # Percentage change
# df["Growth"] = df["Sales"].pct_change()

# # Percentage
# df["GrowthPercent"] = df["Sales"].pct_change()*100

# print(df)

