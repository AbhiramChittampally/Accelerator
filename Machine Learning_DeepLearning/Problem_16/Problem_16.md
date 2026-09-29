PROJECT 16 — HETEROGENEOUS VOTING & STACKING ENSEMBLE ENGINE

Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
-------------------
An automated medical triage system classifies emergency admission severity (0 = Low Urgency, 1 = High Urgency). You must write an API fetching routine to stream continuous diagnostic records over HTTP, build a heterogeneous ensemble combining Logistic Regression, K-Nearest Neighbors, and Decision Trees, and construct both a Soft VotingClassifier and a StackingClassifier with a Logistic Regression meta-learner.

LIVE API ENDPOINTS
Use this active REST endpoint in your fetching function:
-----------------------------

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"


BOILERPLATE & STARTER CODE
-------------------------

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.metrics import accuracy_score, f1_score

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"

# =====================================================================
# STUDENT TASK: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_triage_data(url: str) -> pd.DataFrame:
    """
    Student Implementation Required:
    1. Send GET request using requests.get().
    2. Raise HTTP status exceptions using response.raise_for_status().
    3. Parse CSV string into a Pandas DataFrame using io.StringIO.
    """
    # TODO: Implement API fetch logic
    pass


TASKS & EXPECTED OUTPUTS
----------------------------
TASK 1 — Telemetry API Fetch & Scaling

Fetch dataset via fetch_triage_data(). Clean missing values (dropna()). Create target High_Urgency (1 if species == 'Chinstrap', else 0). Scale continuous features with StandardScaler. Split 75/25 stratified (random_state=42).

Expected Output:
--------------------
[TASK 1 SUCCESS] Triage Data Ingested (333 Records)
Train Set: 249 Records | Test Set: 84 Records
Target Counts (0: Low / 1: High):
0    265
1     68
Name: High_Urgency, dtype: int64


TASK 2 — Base Model Definition & Soft Voting Ensemble

Define three diverse base estimators:
1. lr: LogisticRegression()
2. knn: KNeighborsClassifier(n_neighbors=5)
3. dt: DecisionTreeClassifier(max_depth=4, random_state=42)

Combine them into a VotingClassifier(estimators=..., voting='soft'). Fit on X_train_scaled and evaluate on X_test_scaled.

Expected Output:
--------------------
[TASK 2 SUCCESS] Soft Voting Ensemble Trained:
Base Model 1 (Logistic Regression) Accuracy : 96.43%
Base Model 2 (K-Nearest Neighbors) Accuracy : 95.24%
Base Model 3 (Decision Tree) Accuracy       : 94.05%
Ensemble Soft Voting Test Accuracy          : 97.62%


TASK 3 — Stacking Classifier Construction

Build a StackingClassifier using the same three base estimators and a final_estimator=LogisticRegression() meta-learner. Train and compute test accuracy and F1-score.

Expected Output:
--------------------
[TASK 3 SUCCESS] Stacking Classifier Trained:
Stacking Meta-Learner Test Accuracy : 98.81%
Stacking Meta-Learner Test F1-Score : 0.9714


FINAL EXPECTED OUTPUT
--------------------
========== HETEROGENEOUS VOTING & STACKING ENSEMBLE ENGINE ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 333 Diagnostic Records
Ensemble Diversity         : Linear (Logistic Regression), Distance-Based (k-NN), Tree-Based (Decision Tree)

Architecture Performance Benchmark:
+------------------------------------+---------------+------------+
| Model Architecture                 | Test Accuracy | F1-Score   |
+------------------------------------+---------------+------------+
| Individual Logistic Regression     | 96.43%        | 0.9143     |
| Individual K-Nearest Neighbors     | 95.24%        | 0.8824     |
| Individual Decision Tree           | 94.05%        | 0.8571     |
| Ensemble Soft Voting Classifier    | 97.62%        | 0.9412     |
| Stacking Classifier (Meta-Learner) | 98.81%        | 0.9714     |
+------------------------------------+---------------+------------+

Conclusion:
Stacking heterogeneous algorithms allows a higher-level meta-estimator to learn optimal blend weights across distinct prediction variances, outperforming individual algorithms and simple voting schemes.