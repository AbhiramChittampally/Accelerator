PROBLEM 3 — CROSS-VALIDATION & OVERFITTING DIAGNOSTICS PIPELINE
---------------------------------------------------------------
Platform: Google Colab

Language: Python

Libraries: Pandas, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement
An insurance risk assessment team evaluates machine learning models to predict policy claim likelihood. Relying on a single train-test split produces noisy performance estimates. You must integrate 3 relational sources (Policyholder Info, Vehicle Records, Claim History) covering 50 records, implement K-Fold and Stratified K-Fold Cross-Validation, and evaluate model variance across evaluation folds.

Input Files & Data Setup
--------------------------
import pandas as pd
import numpy as np

# File 1: Policyholder Information (50 Records)
policyholder_data = {
    'Policy_ID': [f'POL_{700+i}' for i in range(50)],
    'Driver_Age': [22, 45, 34, 60, 28, 50, 19, 41, 33, 55,
                   24, 48, 31, 62, 26, 52, 20, 43, 36, 58,
                   23, 46, 32, 61, 27, 51, 21, 42, 35, 56,
                   25, 49, 30, 63, 29, 53, 22, 44, 37, 59,
                   24, 47, 33, 64, 28, 54, 20, 40, 38, 57],
    'Credit_Score': [610, 750, 680, 810, 640, 780, 580, 720, 690, 790,
                     620, 760, 670, 820, 630, 770, 590, 730, 700, 800,
                     615, 755, 675, 815, 635, 775, 585, 725, 695, 795,
                     625, 765, 665, 825, 645, 785, 600, 735, 705, 805,
                     618, 758, 678, 818, 638, 778, 592, 722, 698, 788]
}

# File 2: Vehicle Risk Records (50 Records)
vehicle_data = {
    'Policy_ID': [f'POL_{700+i}' for i in range(50)],
    'Vehicle_Age_Yrs': [12, 3, 7, 1, 9, 2, 14, 4, 6, 2,
                        11, 2, 8, 1, 10, 3, 13, 5, 6, 1,
                        12, 3, 7, 1, 9, 2, 14, 4, 5, 2,
                        10, 2, 8, 1, 9, 3, 13, 4, 6, 1,
                        11, 3, 7, 1, 10, 2, 14, 5, 6, 2],
    'Annual_Mileage_KM': [22000, 11000, 15000, 8000, 18000, 9500, 25000, 12000, 14000, 9000,
                          21000, 10500, 16000, 7500, 19000, 9800, 24000, 12500, 14500, 8500,
                          22500, 11200, 15200, 8200, 18200, 9600, 25500, 12200, 13800, 9100,
                          20500, 10800, 16200, 7800, 18800, 10000, 24500, 12800, 14200, 8800,
                          21800, 11100, 15800, 8100, 18500, 9700, 25200, 12100, 14100, 9200]
}

# File 3: Claim History Target (50 Records)
claim_data = {
    'Policy_ID': [f'POL_{700+i}' for i in range(50)],
    'Made_Claim': [1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                   1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                   1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                   1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                   1, 0, 0, 0, 1, 0, 1, 0, 0, 0] # 15 Claims (30%), 35 No Claims (70%)
}

df_policy = pd.DataFrame(policyholder_data)
df_vehicle = pd.DataFrame(vehicle_data)
df_claim = pd.DataFrame(claim_data)

TASKS TO IMPLEMENT
-------------------
TASK 1 — Relational Insurance Data Merging
Perform inner joins on df_policy, df_vehicle, and df_claim using Primary Key Policy_ID across all 50 records.

Expected Output:
  Policy_ID  Driver_Age  Credit_Score  Vehicle_Age_Yrs  Annual_Mileage_KM  Made_Claim
0   POL_700          22           610               12              22000           1
1   POL_701          45           750                3              11000           0
2   POL_702          34           680                7              15000           0
3   POL_703          60           810                1               8000           0
4   POL_704          28           640                9              18000           1


TASK 2 — Standard 5-Fold Cross-Validation Setup
Configure KFold(n_splits=5, shuffle=True, random_state=42). Iterate through folds and output train/validation record counts alongside fold-wise target distributions.

Expected Output:
K-Fold Splitting Summary (5 Folds):
- Fold 1 Validation : 10 Records | Target Claims: 4 (40.0%)
- Fold 2 Validation : 10 Records | Target Claims: 2 (20.0%)
- Fold 3 Validation : 10 Records | Target Claims: 3 (30.0%)
- Fold 4 Validation : 10 Records | Target Claims: 1 (10.0%)
- Fold 5 Validation : 10 Records | Target Claims: 5 (50.0%)
Target Variance     : Claim ratio varies significantly across folds (10.0% to 50.0%).


TASK 3 — Stratified 5-Fold Cross-Validation Execution
Configure StratifiedKFold(n_splits=5, shuffle=True, random_state=42). Iterate through folds and output train/validation target distributions.

Expected Output:
Stratified K-Fold Splitting Summary (5 Folds):
- Fold 1 Validation : 10 Records | Target Claims: 3 (30.0%)
- Fold 2 Validation : 10 Records | Target Claims: 3 (30.0%)
- Fold 3 Validation : 10 Records | Target Claims: 3 (30.0%)
- Fold 4 Validation : 10 Records | Target Claims: 3 (30.0%)
- Fold 5 Validation : 10 Records | Target Claims: 3 (30.0%)
Target Variance     : Claim ratio is identical across all validation folds (30.0%).


TASK 4 — Baseline Model Cross-Validation Metric Evaluation
Train a LogisticRegression baseline using Stratified 5-Fold CV. Calculate Accuracy scores per fold, mean accuracy, and standard deviation.

Expected Output:
Logistic Regression 5-Fold Accuracy Scores:
- Fold 1 : 100.0%
- Fold 2 : 100.0%
- Fold 3 : 100.0%
- Fold 4 : 100.0%
- Fold 5 : 100.0%
Mean Validation Accuracy : 100.0% (+/- 0.0%)


TASK 5 — Overfitting & Underfitting Conceptual Analysis
Contrast training error vs. validation error behaviors under Overfitting, Underfitting, and Optimal Generalization scenarios.

Expected Output:
DIAGNOSTIC MATRIX:
1. Underfitting  : High Training Error, High Validation Error (Model is too simple).
2. Overfitting   : Very Low Training Error, High Validation Error (Model memorizes noise).
3. Optimal Model : Low Training Error, Low Validation Error (Model generalizes well).


FINAL EXPECTED OUTPUT
------------------------
========== CROSS-VALIDATION & OVERFITTING DIAGNOSTICS ==========

Master Insurance Dataset Records : 50
Features (X)                     : Driver_Age, Credit_Score, Vehicle_Age_Yrs, Annual_Mileage_KM
Target (y)                       : Made_Claim (30.0% Positive Rate)

Cross-Validation Comparison:
- Standard K-Fold (5 Splits)     : High fold variance (Validation positive rate: 10% - 50%)
- Stratified K-Fold (5 Splits)   : Zero fold variance (Validation positive rate fixed at 30%)

Baseline Evaluation Results:
- Mean CV Accuracy Score          : 100.0% (+/- 0.0%)

Conclusion:
Stratified K-Fold Cross-Validation ensures robust, low-variance evaluation on imbalanced risk data by maintaining consistent label distributions across all cross-validation folds.