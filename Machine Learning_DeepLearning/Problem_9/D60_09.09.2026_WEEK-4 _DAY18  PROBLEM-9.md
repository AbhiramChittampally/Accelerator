PROBLEM 2 — TRAIN-TEST SPLITTING & STRATIFIED SAMPLING AUDIT
-----------------------------------------------------------
Platform: Google Colab

Language: Python

Libraries: Pandas, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
-----------------
A medical diagnostics team is constructing an automated screening model for a rare health condition. Because the target label is heavily imbalanced, standard random splits risk leaving the test set with zero positive cases. You must integrate 3 relational datasets (Patient Metadata, Clinical Vitals, Diagnostic Tests) covering 50 records, execute both standard random splitting and stratified splitting, and quantify target distribution drift across training and test folds.

Input Files & Data Setup
--------------------------
import pandas as pd
import numpy as np

# File 1: Patient Demographics (50 Records)
demographics_data = {
    'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
    'Age': [45, 62, 29, 71, 55, 38, 67, 42, 59, 31,
            48, 65, 26, 73, 52, 35, 69, 41, 58, 33,
            50, 61, 28, 70, 54, 39, 66, 44, 60, 30,
            47, 64, 27, 72, 53, 36, 68, 43, 57, 32,
            49, 63, 25, 74, 51, 37, 70, 40, 56, 34],
    'Gender': ['F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
               'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
               'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
               'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
               'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M']
}

# File 2: Clinical Vitals (50 Records)
vitals_data = {
    'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
    'BMI': [24.5, 31.2, 21.0, 34.8, 28.1, 23.4, 32.5, 26.0, 29.8, 22.1,
            25.3, 30.8, 20.5, 35.2, 27.9, 23.0, 33.1, 25.8, 29.1, 21.8,
            26.1, 31.5, 20.8, 34.2, 28.5, 23.9, 32.0, 26.4, 29.5, 22.5,
            25.0, 31.0, 20.2, 35.6, 27.5, 23.2, 33.5, 25.5, 28.8, 22.0,
            25.8, 31.8, 20.0, 36.0, 28.2, 23.6, 32.8, 26.2, 29.0, 22.3],
    'Blood_Pressure_Systolic': [120, 145, 115, 160, 132, 122, 150, 128, 138, 118,
                                122, 142, 112, 162, 130, 120, 152, 126, 136, 116,
                                124, 144, 114, 158, 134, 121, 148, 127, 137, 117,
                                121, 141, 111, 165, 129, 119, 154, 125, 135, 115,
                                123, 143, 110, 164, 131, 122, 151, 126, 134, 116]
}

# File 3: Diagnostic Tests (50 Records - Imbalanced Target)
diagnostics_data = {
    'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
    'Biomarker_Level': [1.2, 8.5, 0.8, 9.1, 2.1, 1.0, 7.8, 1.5, 3.2, 0.9,
                        1.4, 7.9, 0.7, 9.5, 2.3, 1.1, 8.2, 1.6, 3.0, 0.8,
                        1.3, 8.1, 0.6, 9.0, 2.0, 1.2, 7.5, 1.4, 3.1, 0.9,
                        1.1, 8.3, 0.5, 9.8, 2.2, 1.0, 8.0, 1.5, 2.9, 0.7,
                        1.3, 8.4, 0.4, 9.6, 2.4, 1.1, 7.7, 1.6, 2.8, 0.8],
    'Has_Condition': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                      0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                      0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                      0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                      0, 1, 0, 1, 0, 0, 1, 0, 0, 0] # 15 Positive (30%), 35 Negative (70%)
}

df_demo = pd.DataFrame(demographics_data)
df_vitals = pd.DataFrame(vitals_data)
df_diag = pd.DataFrame(diagnostics_data)


TASKS TO IMPLEMENT
-------------------
TASK 1 — Multi-Table Diagnostic Integration
Merge df_demo, df_vitals, and df_diag into a single master medical dataset using Primary Key Patient_ID.

Expected Output:
  Patient_ID  Age Gender   BMI  Blood_Pressure_Systolic  Biomarker_Level  Has_Condition
0    PAT_500   45      F  24.5                      120              1.2              0
1    PAT_501   62      M  31.2                      145              8.5              1
2    PAT_502   29      F  21.0                      115              0.8              0
3    PAT_503   71      M  34.8                      160              9.1              1
4    PAT_504   55      F  28.1                      132              2.1              0


TASK 2 — Target Imbalance Assessment
Calculate absolute counts and percentage distribution of Has_Condition across the dataset.

Expected Output:
Class Distribution (Has_Condition):
- Negative (0) : 35 patients (70.0%)
- Positive (1) : 15 patients (30.0%)


TASK 3 — Non-Stratified Random Train-Test Split
Perform an 80/20 train-test split without stratification (random_state=42). Compute target distributions in train and test sets.

Expected Output:
Non-Stratified Split (80/20):
- Training Set Size : 40 records
  - Negative (0)    : 27 (67.5%)
  - Positive (1)    : 13 (32.5%)
- Testing Set Size  : 10 records
  - Negative (0)    : 8 (80.0%)
  - Positive (1)    : 2 (20.0%)
Drift Analysis      : Positive class proportion shifted from 30.0% in full dataset to 20.0% in test set.


TASK 4 — Stratified Train-Test Split
Perform an 80/20 train-test split using Stratified Sampling (stratify=y, random_state=42). Compute target distributions in train and test sets.

Expected Output:
Stratified Split (80/20):
- Training Set Size : 40 records
  - Negative (0)    : 28 (70.0%)
  - Positive (1)    : 12 (30.0%)
- Testing Set Size  : 10 records
  - Negative (0)    : 7 (70.0%)
  - Positive (1)    : 3 (30.0%)
Drift Analysis      : Class ratios perfectly preserved across both splits (70% / 30%).


TASK 5 — Feature Isolation & Train/Test Shape Auditing
Extract final Feature Matrices (X_train, X_test) and Target Vectors (y_train, y_test). Exclude identifier Patient_ID. Confirm shapes.

Expected Output:
Final Matrix Dimensions:
- X_train Shape : (40, 5)
- X_test Shape  : (10, 5)
- y_train Shape : (40,)
- y_test Shape  : (10,)



FINAL EXPECTED OUTPUT
-----------------------

========== TRAIN-TEST SPLITTING & STRATIFIED SAMPLING AUDIT ==========

Master Diagnostic Dataset Records : 50
Target Label Class Ratio          : 70.0% Negative (0) | 30.0% Positive (1)

Sampling Methodology Comparison:
- Standard Random Split (80/20)   : Test set shifted to 80.0% Negative / 20.0% Positive (Distribution Drift)
- Stratified Random Split (80/20) : Test set perfectly maintained 70.0% Negative / 30.0% Positive ratio

Final Prepared Matrices:
- Training Features (X_train)     : 40 Rows, 5 Numerical/Categorical Features
- Testing Features (X_test)       : 10 Rows, 5 Numerical/Categorical Features

Conclusion:
For imbalanced datasets, Stratified Sampling is mandatory to eliminate class distribution drift between training and evaluation phases.