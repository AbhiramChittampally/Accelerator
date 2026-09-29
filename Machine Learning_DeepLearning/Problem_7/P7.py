import pandas as pd
import numpy as np

# File 1: User Activity Logs

activity_data = {
    'User_ID': [f'USR_{100+i}' for i in range(50)],
    'Device_ID': [f'DEV_{(i%10)+1}' for i in range(50)],
    'Daily_Listening_Mins': [
        180, 25, 210, 40, 190, 30, 220, 35, 175, 20,
        195, 28, 205, 45, 185, 22, 215, 38, 170, 24,
        200, 32, 225, 42, 180, 26, 210, 36, 190, 21,
        198, 29, 208, 48, 178, 23, 218, 39, 172, 27,
        202, 33, 222, 41, 182, 25, 212, 37, 188, 22
    ],
    'Playlists_Created': [
        25, 2, 30, 3, 22, 1, 35, 4, 20, 1,
        26, 2, 28, 4, 21, 1, 32, 3, 19, 1,
        27, 2, 34, 4, 23, 2, 29, 3, 24, 1,
        26, 2, 31, 5, 20, 1, 33, 3, 18, 2,
        28, 3, 36, 4, 22, 1, 30, 3, 25, 1
    ],
    'Skip_Ratio': [
        0.12, 0.65, 0.08, 0.58, 0.15, 0.70, 0.05, 0.60, 0.10, 0.75,
        0.11, 0.62, 0.09, 0.55, 0.14, 0.68, 0.06, 0.59, 0.13, 0.72,
        0.10, 0.64, 0.04, 0.56, 0.12, 0.66, 0.08, 0.57, 0.15, 0.74,
        0.09, 0.61, 0.07, 0.54, 0.11, 0.69, 0.05, 0.58, 0.12, 0.63,
        0.10, 0.65, 0.04, 0.55, 0.13, 0.67, 0.07, 0.58, 0.14, 0.71
    ],
    'Podcast_Listening_Pct': [
        0.45, 0.05, 0.50, 0.10, 0.40, 0.02, 0.55, 0.08, 0.38, 0.01,
        0.46, 0.04, 0.48, 0.12, 0.41, 0.03, 0.52, 0.09, 0.39, 0.02,
        0.47, 0.06, 0.54, 0.11, 0.42, 0.05, 0.49, 0.08, 0.40, 0.01,
        0.45, 0.04, 0.51, 0.13, 0.37, 0.02, 0.53, 0.09, 0.38, 0.05,
        0.46, 0.07, 0.56, 0.10, 0.43, 0.03, 0.50, 0.08, 0.41, 0.02
    ]
}

# File 2: Subscription Metadata

sub_data = {
    'User_ID': [f'USR_{100+i}' for i in range(50)],
    'Account_Age_Months': [
        24, 2, 36, 4, 18, 1, 48, 5, 12, 1,
        28, 3, 32, 6, 16, 2, 42, 4, 14, 1,
        30, 3, 44, 5, 20, 2, 34, 4, 22, 1,
        26, 3, 38, 7, 15, 2, 46, 4, 13, 2,
        29, 3, 50, 6, 17, 1, 35, 4, 21, 1
    ],
    'Monthly_Fee_USD': [
        14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 9.99, 0.00,
        14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 9.99, 0.00,
        14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00,
        14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 9.99, 0.00,
        14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 14.99, 0.00
    ]
}

# File 3: Device & Platform Logs

device_data = {
    'Device_ID': [f'DEV_{i}' for i in range(1, 11)],
    'Primary_OS': [
        'iOS', 'Android', 'iOS', 'Android', 'WebOS',
        'iOS', 'Android', 'iOS', 'Android', 'Windows'
    ],
    'App_Version_Code': [
        4.5, 4.1, 4.5, 4.2, 3.9,
        4.5, 4.1, 4.5, 4.2, 4.0
    ]
}

df_activity = pd.DataFrame(activity_data)
df_sub = pd.DataFrame(sub_data)
df_device = pd.DataFrame(device_data)

# TASK 1 — Multi-Table Unsupervised Dataset Merging

master_df = df_activity.merge(
    df_sub,
    on="User_ID",
    how="inner"
)

master_df = master_df.merge(
    df_device,
    on="Device_ID",
    how="inner"
)

# TASK 2 — Paradigm & Label Absence Verification

target_status = "None (Unsupervised Learning)"
paradigm = "Unsupervised Learning / Clustering"

# TASK 3 — Feature Space Scale & Variance Inspection

