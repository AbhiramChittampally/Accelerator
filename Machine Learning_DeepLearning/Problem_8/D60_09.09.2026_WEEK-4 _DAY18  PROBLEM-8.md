WEEK 4 — DAY 18
---------------------------------
PROBLEM 1 — END-TO-END DATA PREPARATION & ENCODING PIPELINE

Platform: Google Colab

Language: Python

Libraries: Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
---------------------
An e-commerce platform processes raw customer data across multiple relational systems to predict high-value customer retention. Before feeding data into machine learning models, you must join 3 raw datasets, handle missing values using group-wise imputations, detect and trim numerical outliers, scale skewed continuous features, and apply appropriate encoding (One-Hot vs. Ordinal) across 50 records.

Input Files & Data Setup
------------------------
import pandas as pd
import numpy as np

# File 1: Customer Profile Logs (50 Records)
cust_profile_data = {
    'Customer_ID': [f'CUST_{200+i}' for i in range(50)],
    'Account_Tier': ['Silver', 'Gold', 'Bronze', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver',
                     'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold',
                     'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze',
                     'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver', 'Platinum', 'Bronze', 'Gold', 'Silver',
                     'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze', 'Gold', 'Platinum', 'Silver', 'Bronze', 'Gold'],
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

# File 2: Transaction History Metrics (50 Records)
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

# File 3: Engagement Logs (50 Records)
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


TASKS TO IMPLEMENT
------------------
TASK 1 — Multi-Source Relational Data Join
Perform sequential inner joins on df_profile, df_tx, and df_engagement using Primary Key Customer_ID across all 50 records.

Expected Output:
  Customer_ID Account_Tier   Age Region  Total_Spend_USD  Purchase_Frequency  App_Sessions_Per_Month  Is_High_Value
0    CUST_200       Silver  34.0  North           1200.5                  12                      15              0
1    CUST_201         Gold  45.0  South           4500.0                  35                      42              1
2    CUST_202       Bronze   NaN   West            300.2                   2                       4              0
3    CUST_203     Platinum  29.0   East          12500.0                  85                      95              1
4    CUST_204         Gold  52.0  North           3800.0                  28                      33              1


TASK 2 — Missing Value Analysis & Tier-Grouped Imputation
Compute missing value counts per column. Impute missing Age values using median Age grouped by Account_Tier. Impute missing Total_Spend_USD using median spend grouped by Account_Tier.

Expected Output:
Missing Values Before Imputation:
- Age             : 5 missing values
- Total_Spend_USD : 1 missing value

Imputed Metrics by Account_Tier (Age / Spend Medians):
- Bronze   : Median Age = 25.5 | Median Spend = $230.00
- Gold     : Median Age = 48.0 | Median Spend = $4,750.00
- Platinum : Median Age = 36.5 | Median Spend = $12,650.00
- Silver   : Median Age = 33.5 | Median Spend = $1,030.00

Missing Values After Imputation: 0


TASK 3 — Categorical Variable Encoding (One-Hot vs Ordinal)
Encode ordinal features (Account_Tier: Bronze=1, Silver=2, Gold=3, Platinum=4) using Ordinal Encoding. Apply One-Hot Encoding to nominal feature (Region) dropping first column to prevent multi-collinearity.

Expected Output:
Encoded Columns:
- Account_Tier_Encoded : Discrete Values [1, 2, 3, 4]
- One-Hot Region Columns: Region_North, Region_South, Region_West (Region_East dropped as baseline)


TASK 4 — Outlier Detection & IQR Capping
Identify numerical outliers in Total_Spend_USD using 1.5 * IQR bounds. Cap outliers above the upper bound.

Expected Output:
IQR Thresholds for Total_Spend_USD:
- Q1 (25th Percentile) : $860.00
- Q3 (75th Percentile) : $5,525.00
- IQR                  : $4,665.00
- Upper Bound (Q3+1.5*IQR) : $12,522.50

Outliers Detected      : 4 records capped to $12,522.50


TASK 5 — Robust Feature Scaling
Apply StandardScaler to continuous features (Age, Total_Spend_USD, Purchase_Frequency, App_Sessions_Per_Month). Verify output transformed means (~0.0) and standard deviations (~1.0).

Expected Output:
Standard Scaler Metrics:
- Scaled Age                : Mean = 0.00, Std = 1.00
- Scaled Total_Spend_USD    : Mean = 0.00, Std = 1.00
- Scaled Purchase_Frequency : Mean = 0.00, Std = 1.00


FINAL EXPECTED OUTPUT
-----------------------
========== E-COMMERCE DATA PREPARATION & ENCODING PIPELINE ==========

Master Dataset Records     : 50
Initial Columns            : 8
Processed Output Features  : 9

Missing Value Resolution:
- Age Imputations          : 5 records restored via Account_Tier median
- Spend Imputations        : 1 record restored via Account_Tier median

Feature Encoding Summary:
- Ordinal Encoding         : Account_Tier mapped to integer scale [1 to 4]
- One-Hot Encoding         : Region mapped into binary dummy columns [North, South, West]

Outlier Handling & Feature Scaling:
- Capped Total_Spend_USD   : 4 upper-bound outliers truncated at $12,522.50
- Standardization          : All continuous features scaled to Zero Mean and Unit Variance

Pipeline Outcome: Clean, fully transformed feature matrix X prepared for supervised model training.