PROJECT 15 — GRADIENT BOOSTING & EARLY STOPPING OPTIMIZATION

Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
-------------------
A cloud infrastructure platform monitors server health to predict network outages (0 = Stable, 1 = Outage Risk). You must write a REST API fetching function to stream continuous metric logs over HTTP, fit a GradientBoostingClassifier, and implement early stopping parameters (validation_fraction, n_iter_no_change, tol) to automatically truncate tree boosting before over-fitting occurs.

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
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"

# =====================================================================
# STUDENT TASK: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_network_logs(url: str) -> pd.DataFrame:
    """
    Student Implementation Required:
    1. Send GET request using requests.get().
    2. Check response status using response.raise_for_status().
    3. Read CSV content into a Pandas DataFrame using io.StringIO.
    """
    # TODO: Implement API fetch logic
    pass


TASKS & EXPECTED OUTPUTS
----------------------------
TASK 1 — Telemetry REST API Ingestion & Target Setup

Fetch raw logs via fetch_network_logs(). Clean missing values (dropna()). Map target species to binary indicator Outage_Risk (1 if species == 'Gentoo', else 0). Scale numeric features using StandardScaler.

Expected Output:
--------------------
[TASK 1 SUCCESS] Network Log API Ingested (333 Clean Records)
Class Ratios (0: Stable / 1: Outage Risk):
0    214
1    119
Name: Outage_Risk, dtype: int64


TASK 2 — Train-Test Split Strategy

Split dataset 70/30 into Training and Testing sets with stratification (random_state=42).

Expected Output:
--------------------
[TASK 2 SUCCESS] Stratified Split Execution:
Train Records: 233 | Test Records: 100


TASK 3 — Early Stopping Gradient Boosting Implementation

Fit a GradientBoostingClassifier with:
- n_estimators=500
- learning_rate=0.05
- validation_fraction=0.15
- n_iter_no_change=10
- tol=1e-4
- random_state=42

Output the actual number of trees built before early stopping was triggered.

Expected Output:
--------------------
[TASK 3 SUCCESS] Early Stopping Gradient Boosting Trained:
Configured Max Trees   : 500
Actual Trees Fitted    : 62 (Early Stopping Triggered)
Validation Loss Stopped : 0.0412


TASK 4 — Model Accuracy & Loss Evaluation

Evaluate the early-stopped model on X_test_scaled. Compute Accuracy, Log Loss, and ROC-AUC Score.

Expected Output:
--------------------
[TASK 4 SUCCESS] Evaluation Metrics:
Test Accuracy : 99.00%
Test Log Loss : 0.0421
Test ROC-AUC  : 0.9992


FINAL EXPECTED OUTPUT
--------------------
========== GRADIENT BOOSTING & EARLY STOPPING OPTIMIZATION ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 333 Telemetry Records
Model Architecture         : GradientBoostingClassifier (Early Stopping Enabled)

Early Stopping Audit:
- Maximum Tree Boundary    : 500 Trees
- Optimal Stopped Trees    : 62 Trees
- Compute Savings          : 87.6% reduction in redundant boosting iterations

Performance Metrics:
- Test Accuracy            : 99.00%
- Test Log Loss            : 0.0421
- Test ROC-AUC             : 0.9992

Conclusion:
Monitoring out-of-fold validation loss during gradient boosting prevents over-parameterization, stopping training as soon as test generalization peaks.