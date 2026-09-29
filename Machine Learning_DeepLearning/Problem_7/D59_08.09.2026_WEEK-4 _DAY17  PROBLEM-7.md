PROBLEM 3 — CUSTOMER BEHAVIOR CLUSTERING (UNSUPERVISED LEARNING)
---------------
Platform: Google Colab

Language: Python

Libraries: Pandas, NumPy

Submission: Google Colab Notebook

Problem Statement
A digital media platform wants to discover natural audience segments without using manual rule tags or pre-existing labels. You are provided with 3 relational tables: User Activity Logs, Subscription Billing Metadata, and Device & Platform Logs. You must join these datasets across 50 user records, perform feature scale inspection, create heuristic baseline clusters, and evaluate unsupervised clustering frameworks.


Input Files & Data Setup
-------------------------
import pandas as pd
import numpy as np

# File 1: User Activity Logs (50 Records)
activity_data = {
    'User_ID': [f'USR_{100+i}' for i in range(50)],
    'Device_ID': [f'DEV_{(i%10)+1}' for i in range(50)],
    'Daily_Listening_Mins': [180, 25, 210, 40, 190, 30, 220, 35, 175, 20, 195, 28, 205, 45, 185, 22, 215, 38, 170, 24, 200, 32, 225, 42, 180, 26, 210, 36, 190, 21, 198, 29, 208, 48, 178, 23, 218, 39, 172, 27, 202, 33, 222, 41, 182, 25, 212, 37, 188, 22],
    'Playlists_Created': [25, 2, 30, 3, 22, 1, 35, 4, 20, 1, 26, 2, 28, 4, 21, 1, 32, 3, 19, 1, 27, 2, 34, 4, 23, 2, 29, 3, 24, 1, 26, 2, 31, 5, 20, 1, 33, 3, 18, 2, 28, 3, 36, 4, 22, 1, 30, 3, 25, 1],
    'Skip_Ratio': [0.12, 0.65, 0.08, 0.58, 0.15, 0.70, 0.05, 0.60, 0.10, 0.75, 0.11, 0.62, 0.09, 0.55, 0.14, 0.68, 0.06, 0.59, 0.13, 0.72, 0.10, 0.64, 0.04, 0.56, 0.12, 0.66, 0.08, 0.57, 0.15, 0.74, 0.09, 0.61, 0.07, 0.54, 0.11, 0.69, 0.05, 0.58, 0.12, 0.63, 0.10, 0.65, 0.04, 0.55, 0.13, 0.67, 0.07, 0.58, 0.14, 0.71],
    'Podcast_Listening_Pct': [0.45, 0.05, 0.50, 0.10, 0.40, 0.02, 0.55, 0.08, 0.38, 0.01, 0.46, 0.04, 0.48, 0.12, 0.41, 0.03, 0.52, 0.09, 0.39, 0.02, 0.47, 0.06, 0.54, 0.11, 0.42, 0.05, 0.49, 0.08, 0.40, 0.01, 0.45, 0.04, 0.51, 0.13, 0.37, 0.02, 0.53, 0.09, 0.38, 0.05, 0.46, 0.07, 0.56, 0.10, 0.43, 0.03, 0.50, 0.08, 0.41, 0.02]
}

# File 2: Subscription Metadata (50 Records)
sub_data = {
    'User_ID': [f'USR_{100+i}' for i in range(50)],
    'Account_Age_Months': [24, 2, 36, 4, 18, 1, 48, 5, 12, 1, 28, 3, 32, 6, 16, 2, 42, 4, 14, 1, 30, 3, 44, 5, 20, 2, 34, 4, 22, 1, 26, 3, 38, 7, 15, 2, 46, 4, 13, 2, 29, 3, 50, 6, 17, 1, 35, 4, 21, 1],
    'Monthly_Fee_USD': [14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 14.99, 0.00, 9.99, 0.00, 14.99, 0.00, 14.99, 0.00]
}

# File 3: Device & Platform Logs (10 Records)
device_data = {
    'Device_ID': [f'DEV_{i}' for i in range(1, 11)],
    'Primary_OS': ['iOS', 'Android', 'iOS', 'Android', 'WebOS', 'iOS', 'Android', 'iOS', 'Android', 'Windows'],
    'App_Version_Code': [4.5, 4.1, 4.5, 4.2, 3.9, 4.5, 4.1, 4.5, 4.2, 4.0]
}

df_activity = pd.DataFrame(activity_data)
df_sub = pd.DataFrame(sub_data)
df_device = pd.DataFrame(device_data)