numeric_features = [
    "Daily_Listening_Mins",
    "Playlists_Created",
    "Skip_Ratio",
    "Podcast_Listening_Pct",
    "Account_Age_Months"
]

X = master_df[numeric_features]

range_analysis = pd.DataFrame({
    "Min": X.min(),
    "Max": X.max()
})

range_analysis["Span"] = (
    range_analysis["Max"] - range_analysis["Min"]
)

largest_scale_feature = range_analysis["Span"].idxmax()
smallest_scale_feature = range_analysis["Span"].idxmin()

# TASK 4 — Heuristic Baseline Segmentation

power_condition = (
    (master_df["Daily_Listening_Mins"] > 100) &
    (master_df["Monthly_Fee_USD"] > 0)
)

master_df["Cluster"] = np.where(
    power_condition,
    0,
    1
)

cluster_counts = master_df["Cluster"].value_counts().sort_index()
cluster_percentages = (
    cluster_counts / len(master_df) * 100
)

# TASK 5 — Cluster Centroid Profiling

cluster_profile = master_df.groupby("Cluster")[
    numeric_features
].mean()

# TASK 6 — Supervised vs Unsupervised Paradigm Matrix

comparison_data = [
    [
        "Input Data",
        "Features (X) + Target (y)",
        "Features (X) Only"
    ],
    [
        "Primary Goal",
        "Predict Target Outcome",
        "Discover Latent Clusters/Patterns"
    ],
    [
        "Evaluation Metric",
        "Accuracy, RMSE, F1-Score",
        "Silhouette Score, Inertia"
    ],
    [
        "Common Algorithms",
        "Linear Reg, Decision Trees",
        "K-Means, DBSCAN, Agglomerative"
    ]
]

comparison_df = pd.DataFrame(
    comparison_data,
    columns=[
        "FEATURE",
        "SUPERVISED LEARNING",
        "UNSUPERVISED LEARNING"
    ]
)
print()
print("========================================================================================")
print("FEATURE                 SUPERVISED LEARNING             UNSUPERVISED LEARNING")
print("========================================================================================")

for _, row in comparison_df.iterrows():
    print(
        f"{row['FEATURE']:<24}"
        f"{row['SUPERVISED LEARNING']:<34}"
        f"{row['UNSUPERVISED LEARNING']}"
    )

print("========================================================================================")

# FINAL OUTPUT

print("========== CUSTOMER BEHAVIOR UNSUPERVISED CLUSTERING ==========")
print()

print(f"Master Dataset Records     : {len(master_df)}")
print(f"Total Input Features       : {len(X.columns)}")
print(f"Target Vector Status       : {target_status}")
print()

print("Feature Variance & Scale Summary:")

largest_min = range_analysis.loc[
    largest_scale_feature, "Min"
]
largest_max = range_analysis.loc[
    largest_scale_feature, "Max"
]

smallest_min = range_analysis.loc[
    smallest_scale_feature, "Min"
]
smallest_max = range_analysis.loc[
    smallest_scale_feature, "Max"
]

print(
    f"- Largest Scale Feature    : "
    f"{largest_scale_feature} "
    f"({largest_min:g} - {largest_max:g})"
)

print(
    f"- Smallest Scale Feature   : "
    f"{smallest_scale_feature} "
    f"({smallest_min:g} - {smallest_max:g})"
)

print(
    "- Normalization Requirement: "
    "MANDATORY (Distance metrics sensitive to feature magnitude)"
)

print()
print("Heuristic Segmentation Results:")

print(
    f"- Cluster 0 (Power Users)  : "
    f"{cluster_counts.get(0, 0)} Users | "
    f"Mean Listening = "
    f"{cluster_profile.loc[0, 'Daily_Listening_Mins']:.2f} mins | "
    f"Mean Skips = "
    f"{cluster_profile.loc[0, 'Skip_Ratio']:.3f}"
)

print(
    f"- Cluster 1 (Casual Users) : "
    f"{cluster_counts.get(1, 0)} Users | "
    f"Mean Listening = "
    f"{cluster_profile.loc[1, 'Daily_Listening_Mins']:.2f} mins | "
    f"Mean Skips = "
    f"{cluster_profile.loc[1, 'Skip_Ratio']:.3f}"
)


print()
print("Conclusion:")
print(
    "In the absence of ground-truth target labels, multi-table clustering "
    "isolates distinct user behavior archetypes using spatial distance metrics. "
    "Feature scaling ensures balanced feature contributions during geometric clustering."
)