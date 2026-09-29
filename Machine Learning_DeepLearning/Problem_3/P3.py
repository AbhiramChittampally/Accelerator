# PROJECT 13 — ENTERPRISE LOGISTICS & FLEET DELAY ANALYTICS

import pandas as pd
import numpy as np


# FILE 1 — SHIPMENTS DATA

shipments_data = {
    "Shipment_ID": [f"SHP_{100+i}" for i in range(50)],
    "Vehicle_ID": [f"VEH_{(i%10)+1}" for i in range(50)],
    "Region_ID": [f"REG_{(i%5)+1}" for i in range(50)],

    "Distance_KM": [
        120, 450, 80, 600, 310, 150, 520, 210, 750, 90,
        340, 180, 620, 290, 410, 110, 800, 230, 500, 140,
        380, 260, 710, 190, 440, 160, 680, 220, 530, 130,
        360, 270, 740, 170, 490, 150, 650, 240, 580, 200,
        420, 280, 790, 180, 460, 210, 630, 250, 510, 300
    ],

    "Cargo_Weight_Tons": [
        5.2, 18.0, 2.1, 22.5, 12.0, 4.5, 19.8, 8.1, 24.0, 3.0,
        14.2, 6.0, 21.0, 10.5, 16.0, 4.0, 25.0, 7.5, 18.5, 5.0,
        13.5, 9.0, 23.0, 6.5, 17.0, 5.5, 22.0, 8.0, 19.0, 4.8,
        13.0, 9.5, 24.5, 6.2, 17.5, 5.8, 21.5, 8.5, 20.0, 7.0,
        15.5, 10.0, 24.8, 6.8, 16.5, 7.8, 21.2, 8.8, 18.8, 11.0
    ],

    "Actual_Delay_Hours": [
        0.5, 4.2, 0.0, 6.5, 1.2, 0.0, 5.1, 0.8, 8.0, 0.0,
        2.5, 0.2, 7.1, 1.0, 3.8, 0.0, 9.2, 0.5, 4.8, 0.1,
        2.8, 0.9, 7.8, 0.3, 3.5, 0.1, 6.9, 0.6, 5.2, 0.0,
        2.1, 0.7, 8.5, 0.2, 4.1, 0.0, 6.2, 0.8, 5.5, 0.4,
        3.0, 1.1, 8.9, 0.3, 3.9, 0.7, 6.0, 1.0, 4.9, 1.5
    ],

    "Is_Delayed": [
        "No", "Yes", "No", "Yes", "No",
        "No", "Yes", "No", "Yes", "No",
        "Yes", "No", "Yes", "No", "Yes",
        "No", "Yes", "No", "Yes", "No",
        "Yes", "No", "Yes", "No", "Yes",
        "No", "Yes", "No", "Yes", "No",
        "Yes", "No", "Yes", "No", "Yes",
        "No", "Yes", "No", "Yes", "No",
        "Yes", "No", "Yes", "No", "Yes",
        "No", "Yes", "No", "Yes", "No"
    ]
}


# FILE 2 — FLEET METADATA

fleet_data = {
    "Vehicle_ID": [f"VEH_{i}" for i in range(1, 11)],
    "Vehicle_Age_Years": [2, 8, 1, 12, 5, 3, 9, 4, 11, 2],
    "Maintenance_Score": [95, 62, 98, 45, 78, 88, 55, 82, 48, 91],
    "Driver_Experience_Yrs": [8, 3, 12, 2, 6, 9, 4, 7, 1, 10]
}


# FILE 3 — REGIONAL WEATHER LOGS

weather_data = {
    "Region_ID": [f"REG_{i}" for i in range(1, 6)],
    "Weather_Condition": [
        "Clear",
        "Heavy Rain",
        "Fog",
        "Clear",
        "Storm"
    ],
    "Traffic_Congestion_Index": [
        2.1, 8.5, 6.2, 3.0, 9.1
    ]
}


# CREATE DATAFRAMES

