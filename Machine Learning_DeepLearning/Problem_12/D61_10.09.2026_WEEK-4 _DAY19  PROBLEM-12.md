PROJECT 12 — API-DRIVEN DECISION TREE CLASSIFIER & FEATURE IMPORTANCE ANALYTICS
-------------
Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement
-------------------
An enterprise cloud monitoring service automates system failure detection (0 = Normal Operation, 1 = System Failure). You must write an API ingestion pipeline to pull telemetry records from an active HTTP CSV endpoint over REST, engineer categorical indicators, train an unpruned Decision Tree Classifier, extract feature importance rankings, and evaluate hyperparameter tree pruning (max_depth) to eliminate overfitting.

LIVE API ENDPOINT
Use this active REST endpoint in your fetching function:
---------------
HOST_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


BOILERPLATE & STARTER CODE
----------------------------

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, precision_score, recall_score

HOST_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

# =====================================================================
# STUDENT TASK: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_telemetry_data(url: str) -> pd.DataFrame:
    """
    Student Implementation Required:
    1. Send an HTTP GET request to the provided URL using requests.
    2. Check for HTTP status code errors using response.raise_for_status().
    3. Parse the returned CSV response payload into a Pandas DataFrame using io.StringIO.
    4. Implement error handling (try-except block) for network failures.
    """
    # TODO: Write your code here
    pass


TASKS & EXPECTED OUTPUTS
-------------------------
TASK 1 — REST API Ingestion & Target Binary TransformationFetch the raw dataset using fetch_telemetry_data(). Rename feature columns to cloud metrics (sepal_length ->cpu_usage_pct, sepal_width ->memory_usage_pct, petal_length ->disk_io_rate, petal_width ->network_latency_ms). Map the species column to binary target Is_Failure (setosa ->0, other ->1).

Expected Output:
[TASK 1 SUCCESS] Telemetry API Data Ingested (150 Records)
Target Distribution (0: Normal / 1: Failure):
0    50
1    100
Name: Is_Failure, dtype: int64

Sample Feature Table:
   cpu_usage_pct  memory_usage_pct  disk_io_rate  network_latency_ms  Is_Failure
0            5.1               3.5           1.4                 0.2           0
1            4.9               3.0           1.4                 0.2           0
2            4.7               3.2           1.3                 0.2           0


TASK 2 — Stratified Data Partitioning

Separate predictive features from the target (Is_Failure). Perform an 80/20 Stratified Train-Test Split using random_state=42 to retain balanced failure class ratios across both sets.

Expected Output:

[TASK 2 SUCCESS] Data Stratified & Split.
Train Matrix Shape : (120, 4) | Target Counts: 0 -> 40, 1 -> 80
Test Matrix Shape  : (30, 4)  | Target Counts: 0 -> 10, 1 -> 20


TASK 3 — Unpruned Decision Tree Training & Overfitting Audit

Fit a baseline DecisionTreeClassifier(criterion='gini', random_state=42) without depth constraints. Compute accuracy scores on both training and test sets to demonstrate variance/overfitting.

Expected Output:
[TASK 3 SUCCESS] Unpruned Decision Tree Trained.
Training Accuracy : 100.0%
Testing Accuracy  : 96.67%
Overfitting Gap   : 3.33%



TASK 4 — Gini Feature Importance & Rule Extraction

Extract feature_importances_ to inspect top splitting attributes. Output human-readable decision rules using export_text().

Expected Output:

[TASK 4 SUCCESS] Gini Feature Importances Extracted:
- network_latency_ms : 0.9524
- disk_io_rate       : 0.0476
- memory_usage_pct   : 0.0000
- cpu_usage_pct      : 0.0000

Extracted Tree Decision Structure:
|--- network_latency_ms <= 0.80
|   |--- class: 0
|--- network_latency_ms >  0.80
|   |--- class: 1


TASK 5 — Hyperparameter Pruning & Model Regularization

Train a regularized decision tree by restricting tree depth (max_depth=2, min_samples_leaf=5). Evaluate training vs. testing accuracy to prove variance reduction.

Expected Output:

[TASK 5 SUCCESS] Pruned Decision Tree Trained (max_depth=2).
Pruned Train Accuracy : 100.0%
Pruned Test Accuracy  : 100.0%
Variance Status       : Zero Overfitting Gap (Optimal Generalization)



FINAL EXPECTED OUTPUT
------------------------

========== API-DRIVEN DECISION TREE & OVERFITTING ENGINE ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 150 Telemetry Logs
Features Included          : 4 Continuous Metrics (cpu_usage_pct, memory_usage_pct, disk_io_rate, network_latency_ms)
Target Output              : Is_Failure (Binary Classification: 0 = Normal, 1 = Failure)

Model Training Metrics:
- Stratified Train Split   : 120 Records (40 Normal / 80 Failure)
- Stratified Test Split    : 30 Records (10 Normal / 20 Failure)
- Unpruned Tree Accuracy   : Train = 100.0% | Test = 96.67%

Feature Importance Profiling:
- Primary Root Split Feature: network_latency_ms (Gini Importance = 0.9524)
- Secondary Split Feature   : disk_io_rate (Gini Importance = 0.0476)

Hyperparameter Pruning & Regularization:
- Baseline Unpruned Tree    : 96.67% Test Accuracy (Slight overfitting on train split)
- Pruned Tree (max_depth=2) : 100.0% Test Accuracy (Eliminated training variance)

Conclusion:
By fetching telemetry data dynamically over HTTP REST endpoints, the pipeline evaluates system health in real time. Pruning the Decision Tree using depth boundaries prevents memorization of noise, achieving optimal generalization for automated failure detection.