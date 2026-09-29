WEEK 4 — DAY 17 (HARD PROBLEMS)
--------------------------------
PROBLEM 5 — MULTI-CLASS PATIENT TRIAGE CLASSIFICATION
Difficulty: Hard

Platform: Google Colab

Language: Python

Libraries: Pandas, NumPy

Submission: Google Colab Notebook


Problem Statement:
----------------
An emergency hospital system routes incoming patients to three care levels: General, Urgent, or ICU.
You must categorize medical attributes, configure a labeled dataset for multi-class supervised learning,
map supervised algorithms to specific tasks, and analyze class distributions.


Sample Input
----------------
Patient_ID,Heart_Rate_BPM,Systolic_BP,Oxygen_Sat_Pct,Age,Triage_Category
P_501,72,120,98,35,General
P_502,125,165,89,68,ICU
P_503,95,138,94,45,Urgent
P_504,68,115,99,28,General
P_505,140,180,85,75,ICU
P_506,88,130,95,52,Urgent
P_507,75,122,97,40,General
P_508,130,170,88,62,ICU
P_509,92,135,93,50,Urgent
P_510,70,118,98,30,General


TASKS TO IMPLEMENT
-------------------
TASK 1 — Dataset Construction: Load the 10 patient records into a Pandas DataFrame.  

TASK 2 — Supervised Paradigm Identification: Identify whether this is Classification or Regression. State whether the target is discrete or continuous.  

TASK 3 — Input-Output Splitting: Extract feature matrix $X$ and target vector $y$. Exclude non-predictive Patient_ID.  

TASK 4 — Multi-Class Target Distribution: Calculate absolute counts and percentages for General, Urgent, and ICU.  

TASK 5 — Group-Wise Feature Means: Compute mean Heart_Rate_BPM, Systolic_BP, and Oxygen_Sat_Pct for each triage level.  

TASK 6 — Supervised Algorithm Selection Guide: Map candidate algorithms (Logistic Regression, Decision Trees, K-Nearest Neighbors) to this task with justifications. 


EXPECTED OUTPUT
----------------
========== EMERGENCY PATIENT TRIAGE ANALYSIS ==========

Dataset Shape              : 10 Rows, 6 Columns
Supervised Paradigm        : Multi-Class Classification (Discrete Categorical Target)

Features (X)               : Heart_Rate_BPM, Systolic_BP, Oxygen_Sat_Pct, Age
Target (y)                 : Triage_Category

Class Distribution:
- General                  : 4 (40.0%)
- Urgent                   : 3 (30.0%)
- ICU                      : 3 (30.0%)

Triage Level Group Averages:
          Heart_Rate_BPM  Systolic_BP  Oxygen_Sat_Pct
General             71.25       118.25           98.00
Urgent              91.67       134.33           94.00
ICU                131.67       171.67           87.33

Algorithm Guidance: Decision Trees or Multi-Class Logistic Regression are recommended for interpretable clinical rule boundaries.