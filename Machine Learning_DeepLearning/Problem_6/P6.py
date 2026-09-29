# copy your solution

import pandas as pd
import numpy as np

# File 1: Property Listings

listings_data = {
    'Property_ID': [f'PROP_{100+i}' for i in range(50)],
    'Neighborhood_ID': [f'NGH_{(i%5)+1}' for i in range(50)],
    'Area_SqFt': [2500, 1200, 4000, 1800, 3200, 950, 2800, 1500, 4500, 2100,
                  3100, 1300, 4200, 1900, 3300, 1000, 4600, 1600, 3400, 2200,
                  2900, 1400, 4100, 2000, 3500, 1100, 4700, 1700, 3600, 2300,
                  3000, 1250, 4300, 1850, 3250, 1050, 4400, 1650, 3350, 2150,
                  2850, 1350, 3950, 1750, 3450, 1150, 4800, 1550, 3700, 2250],
    'Bedrooms': [4, 2, 5, 3, 4, 1, 4, 2, 5, 3,
                 4, 2, 5, 3, 4, 1, 5, 2, 4, 3,
                 4, 2, 5, 3, 4, 1, 5, 2, 4, 3,
                 4, 2, 5, 3, 4, 1, 5, 2, 4, 3,
                 4, 2, 5, 3, 4, 1, 5, 2, 4, 3],
    'Building_Age_Yrs': [8, 25, 2, 15, 5, 30, 10, 18, 1, 12,
                         6, 22, 3, 14, 4, 28, 1, 16, 5, 11,
                         9, 20, 2, 13, 4, 26, 1, 17, 3, 10,
                         7, 24, 2, 15, 5, 29, 1, 18, 4, 12,
                         8, 21, 3, 16, 5, 27, 1, 19, 3, 11],
    'Price_USD_M': [1.25, 0.42, 2.85, 0.68, 1.95, 0.29, 1.40, 0.55, 3.20, 0.92,
                    1.80, 0.48, 2.95, 0.72, 1.90, 0.32, 3.35, 0.58, 2.05, 0.98,
                    1.48, 0.51, 2.88, 0.78, 2.15, 0.35, 3.45, 0.62, 2.25, 1.05,
                    1.65, 0.45, 3.05, 0.70, 1.98, 0.31, 3.15, 0.60, 2.10, 0.95,
                    1.42, 0.49, 2.75, 0.65, 2.20, 0.38, 3.50, 0.56, 2.30, 1.02]
}

# File 2: Neighborhood Analytics

neighborhood_data = {
    'Neighborhood_ID': [f'NGH_{i}' for i in range(1, 6)],
    'Distance_City_KM': [2.5, 18.0, 5.0, 12.0, 1.2],
    'School_Rating': [9.2, 5.5, 8.8, 6.8, 9.6],
    'Crime_Index': [12.0, 45.0, 18.0, 32.0, 8.5]
}

# File 3: Macroeconomic Indicators

macro_data = {
    'Property_ID': [f'PROP_{100+i}' for i in range(50)],
    'Interest_Rate_Pct': [
        6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5,
        6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8,
        7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0,
        6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2,
        6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4
    ],
    'Property_Tax_Rate': [
        0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012, 0.012,
        0.014, 0.014, 0.014, 0.014, 0.014, 0.014, 0.014, 0.014, 0.014, 0.014,
        0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015,
        0.011, 0.011, 0.011, 0.011, 0.011, 0.011, 0.011, 0.011, 0.011, 0.011,
        0.013, 0.013, 0.013, 0.013, 0.013, 0.013, 0.013, 0.013, 0.013, 0.013
    ]
}

df_listings = pd.DataFrame(listings_data)
df_neighborhood = pd.DataFrame(neighborhood_data)
df_macro = pd.DataFrame(macro_data)

# TASK 1 — Multi-Source Relational Data Merging

master_df = df_listings.merge(
    df_neighborhood,
    on="Neighborhood_ID",
    how="inner"
)

master_df = master_df.merge(
    df_macro,
    on="Property_ID",
    how="inner"
)

# TASK 2 — Supervised Paradigm Verification