TASKS TO IMPLEMENT
--------------------
TASK 1 — Multi-Table Unsupervised Dataset Merging
Merge df_activity, df_sub, and df_device using relational keys (User_ID, Device_ID).

Expected Output:
  User_ID Device_ID  Daily_Listening_Mins  ...  Account_Age_Months  Monthly_Fee_USD Primary_OS
0  USR_100     DEV_1                   180  ...                  24            14.99        iOS
1  USR_101     DEV_2                    25  ...                   2             0.00    Android
2  USR_102     DEV_3                   210  ...                  36            14.99        iOS
3  USR_103     DEV_4                    40  ...                   4             0.00    Android
4  USR_104     DEV_5                   190  ...                  18            14.99      WebOS


TASK 2 — Paradigm & Label Absence Verification
Verify shape, column types, and explicitly demonstrate the ABSENCE of a target label (y).

Expected Output:
Total Combined Records : 50
Total Combined Columns : 10
Target Vector (y)      : ABSENT (Unsupervised Setup)
Paradigm               : Unsupervised Learning / Clustering


TASK 3 — Feature Space Scale & Variance Inspection
Extract numeric feature set X and inspect feature ranges to justify feature scaling.

Expected Output:
Numeric Features (X) Range Analysis:
- Daily_Listening_Mins : Min = 20, Max = 225 (Span: 205)
- Playlists_Created    : Min = 1, Max = 36 (Span: 35)
- Skip_Ratio           : Min = 0.04, Max = 0.75 (Span: 0.71)
- Podcast_Listening_Pct: Min = 0.01, Max = 0.56 (Span: 0.55)
- Account_Age_Months   : Min = 1, Max = 50 (Span: 49)

Scale Analysis: Daily_Listening_Mins dominates distance metrics due to magnitude. Feature scaling (StandardScaler/MinMaxScaler) is mandatory.


TASK 4 — Heuristic Baseline Segmentation
Define heuristic baseline segments:
Cluster 0 (Power Listeners): Daily_Listening_Mins > 100 AND Monthly_Fee_USD > 0
Cluster 1 (Casual Listeners): All remaining users

Expected Output:
Heuristic Segment Counts:
Cluster 0 (Power Listeners)  : 25 users (50.0%)
Cluster 1 (Casual Listeners) : 25 users (50.0%)


TASK 5 — Cluster Centroid Profiling
Compute mean metrics for each heuristic cluster across all continuous features.

Expected Output:
Mean Profile by Cluster:
                     Daily_Listening_Mins  Playlists_Created  Skip_Ratio  Podcast_Listening_Pct  Account_Age_Months
Cluster 0 (Power)                  198.80              27.96       0.098                   0.460               31.12
Cluster 1 (Casual)                  29.52               2.08       0.632                   0.046                2.68


TASK 6 — Supervised vs Unsupervised Paradigm Matrix
Print explicit comparison table detailing Supervised vs Unsupervised paradigms.

Expected Output:
========================================================================================
FEATURE                 SUPERVISED LEARNING             UNSUPERVISED LEARNING
========================================================================================
Input Data              Features (X) + Target (y)       Features (X) Only
Primary Goal            Predict Target Outcome          Discover Latent Clusters/Patterns
Evaluation Metric       Accuracy, RMSE, F1-Score        Silhouette Score, Inertia
Common Algorithms       Linear Reg, Decision Trees      K-Means, DBSCAN, Agglomerative
========================================================================================


FINAL EXPECTED OUTPUT
---------------------
========== CUSTOMER BEHAVIOR UNSUPERVISED CLUSTERING ==========

Master Dataset Records     : 50
Total Input Features       : 8
Target Vector Status       : None (Unsupervised Learning)

Feature Variance & Scale Summary:
- Largest Scale Feature    : Daily_Listening_Mins (20 - 225 Mins)
- Smallest Scale Feature   : Skip_Ratio (0.04 - 0.75 Ratio)
- Normalization Requirement: MANDATORY (Distance metrics sensitive to feature magnitude)

Heuristic Segmentation Results:
- Cluster 0 (Power Users)  : 25 Users | Mean Listening = 198.80 mins | Mean Skips = 0.098
- Cluster 1 (Casual Users) : 25 Users | Mean Listening = 29.52 mins  | Mean Skips = 0.632

Conclusion:
In the absence of ground-truth target labels, multi-table clustering isolates distinct user behavior archetypes using spatial distance metrics. Feature scaling ensures balanced feature contributions during geometric clustering.