df_shipments = pd.DataFrame(shipments_data)
df_fleet = pd.DataFrame(fleet_data)
df_weather = pd.DataFrame(weather_data)


# TASK 1 — MULTI-SOURCE DATA MERGING

integrated_df = df_shipments.merge(
    df_fleet,
    on="Vehicle_ID",
    how="inner"
)

integrated_df = integrated_df.merge(
    df_weather,
    on="Region_ID",
    how="inner"
)


print("\n========== TASK 1: MULTI-SOURCE DATA MERGING ==========")
print(integrated_df)


# TASK 2 — FLEET OPERATIONAL PROFILING

row_count = integrated_df.shape[0]

merged_column_count = integrated_df.shape[1]

total_combined_features = merged_column_count - 1

memory_footprint = integrated_df.memory_usage(
    deep=True
).sum()


print("\n========== TASK 2: FLEET OPERATIONAL PROFILING ==========")

print("Row Count               :", row_count)
print("Merged Column Count     :", merged_column_count)
print("Total Combined Features :", total_combined_features)
print("Memory Footprint        :", memory_footprint, "bytes")

print("\nSchema Data Types:")
print(integrated_df.dtypes)


# TASK 3 — DYNAMIC FEATURE AND TARGET SEPARATION

non_predictive_keys = [
    "Shipment_ID",
    "Vehicle_ID",
    "Region_ID"
]

target = "Is_Delayed"

X = integrated_df.drop(
    columns=non_predictive_keys + [target]
)

y = integrated_df[target]

numerical_features = X.select_dtypes(
    include=np.number
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=np.number
).columns.tolist()


print("\n========== TASK 3: FEATURE AND TARGET SEPARATION ==========")

print("Target :", target)

print("\nNumerical Features:")

for feature in numerical_features:
    print(feature)

print("\nCategorical Features:")

for feature in categorical_features:
    print(feature)

print("\nDropped Non-Predictive Keys:")

for key in non_predictive_keys:
    print(key)


# TASK 4 — TARGET IMBALANCE AND DELAY DISTRIBUTION

target_counts = y.value_counts()

target_proportions = (
    y.value_counts(normalize=True) * 100
)

group_metrics = integrated_df.groupby(
    "Is_Delayed"
).agg(
    Mean_Distance=("Distance_KM", "mean"),
    Mean_Maintenance=("Maintenance_Score", "mean")
)


print("\n========== TASK 4: TARGET IMBALANCE AND DELAY DISTRIBUTION ==========")

print("Target Class Counts:")
print(target_counts)

print("\nTarget Class Proportions:")

for label in ["No", "Yes"]:
    print(
        f"{label} = {target_counts[label]} "
        f"({target_proportions[label]:.1f}%)"
    )

print("\nGroup Metrics:")

print(
    "Mean Distance - Delayed :",
    f"{group_metrics.loc['Yes', 'Mean_Distance']:.2f} KM"
)

print(
    "Mean Distance - On-Time :",
    f"{group_metrics.loc['No', 'Mean_Distance']:.2f} KM"
)

print(
    "Mean Maintenance - Delayed :",
    f"{group_metrics.loc['Yes', 'Mean_Maintenance']:.2f} Score"
)

print(
    "Mean Maintenance - On-Time :",
    f"{group_metrics.loc['No', 'Mean_Maintenance']:.2f} Score"
)


# TASK 5 — MULTI-FACTOR RULE ENGINE

rule_condition = (
    (
        (integrated_df["Distance_KM"] > 400)
        &
        (integrated_df["Maintenance_Score"] < 60)
    )
    |
    (
        integrated_df["Weather_Condition"].isin(
            ["Storm", "Heavy Rain"]
        )
    )
)

integrated_df["Prediction"] = np.where(
    rule_condition,
    "Yes",
    "No"
)


print("\n========== TASK 5: MULTI-FACTOR RULE ENGINE ==========")

print(
    "Rule: (Distance_KM > 400 AND Maintenance_Score < 60)"
    " OR Weather_Condition IN ['Storm', 'Heavy Rain']"
)

