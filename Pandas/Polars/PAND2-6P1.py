# PY2.6 — Part 1
# Pandas vs Polars (Introduction)
import polars as pl

df = pl.read_csv("employees.csv")

print(df)

##EXAMPLE
import polars as pl

students = pl.DataFrame(
{
    "Name":["Ravi","Priya","John"],
    "Marks":[90,85,78]
})

print(students)

##EXAMPLE2
import polars as pl

employees = pl.DataFrame(
{
    "Employee":["Raj","Anu","Kiran"],
    "Salary":[50000,60000,55000]
})

print(employees)


##LazyLoad BP
import polars as pl

df = (
    pl.scan_csv("employees.csv")
      .filter(pl.col("Salary") > 50000)
      .select(["Name", "Salary"])
      .collect()
)

print(df)


##WHENEVER USING LAZY
import polars as pl

df = (
    pl.scan_csv("file.csv")
      .filter(...)
      .select(...)
      .group_by(...)
      .agg(...)
      .collect()
)


# # PY2.6 — Part 4
# Writing Polars Code (The Core Syntax)
#Example
import polars as pl

df=pl.read_csv("employees.csv")

result=(

df

.filter(pl.col("Salary")>50000)

.with_columns(

(pl.col("Salary")*0.1)

.alias("Bonus")

)

.select(

["Name","Salary","Bonus"]

)

.sort("Bonus")

)

print(result)
###Column ops
import polars as pl

students=pl.DataFrame(

{

"Name":["Ravi","Priya","John"],

"Marks":[90,85,70]

}

)

result=(

students

.filter(pl.col("Marks")>80)

.with_columns(

(pl.col("Marks")+5)

.alias("Bonus")

)

.sort("Bonus")

)

print(result)

#column ops bp
import polars as pl

df=pl.read_csv("employees.csv")

result=(

df

.filter(pl.col("Salary")>50000)

.with_columns(

(pl.col("Salary")*0.1)

.alias("Bonus")

)

.select(

["Name","Salary","Bonus"]

)

.sort("Bonus")

)

print(result)



###PY2.6 — Part 5
# group_by(), agg() and Aggregations in Polars
import polars as pl

df = pl.read_csv("file.csv")

result = (
    df
    .group_by("GroupColumn")
    .agg([
        pl.col("ValueColumn").sum().alias("Total"),
        pl.col("ValueColumn").mean().alias("Average"),
        pl.col("ValueColumn").min().alias("Minimum"),
        pl.col("ValueColumn").max().alias("Maximum"),
        pl.len().alias("Count")
    ])
    .sort("Total", descending=True)
)

print(result)


###PY2.6 — Part 6: Feature Engineering in Polars

##FLOW
# ADD/MODIFY COLUMNS
# ↓
# with_columns()

# COLUMN
# ↓
# pl.col()

# FIXED VALUE
# ↓
# pl.lit()

# IF
# ↓
# pl.when()

# THEN
# ↓
# .then()

# ELSE
# ↓
# .otherwise()

# GROUP CALCULATION WITHOUT REMOVING ROWS
# ↓
# .over()

# RANK
# ↓
# .rank()

# RENAME OUTPUT
# ↓
# .alias()


##FE BP
import polars as pl

df = pl.read_csv("data.csv")

result = df.with_columns([
    (
        pl.col("A") * pl.col("B")
    ).alias("CalculatedValue"),

    pl.col("Value")
    .mean()
    .over("Group")
    .alias("GroupAverage"),

    pl.col("Value")
    .rank("dense", descending=True)
    .over("Group")
    .alias("Rank"),

    pl.when(pl.col("Value") > 1000)
    .then(pl.lit("High"))
    .when(pl.col("Value") > 500)
    .then(pl.lit("Medium"))
    .otherwise(pl.lit("Low"))
    .alias("Category")
])

print(result)


