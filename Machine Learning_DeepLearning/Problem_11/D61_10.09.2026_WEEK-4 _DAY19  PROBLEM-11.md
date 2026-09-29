PROJECT 11 — REAL-TIME NETWORK SECURITY LOGISTIC REGRESSION ENGINE
--------------------
Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement
------------------
An enterprise network security platform automates request classification into Standard (0) or Anomalous (1). You must write a dynamic REST API fetching function to pull live data from GitHub CSV endpoints, merge network traffic logs with host telemetry, train a Logistic Regression classifier, inspect sigmoid probabilities, and evaluate accuracy across custom decision boundaries.


LIVE API ENDPOINTS
-------------------
FLOW_LOGS_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
HOST_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


BOILERPLATE & STARTER CODE
---------------------------
import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

FLOW_LOGS_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
HOST_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

# =====================================================================
# STUDENT TASK 1: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_api_data(url: str) -> pd.DataFrame:
    """
    Student Implementation Required:
    1. Send an HTTP GET request to the provided URL using requests.
    2. Check for HTTP status code errors using response.raise_for_status().
    3. Parse the returned CSV content using io.StringIO and pd.read_csv().
    4. Return the resulting DataFrame.
    """
    # TODO: Write your API fetching code here
    pass



  TASKS & EXPECTED OUTPUTS
  ----------------------------
  TASK 1 — Live API Ingestion & Feature PreprocessingFetch both datasets via fetch_api_data(). Clean penguins.csv by dropping rows with missing values (dropna()). Map target species to binary classification (Adelie -> 0, Other -> 1). Extract continuous features (bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g).

Expected Output:
---------------------

[TASK 1 SUCCESS] API Data Fetched Successfully!
Processed Network Logs Shape: (333, 5)
Class Distribution (0: Normal / 1: Anomalous):
0    146
1    187
Name: Is_Anomalous, dtype: int64

First 3 Rows:
   bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g  Is_Anomalous
0            39.1           18.7              181.0       3750.0             0
1            39.5           17.4              186.0       3800.0             0
2            40.3           18.0              195.0       3250.0             0


TASK 2 — Stratified Train-Test Split & Feature Scaling
Separate predictive features from the target variable (Is_Anomalous). Perform a 70% Train / 30% Test split stratified on the target label using random_state=42. Scale continuous features using StandardScaler.

Expected Output:
[TASK 2 SUCCESS] Data Partitioned & Scaled.
Training Features Shape : (233, 4)
Testing Features Shape  : (100, 4)
Train Target Balance    : 0 -> 102 | 1 -> 131
Test Target Balance     : 0 -> 44  | 1 -> 56



TASK 3 — Logistic Regression Fitting & Coefficient InspectionFit a LogisticRegression(random_state=42) model on X_train_scaled. Extract and display the intercept (beta_0) and feature coefficients (beta_i) paired with feature names.
Expected Output:

[TASK 3 SUCCESS] Logistic Regression Model Trained.
Model Intercept (Beta_0): [0.9324]

Feature Coefficients (Beta_i):
  - bill_length_mm   :  2.8451
  - bill_depth_mm    : -3.1204
  - flipper_length_mm:  1.4012
  - body_mass_g      : -1.0523


TASK 4 — Probability Extraction & Sigmoid Output AuditCompute prediction probabilities
 P(Y=1|X) on X_test_scaled using predict_proba(). Print raw probabilities and assigned risk levels (High Risk if P > 0.50, else Low Risk) for the first 5 test samples.
 
 Expected Output:
 --------------

 [TASK 4 SUCCESS] Probabilities Evaluated for Test Samples:
Sample 1 | P(Anomalous): 0.9982 | Label: 1 | Assigned: High Risk
Sample 2 | P(Anomalous): 0.0015 | Label: 0 | Assigned: Low Risk
Sample 3 | P(Anomalous): 0.9854 | Label: 1 | Assigned: High Risk
Sample 4 | P(Anomalous): 0.0120 | Label: 0 | Assigned: Low Risk
Sample 5 | P(Anomalous): 0.9991 | Label: 1 | Assigned: High Risk


TASK 5 — Custom Decision Boundary Sensitivity AnalysisWrite an evaluation loop testing decision thresholds
T belongsto [0.30, 0.50, 0.70]. Convert probabilities into binary decisions based on each threshold, calculating Accuracy, Precision, and Recall.

Expected Output:

========== DECISION BOUNDARY SENSITIVITY ANALYSIS ==========
Threshold: 0.30 | Accuracy: 97.0% | Precision: 0.9655 | Recall: 0.9821
Threshold: 0.50 | Accuracy: 98.0% | Precision: 0.9821 | Recall: 0.9821
Threshold: 0.70 | Accuracy: 96.0% | Precision: 1.0000 | Recall: 0.9286
============================================================


Final Expected Output
------------------------

========== API-DRIVEN LOGISTIC REGRESSION & DECISION BOUNDARY ENGINE ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 333 (Cleaned & Preprocessed)
Features Included          : 4 Continuous Log Metrics (bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g)
Target Output              : Is_Anomalous (Binary Classification: 0 = Standard, 1 = Anomalous)

Model Training Metrics:
- Stratified Train Split   : 233 Records (102 Normal / 131 Anomalous)
- Stratified Test Split    : 100 Records (44 Normal / 56 Anomalous)
- Base Test Accuracy       : 98.0% (at Default 0.50 Threshold)

Sigmoid Probability Profiling:
- Maximum Anomalous Prob   : 99.91%
- Minimum Anomalous Prob   : 0.15%
- Key Probability Drivers  : bill_length_mm (+2.8451), bill_depth_mm (-3.1204)

Decision Threshold Tuning:
- Threshold @ 0.30 (Strict): 97.0% Accuracy | Precision: 0.9655 | Recall: 0.9821 (Maximizes detection for suspicious traffic)
- Threshold @ 0.50 (Normal): 98.0% Accuracy | Precision: 0.9821 | Recall: 0.9821 (Balanced baseline model performance)
- Threshold @ 0.70 (Alert) : 96.0% Accuracy | Precision: 1.0000 | Recall: 0.9286 (Minimizes false alarms and alert fatigue)

Conclusion:
By implementing dynamic REST API fetching, the data pipeline dynamically ingests raw security logs over HTTP. Logistic Regression maps continuous features to calibrated sigmoid probability scores, enabling security operations teams to tune decision boundaries based on system risk tolerance.