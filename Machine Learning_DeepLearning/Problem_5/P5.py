import pandas as pd
import numpy as np

# TASK 1 — Dataset Construction

data = {
    "Patient_ID": [
        "P_501", "P_502", "P_503", "P_504", "P_505",
        "P_506", "P_507", "P_508", "P_509", "P_510"
    ],
    "Heart_Rate_BPM": [72, 125, 95, 68, 140, 88, 75, 130, 92, 70],
    "Systolic_BP": [120, 165, 138, 115, 180, 130, 122, 170, 135, 118],
    "Oxygen_Sat_Pct": [98, 89, 94, 99, 85, 95, 97, 88, 93, 98],
    "Age": [35, 68, 45, 28, 75, 52, 40, 62, 50, 30],
    "Triage_Category": [
        "General", "ICU", "Urgent", "General", "ICU",
        "Urgent", "General", "ICU", "Urgent", "General"
    ]
}

df = pd.DataFrame(data)

# TASK 2 — Supervised Paradigm Identification

supervised_paradigm = "Multi-Class Classification (Discrete Categorical Target)"

# TASK 3 — Input-Output Splitting

features = ["Heart_Rate_BPM", "Systolic_BP", "Oxygen_Sat_Pct", "Age"]

X = df[features]
y = df["Triage_Category"]

# TASK 4 — Multi-Class Target Distribution

class_counts = y.value_counts().reindex(
    ["General", "Urgent", "ICU"]
)

class_percentages = (class_counts / len(y)) * 100

# TASK 5 — Group-Wise Feature Means

group_averages = df.groupby("Triage_Category")[
    ["Heart_Rate_BPM", "Systolic_BP", "Oxygen_Sat_Pct"]
].mean().reindex(["General", "Urgent", "ICU"])

# TASK 6 — Supervised Algorithm Selection Guide

algorithm_guidance = {
    "Logistic Regression":
        "Suitable for multi-class classification and provides interpretable linear class boundaries.",
    "Decision Trees":
        "Suitable for interpretable clinical rule boundaries using feature-based decision splits.",
    "K-Nearest Neighbors":
        "Suitable for classification based on similarity to nearby patients; feature scaling is important for distance-based learning."
}

# OUTPUT

print("========== EMERGENCY PATIENT TRIAGE ANALYSIS ==========")
print()

print(f"Dataset Shape              : {df.shape[0]} Rows, {df.shape[1]} Columns")
print(f"Supervised Paradigm        : {supervised_paradigm}")
print()

print("Features (X)               : {for x in X.columns: print(x)}")
print(f"Target (y)                 : {y.name}")
print()

print("Class Distribution:")
for category in ["General", "Urgent", "ICU"]:
    print(
        f"- {category:<24}: "
        f"{class_counts[category]} "
        f"({class_percentages[category]:.1f}%)"
    )

print()
print("Triage Level Group Averages:")
print(group_averages.to_string())

print()
print("Algorithm Guidance:")
for algorithm, guidance in algorithm_guidance.items():
    print(f"- {algorithm}: {guidance}")