print("\nRule Predictions:")

print(
    integrated_df[
        [
            "Shipment_ID",
            "Is_Delayed",
            "Prediction"
        ]
    ].to_string(index=False)
)


# TASK 6 — RULE CONFUSION AND ACCURACY ASSESSMENT

correct_predictions = (
    integrated_df["Prediction"] ==
    integrated_df["Is_Delayed"]
).sum()

total_predictions = integrated_df.shape[0]

rule_accuracy = (
    correct_predictions /
    total_predictions
) * 100

false_positives = (
    (
        integrated_df["Prediction"] == "Yes"
    )
    &
    (
        integrated_df["Is_Delayed"] == "No"
    )
).sum()

false_negatives = (
    (
        integrated_df["Prediction"] == "No"
    )
    &
    (
        integrated_df["Is_Delayed"] == "Yes"
    )
).sum()


print("\n========== TASK 6: RULE CONFUSION AND ACCURACY ==========")

print("Correct Predictions :", correct_predictions)
print("Total Predictions   :", total_predictions)
print(f"Rule Accuracy       : {rule_accuracy:.2f}%")
print("False Positives     :", false_positives)
print("False Negatives     :", false_negatives)


# TASK 7 — OPERATIONAL FAILURE ANALYSIS

failed_cases = integrated_df[
    integrated_df["Prediction"] !=
    integrated_df["Is_Delayed"]
]


print("\n========== TASK 7: OPERATIONAL FAILURE ANALYSIS ==========")

print("\nFailed Rule Cases:")

print(
    failed_cases[
        [
            "Shipment_ID",
            "Distance_KM",
            "Maintenance_Score",
            "Weather_Condition",
            "Traffic_Congestion_Index",
            "Actual_Delay_Hours",
            "Is_Delayed",
            "Prediction"
        ]
    ].to_string(index=False)
)

print("\nWhy the Rule Fails:")

print(
    "Static rules depend on fixed thresholds and conditions."
)

print(
    "They can miss complex interactions between distance, "
    "maintenance, weather, traffic and other operational factors."
)

print(
    "Machine learning models can learn these relationships "
    "from historical data instead of relying only on "
    "hand-coded threshold rules."
)


# FINAL EXPECTED OUTPUT

integrated_dataset_records = integrated_df.shape[0]

combined_features = integrated_df.shape[1]


print("\n========== ENTERPRISE LOGISTICS DELAY ANALYTICS ==========")

print(
    f"Integrated Dataset Records : {integrated_dataset_records}"
    f"\nTotal Combined Features    : {combined_features}"
)

print(
    "Target Class Distribution   :",
    f"No = {target_counts['No']} "
    f"({target_proportions['No']:.1f}%), "
    f"Yes = {target_counts['Yes']} "
    f"({target_proportions['Yes']:.1f}%)"
)

print("\nGroup Metrics (Delayed vs On-Time):")

print(
    "- Mean Distance            :",
    f"Delayed = {group_metrics.loc['Yes', 'Mean_Distance']:.2f} KM",
    "|",
    f"On-Time = {group_metrics.loc['No', 'Mean_Distance']:.2f} KM"
)

print(
    "- Mean Vehicle Maintenance :",
    f"Delayed = {group_metrics.loc['Yes', 'Mean_Maintenance']:.2f} Score",
    "|",
    f"On-Time = {group_metrics.loc['No', 'Mean_Maintenance']:.2f} Score"
)

print("\nRule Engine Evaluation:")

print(
    "- Rule Accuracy            :",
    f"{rule_accuracy:.2f}%"
)

print(
    "- False Positives          :",
    false_positives
)

print(
    "- False Negatives          :",
    false_negatives
)

print("\nConclusion:")

print(
    "Multi-table integration reveals that severe weather "
    "and low maintenance score interact non-linearly "
    "with distance. An ML algorithm dynamically weights "
    "these interactions without hand-coded threshold rules."
)