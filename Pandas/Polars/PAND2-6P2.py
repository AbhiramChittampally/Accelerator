#PY2.6 — Part 7: Polars Lazy API — .lazy(), .collect(), scan_csv(), Filter Pushdown & Projection Pushdown
import polars as pl

result = (
    pl.scan_csv("data.csv")
    .filter(
        pl.col("column") > value
    )
    .with_columns(
        expression.alias("NewColumn")
    )
    .group_by("GroupColumn")
    .agg([
        pl.col("Value")
        .sum()
        .alias("Total"),

        pl.col("ID")
        .count()
        .alias("Count")
    ])
    .sort(
        "Total",
        descending=True
    )
    .collect()
)

print(result)
# PY2.6 — Part 8: Why Polars Is Faster Than Pandas — Rust, GIL, Multi-Threading, SIMD & Apache Arrow
#example
import polars as pl

result = (
    pl.scan_parquet("orders.parquet")
    .filter(
        (pl.col("Category") == "Electronics")
        &
        (pl.col("Revenue") > 10000)
    )
    .group_by("Region")
    .agg(
        pl.col("Revenue")
        .sum()
        .alias("TotalRevenue")
    )
    .collect()
)

print(result)
#realworld bp
import polars as pl

result = (
    pl.scan_parquet("orders.parquet")
    .filter(
        pl.col("Revenue") > 1000
    )
    .with_columns(
        (
            pl.col("Revenue") * 0.20
        ).alias("Profit")
    )
    .group_by("Category")
    .agg([
        pl.col("Profit")
        .sum()
        .alias("TotalProfit"),

        pl.col("Revenue")
        .mean()
        .alias("AverageRevenue")
    ])
    .sort(
        "TotalProfit",
        descending=True
    )
    .collect()
)

print(result)


#Complete Feature Engineering Example
# PY2.6 — Part 9: Polars Expression API in Depth
import polars as pl

df = pl.DataFrame({
    "OrderID": ["O101", "O102", "O103", "O104", "O105"],
    "Customer": ["Ravi", "Priya", "Rahul", "Anu", "Kiran"],
    "Category": [
        "Electronics",
        "Fashion",
        "Electronics",
        "Fashion",
        "Electronics"
    ],
    "Quantity": [2, 5, 3, 4, 1],
    "Revenue": [5000, 2000, 8000, 3500, 1000]
})

result = (
    df
    .filter(
        pl.col("Quantity") >= 2
    )
    .with_columns([
        (
            pl.col("Revenue")
            / pl.col("Quantity")
        )
        .alias("RevenuePerItem"),

        pl.col("Revenue")
        .mean()
        .over("Category")
        .alias("CategoryAverage"),

        pl.when(
            pl.col("Revenue") > 5000
        )
        .then(
            pl.lit("High")
        )
        .when(
            pl.col("Revenue") > 2000
        )
        .then(
            pl.lit("Medium")
        )
        .otherwise(
            pl.lit("Low")
        )
        .alias("RevenueTier")
    ])
    .group_by("Category")
    .agg([
        pl.col("Revenue")
        .sum()
        .alias("TotalRevenue"),

        pl.col("RevenuePerItem")
        .mean()
        .alias("AverageRevenuePerItem"),

        pl.col("OrderID")
        .count()
        .alias("OrderCount")
    ])
    .sort(
        "TotalRevenue",
        descending=True
    )
)

print(result)
#Complete Placement BP
import polars as pl

df = pl.read_csv("data.csv")

result = (
    df
    .filter(
        pl.col("Value") > 100
    )
    .with_columns([
        (
            pl.col("Value") * 0.10
        ).alias("Bonus"),

        pl.when(
            pl.col("Value") > 1000
        )
        .then(
            pl.lit("High")
        )
        .otherwise(
            pl.lit("Low")
        )
        .alias("CategoryLevel"),

        pl.col("Value")
        .mean()
        .over("Category")
        .alias("CategoryAverage")
    ])
    .group_by("Category")
    .agg([
        pl.col("Value")
        .sum()
        .alias("TotalValue"),

        pl.col("Value")
        .mean()
        .alias("AverageValue")
    ])
    .sort(
        "TotalValue",
        descending=True
    )
)

print(result)
#PY2.6 — Part 10: Polars Lazy Execution, scan_csv(), scan_parquet() and Query Optimisation
#Real Business Lazy Pipeline
import polars as pl

result = (
    pl.scan_csv("sales.csv")

    .filter(
        pl.col("IsReturned") == False
    )

    .with_columns([
        pl.col("Revenue")
        .log1p()
        .alias("LogRevenue"),

        pl.col("Revenue")
        .mean()
        .over("Category")
        .alias("CategoryAverage")
    ])

    .group_by("Category")

    .agg([
        pl.col("Revenue")
        .sum()
        .alias("TotalRevenue"),

        pl.col("LogRevenue")
        .mean()
        .alias("MeanLogRevenue"),

        pl.col("OrderID")
        .count()
        .alias("Orders")
    ])

    .sort(
        "TotalRevenue",
        descending=True
    )

    .collect()
)

print(result)


#Placement Boilerplate — Lazy CSV Analytics
import polars as pl

result = (
    pl.scan_csv("data.csv")

    .filter(
        pl.col("Value") > 100
    )

    .with_columns([
        (
            pl.col("Value") * 0.10
        )
        .alias("Bonus"),

        pl.col("Value")
        .mean()
        .over("Category")
        .alias("CategoryAverage")
    ])

    .group_by("Category")

    .agg([
        pl.col("Value")
        .sum()
        .alias("TotalValue"),

        pl.col("Value")
        .mean()
        .alias("AverageValue")
    ])

    .sort(
        "TotalValue",
        descending=True
    )

    .collect()
)

print(result)