total_records = len(master_df)
total_columns = len(master_df.columns)
target_variable = "Price_USD_M"
target_dtype = master_df[target_variable].dtype
supervised_paradigm = "Regression (Continuous Target)"

# TASK 3 — Feature Space & Target Structuring

feature_columns = [
    "Area_SqFt",
    "Bedrooms",
    "Building_Age_Yrs",
    "Distance_City_KM",
    "School_Rating",
    "Crime_Index",
    "Interest_Rate_Pct",
    "Property_Tax_Rate"
]

X = master_df[feature_columns]
y = master_df[target_variable]

# TASK 4 — Pearson Correlation Matrix Analysis

correlation_matrix = master_df.select_dtypes(
    include=np.number
).corr()

price_correlations = correlation_matrix[target_variable].drop(
    target_variable
)

strongest_positive_feature = price_correlations.idxmax()
strongest_positive_value = price_correlations.max()

strongest_negative_feature = price_correlations.idxmin()
strongest_negative_value = price_correlations.min()

# TASK 5 — Sub-Group Property Valuation Metrics

high_value = master_df[master_df["Price_USD_M"] > 1.5]
moderate_value = master_df[master_df["Price_USD_M"] <= 1.5]

high_value_metrics = high_value[
    ["Area_SqFt", "Distance_City_KM", "School_Rating"]
].mean()

moderate_value_metrics = moderate_value[
    ["Area_SqFt", "Distance_City_KM", "School_Rating"]
].mean()

# Final Target Metrics

minimum_price = y.min()
maximum_price = y.max()
mean_price = y.mean()

# TASK 6 — Algorithm Selection Guide

algorithm_guidance = {
    "Linear Regression":
        "Baseline linear relationship mapping; fast and interpretable.",
    "Ridge / Lasso":
        "Handles multicollinearity between Area_SqFt and Bedrooms.",
    "Decision Tree Regressor":
        "Captures non-linear local neighborhood threshold effects."
}

# OUTPUT

print("========== COMMERCIAL PROPERTY REGRESSION ANALYSIS ==========")
print()

print(f"Master Dataset Records     : {total_records}")
print(f"Total Feature Attributes   : {len(X.columns)}")
print(f"Supervised Paradigm        : {supervised_paradigm}")
print()

print("Target Metrics (Price_USD_M):")
print(f"- Minimum Price             : ${minimum_price:.2f}M")
print(f"- Maximum Price             : ${maximum_price:.2f}M")
print(f"- Mean Price                : ${mean_price:.2f}M")
print()

print("Key Feature Correlations:")
print(
    f"- Top Positive Predictor   : "
    f"{strongest_positive_feature} (+{strongest_positive_value:.3f})"
)
print(
    f"- Top Negative Predictor   : "
    f"{strongest_negative_feature} ({strongest_negative_value:.3f})"
)
print()

print("Valuation Sub-Group Profiling:")
print(
    f"- High Value (> $1.5M)     : "
    f"Mean Area = {high_value_metrics['Area_SqFt']:,.2f} SqFt | "
    f"Mean Distance = {high_value_metrics['Distance_City_KM']:.2f} KM | "
    f"Mean School Rating = {high_value_metrics['School_Rating']:.2f}"
)
print(
    f"- Moderate Value (<= $1.5M): "
    f"Mean Area = {moderate_value_metrics['Area_SqFt']:,.2f} SqFt | "
    f"Mean Distance = {moderate_value_metrics['Distance_City_KM']:.2f} KM | "
    f"Mean School Rating = {moderate_value_metrics['School_Rating']:.2f}"
)
print()

print("REGRESSION ALGORITHM MAP:")
for number, (algorithm, guidance) in enumerate(
    algorithm_guidance.items(), start=1
):
    print(f"{number}. {algorithm} : {guidance}")

print()
print("Conclusion:")
print(
    "Multi-table integration confirms property prices are strongly driven "
    "by continuous physical attributes (Area) and spatial neighborhood "
    "metrics (Distance/School Rating). Linear and Regularized Regression "
    "models are optimal candidate baselines."
)