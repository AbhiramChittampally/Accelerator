PROJECT 14 — IMBALANCED FRAUD DETECTION VIA CLASS-WEIGHTED RANDOM FORESTS

Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
-------------------
An e-commerce payments platform detects fraudulent activity where instances are heavily imbalanced. You must construct a REST API fetching function to load telemetry data over HTTP, engineer a severe class imbalance (~90% / 10%), train both a standard RandomForestClassifier and a class_weight='balanced' model, and evaluate performance using Precision-Recall metrics and F1-score comparisons.

LIVE API ENDPOINTS
Use this active REST endpoint in your fetching function:
-----------------------------

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


BOILERPLATE & STARTER CODE
-------------------------

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve, auc

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

# =====================================================================
# STUDENT TASK: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_transaction_data(url: str) -> pd.DataFrame:
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
TASK 1 — Live Data Ingestion & Imbalanced Label Creation

Fetch the raw dataset via fetch_transaction_data(). Define target label Is_Fraud (1 if species == 'setosa', else 0). To simulate extreme real-world fraud imbalance, randomly downsample class 1 to produce a ~90/10 ratio.

Expected Output:
--------------------
[TASK 1 SUCCESS] Transaction Data Ingested & Downsampled (110 Records)
Imbalanced Class Distribution:
0    100
1     10
Name: Is_Fraud, dtype: int64


TASK 2 — Stratified Train-Test Partitioning

Partition the dataset into 80% Training and 20% Testing using train_test_split with stratify=y and random_state=42.

Expected Output:
--------------------
[TASK 2 SUCCESS] Data Partitioned with Stratification:
Train Set: 88 Samples (80 Legitimate / 8 Fraud)
Test Set : 22 Samples (20 Legitimate / 2 Fraud)


TASK 3 — Standard vs. Class-Weighted Forest Comparison

Train two Random Forest models (n_estimators=100, random_state=42):
1. Unweighted Baseline: Default settings.
2. Cost-Sensitive Model: class_weight='balanced'.

Compute Precision, Recall, and F1-Score for both models on the test set.

Expected Output:
--------------------
[TASK 3 SUCCESS] Model Comparison Complete:

Unweighted Baseline Model:
- Precision (Fraud) : 0.5000
- Recall (Fraud)    : 0.5000
- F1-Score (Fraud)  : 0.5000

Class-Weighted Model (class_weight='balanced'):
- Precision (Fraud) : 1.0000
- Recall (Fraud)    : 1.0000
- F1-Score (Fraud)  : 1.0000


FINAL EXPECTED OUTPUT
--------------------
========== IMBALANCED FRAUD DETECTION VIA CLASS-WEIGHTED RANDOM FORESTS ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 110 Records (Synthetically Imbalanced 90.9% / 9.1%)
Target Output              : Is_Fraud (0 = Legitimate, 1 = Fraudulent)

Performance Metrics Comparison:
+---------------------+-----------+--------+----------+
| Model Type          | Precision | Recall | F1-Score |
+---------------------+-----------+--------+----------+
| Standard Unweighted | 0.5000    | 0.5000 | 0.5000   |
| Cost-Sensitive      | 1.0000    | 1.0000 | 1.0000   |
+---------------------+-----------+--------+----------+

Conclusion:
Applying cost-sensitive learning (class_weight='balanced') penalizes misclassifications of the rare fraud class, restoring detection recall without requiring synthetic oversampling techniques.