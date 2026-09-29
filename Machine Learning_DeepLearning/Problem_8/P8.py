# copy your solution

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# ============================================================
# INPUT DATA
# ============================================================
def run_pipeline():
    cust_profile_data = {
        'Customer_ID': [f'CUST_{200+i}' for i in range(50)],
        'Account_Tier': ['Silver', 'Gold', 'Bronze', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver',
                        'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold',
                        'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze',
                        'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver',
                        'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'East', 'Gold'],
        'Age': [34, 45, np.nan, 29, 52, 38, 24, np.nan, 41, 31,
                27, 49, 36, 43, np.nan, 50, 33, 28, 22, 47,
                39, 26, 51, 42, 30, np.nan, 46, 35, 25, 48,
                37, 32, 44, 23, 53, 40, np.nan, 29, 47, 31,
                26, 50, 43, 34, 21, 49, 38, 27, 45, 33],
        'Region': ['North', 'South', 'West', 'East', 'North', 'South', 'West', 'East', 'North', 'South',
                'West', 'East', 'North', 'South', 'West', 'East', 'North', 'South', 'West', 'East',
                'North', 'South', 'West', 'East', 'North', 'South', 'West', 'East', 'North', 'South',
                'West', 'East', 'North', 'South', 'West', 'East', 'North', 'South', 'West', 'East',
                'North', 'South', 'West', 'East', 'North', 'South', 'West', 'East', 'North', 'South']
    }

    cust_tx_data = {
        'Customer_ID': [f'CUST_{200+i}' for i in range(50)],
        'Total_Spend_USD': [1200.5, 4500.0, 300.2, 12500.0, 3800.0, 950.0, 210.0, 5100.0, 15000.0, 1100.0,
                            180.0, 4200.0, 1300.0, 11800.0, 250.0, 4900.0, 890.0, 13200.0, 190.0, 4600.0,
                            1050.0, 220.0, 5300.0, 11000.0, 980.0, np.nan, 4700.0, 14000.0, 310.0, 4400.0,
                            1150.0, 920.0, 12100.0, 150.0, 5600.0, 1080.0, 13500.0, 280.0, 4800.0, 1010.0,
                            230.0, 5200.0, 11900.0, 1120.0, 170.0, 5000.0, 12800.0, 850.0, 4300.0, 990.0],
        'Purchase_Frequency': [12, 35, 2, 85, 28, 8, 3, 38, 92, 10,
                            2, 31, 11, 78, 3, 36, 7, 88, 2, 33,
                            9, 3, 40, 75, 8, 1, 34, 90, 4, 32,
                            10, 8, 81, 1, 42, 9, 89, 3, 35, 11,
                            2, 37, 80, 12, 1, 38, 86, 7, 31, 9]
    }

    cust_engagement_data = {
        'Customer_ID': [f'CUST_{200+i}' for i in range(50)],
        'App_Sessions_Per_Month': [15, 42, 4, 95, 33, 11, 5, 48, 110, 14,
                                3, 39, 16, 88, 4, 44, 9, 102, 3, 41,
                                12, 5, 52, 82, 10, 2, 43, 105, 6, 38,
                                13, 10, 91, 2, 55, 12, 100, 4, 42, 15,
                                3, 46, 89, 14, 2, 47, 98, 8, 37, 11],
        'Is_High_Value': [0, 1, 0, 1, 1, 0, 0, 1, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                        0, 0, 1, 1, 0, 0, 1, 1, 0, 1,
                        0, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 1, 0, 0, 1, 1, 0, 1, 0]
    }


    df_profile = pd.DataFrame(cust_profile_data)
    df_tx = pd.DataFrame(cust_tx_data)
    df_engagement = pd.DataFrame(cust_engagement_data)


    # ============================================================
    # TASK 1 — MULTI-SOURCE RELATIONAL DATA JOIN
    # ============================================================

    master_df = df_profile.merge(
        df_tx,
        on="Customer_ID",
        how="inner"
    )

    master_df = master_df.merge(
        df_engagement,
        on="Customer_ID",
        how="inner"
    )

    print("\n========== TASK 1 — MASTER DATASET ==========")
    print(master_df.head())


    # ============================================================
    # TASK 2 — MISSING VALUE ANALYSIS & GROUP-WISE IMPUTATION
    # ============================================================

    missing_before = master_df.isnull().sum()

    age_missing_before = master_df["Age"].isnull().sum()
    spend_missing_before = master_df["Total_Spend_USD"].isnull().sum()

    age_tier_median = master_df.groupby(
        "Account_Tier"
    )["Age"].transform("median")

    spend_tier_median = master_df.groupby(
        "Account_Tier"
    )["Total_Spend_USD"].transform("median")

    master_df["Age"] = master_df["Age"].fillna(age_tier_median)

    master_df["Total_Spend_USD"] = master_df[
        "Total_Spend_USD"
    ].fillna(spend_tier_median)

    tier_medians = master_df.groupby("Account_Tier").agg(
        Median_Age=("Age", "median"),
        Median_Spend=("Total_Spend_USD", "median")
    )

    missing_after = master_df.isnull().sum().sum()


    print("\n========== TASK 2 — MISSING VALUE ANALYSIS ==========")

    print("\nMissing Values Before Imputation:")
    print("- Age             :", age_missing_before)
    print("- Total_Spend_USD :", spend_missing_before)

    print("\nImputed Metrics by Account_Tier (Age / Spend Medians):")

    for tier in ["Bronze", "Gold", "Platinum", "Silver"]:
        print(
            f"- {tier:<9}: "
            f"Median Age = {tier_medians.loc[tier, 'Median_Age']:.1f} | "
            f"Median Spend = ${tier_medians.loc[tier, 'Median_Spend']:,.2f}"
        )

    print("\nMissing Values After Imputation:", missing_after)


    # ============================================================
    # TASK 3 — CATEGORICAL VARIABLE ENCODING
    # ============================================================

    tier_mapping = {
        "Bronze": 1,
        "Silver": 2,
        "Gold": 3,
        "Platinum": 4
    }

    master_df["Account_Tier_Encoded"] = master_df[
        "Account_Tier"
    ].map(tier_mapping)

    region_encoded = pd.get_dummies(
        master_df["Region"],
        prefix="Region",
        drop_first=True,
        dtype=int
    )

    master_df = pd.concat(
        [master_df, region_encoded],
        axis=1
    )

    encoded_region_columns = [
        column for column in region_encoded.columns
    ]


    print("\n========== TASK 3 — CATEGORICAL ENCODING ==========")

    print("Encoded Columns:")
    print(
        "- Account_Tier_Encoded : Discrete Values",
        sorted(master_df["Account_Tier_Encoded"].unique().tolist())
    )

    print(
        "- One-Hot Region Columns:",
        ", ".join(encoded_region_columns),
        "(Region_East dropped as baseline)"
    )


    # ============================================================
    # TASK 4 — OUTLIER DETECTION & IQR CAPPING
    # ============================================================

    q1 = master_df["Total_Spend_USD"].quantile(0.25)
    q3 = master_df["Total_Spend_USD"].quantile(0.75)

    iqr = q3 - q1

    upper_bound = q3 + 1.5 * iqr

    outlier_mask = (
        master_df["Total_Spend_USD"] > upper_bound
    )

    outliers_detected = outlier_mask.sum()

    master_df.loc[
        outlier_mask,
        "Total_Spend_USD"
    ] = upper_bound


    print("\n========== TASK 4 — OUTLIER DETECTION ==========")

    print("IQR Thresholds for Total_Spend_USD:")
    print(f"- Q1 (25th Percentile)       : ${q1:,.2f}")
    print(f"- Q3 (75th Percentile)       : ${q3:,.2f}")
    print(f"- IQR                         : ${iqr:,.2f}")
    print(
        f"- Upper Bound (Q3+1.5*IQR)  : ${upper_bound:,.2f}"
    )

    print(
        f"\nOutliers Detected      : "
        f"{outliers_detected} records capped to ${upper_bound:,.2f}"
    )


    # ============================================================
    # TASK 5 — ROBUST FEATURE SCALING
    # ============================================================

    continuous_features = [
        "Age",
        "Total_Spend_USD",
        "Purchase_Frequency",
        "App_Sessions_Per_Month"
    ]

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        master_df[continuous_features]
    )

    scaled_df = pd.DataFrame(
        scaled_features,
        columns=continuous_features,
        index=master_df.index
    )

    processed_features = pd.concat(
        [
            master_df[
                [
                    "Customer_ID",
                    "Account_Tier_Encoded",
                    "Region_North",
                    "Region_South",
                    "Region_West",
                    "Is_High_Value"
                ]
            ],
            scaled_df
        ],
        axis=1
    )

    scaled_means = scaled_df.mean()
    scaled_stds = scaled_df.std(ddof=0)


    print("\n========== TASK 5 — FEATURE SCALING ==========")

    print("Standard Scaler Metrics:")

    for feature in continuous_features[:3]:
        print(
            f"- Scaled {feature:<22}: "
            f"Mean = {scaled_means[feature]:.2f}, "
            f"Std = {scaled_stds[feature]:.2f}"
        )


    # ============================================================
    # FINAL EXPECTED OUTPUT
    # ============================================================

    initial_columns = df_profile.shape[1] + (
        df_tx.shape[1] - 1
    ) + (
        df_engagement.shape[1] - 1
    )

    processed_output_features = (
        len(continuous_features)
        + 1
        + 3
        + 1
    )

    print("\n")
    print("========== E-COMMERCE DATA PREPARATION & ENCODING PIPELINE ==========")

    print("\nMaster Dataset Records     :", len(master_df))
    print("Initial Columns            :", initial_columns)
    print("Processed Output Features  :", processed_output_features)

    print("\nMissing Value Resolution:")
    print(
        "- Age Imputations          :",
        age_missing_before,
        "records restored via Account_Tier median"
    )
    print(
        "- Spend Imputations        :",
        spend_missing_before,
        "record restored via Account_Tier median"
    )

    print("\nFeature Encoding Summary:")
    print(
        "- Ordinal Encoding         : "
        "Account_Tier mapped to integer scale [1 to 4]"
    )
    print(
        "- One-Hot Encoding         : "
        "Region mapped into binary dummy columns [North, South, West]"
    )

    print("\nOutlier Handling & Feature Scaling:")
    print(
        f"- Capped Total_Spend_USD   : "
        f"{outliers_detected} upper-bound outliers "
        f"truncated at ${upper_bound:,.2f}"
    )
    print(
        "- Standardization          : "
        "All continuous features scaled to Zero Mean and Unit Variance"
    )

    print(
        "\nPipeline Outcome: "
        "Clean, fully transformed feature matrix X prepared "
        "for supervised model training."
    )
run_pipeline()    