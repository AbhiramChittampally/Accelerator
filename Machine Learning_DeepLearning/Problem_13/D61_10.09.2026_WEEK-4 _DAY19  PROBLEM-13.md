PROJECT 13 — API-DRIVEN KNN REGRESSOR & DISTANCE METRIC HYPERPARAMETER ENGINE

Platform: Google Colab

Language: Python

Libraries: Requests, Pandas, NumPy, Scikit-Learn

Submission: Google Colab Notebook

Problem Statement:
-------------------
An urban transportation analytics platform predicts ride-hailing trip durations in minutes. You must construct an API ingestion pipeline to fetch live spatial and traffic records over HTTP, preprocess continuous telemetry features, scale features using StandardScaler, fit a K-Nearest Neighbors (k-NN) Regressor, and systematically tune K hyperparameter values alongside distance metrics (Euclidean vs. Manhattan) to minimize prediction error (MAE and RMSE).

LIVE API ENDPOINTS
Use these active REST endpoints in your fetching function:
-----------------------------

TRIP_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
TRAFFIC_METRICS_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


BOILERPLATE & STARTER CODE
-------------------------

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

TRIP_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
TRAFFIC_METRICS_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

# =====================================================================
# STUDENT TASK 1: IMPLEMENT API FETCHING FUNCTION
# =====================================================================
def fetch_api_dataset(url: str) -> pd.DataFrame:
    """
    Student Implementation Required:
    1. Send an HTTP GET request to the provided URL using requests.get().
    2. Check for HTTP status code errors using response.raise_for_status().
    3. Parse the returned CSV response payload into a Pandas DataFrame using io.StringIO.
    4. Implement error handling (try-except block) for network failures.
    """
    # TODO: Write your API fetching code here
    pass


TASKS & EXPECTED OUTPUTS
----------------------------
TASK 1 — REST API Ingestion & Regression Target Pipeline Setup

Fetch the raw dataset from TRIP_TELEMETRY_API_ENDPOINT using fetch_api_dataset().
 Clean missing values (dropna()). Map numeric features to ride metrics:
 
flipper_length_mm -> distance_km
bill_length_mm -> traffic_density_index
bill_depth_mm -> pickup_hour
Target: body_mass_g -> trip_duration_min (scale by dividing by 100 to represent duration in minutes)
 
Expected Output:
--------------------
 [TASK 1 SUCCESS] API Dataset Ingested & Processed (333 Clean Records)
Feature Range Summary:
- distance_km          : Min = 172.0, Max = 231.0
- traffic_density_index: Min = 32.1,  Max = 59.6
- pickup_hour          : Min = 13.1,  Max = 21.5
- trip_duration_min    : Min = 27.0,  Max = 63.0 (Target Variable)


TASK 2 — Binned Stratified Train-Test Split & Feature Scaling

Continuous regression targets cannot be directly stratified. Use pd.qcut() to bin trip_duration_min into 5 discrete quantile bins. Perform an 80/20 train-test split stratified on these quantile bins using random_state=42. Standardize continuous features using StandardScaler.

Expected Output:
[TASK 2 SUCCESS] Stratified Quantile Split & Feature Scaling Complete.
Training Set Shape : (266, 3) | Target Mean = 42.02 min
Testing Set Shape  : (67, 3)  | Target Mean = 41.98 min
Scaled Features    : Mean = 0.00, Std = 1.00


TASK 3 — Baseline KNN Regressor Fitting

Fit a baseline KNeighborsRegressor(n_neighbors=5, metric='minkowski', p=2) (Euclidean distance) on scaled training data. Predict durations on X_test_scaled and evaluate Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

Expected Output:

[TASK 3 SUCCESS] Baseline KNN Regressor (K=5, Euclidean) Model Trained.
Baseline Test MAE  : 2.85 minutes
Baseline Test RMSE : 3.62 minutes



TASK 4 — Distance Metric & K-Neighbor Hyperparameter Grid SearchIterate over neighbor values K {1, 3, 5, 7, 9, 15} across two distance metrics:
Euclidean Distance (p = 2)
Manhattan Distance (p = 1)
Log and print MAE and RMSE metrics for every hyperparameter combination in a structured output table.

Expected Output:

[TASK 4 SUCCESS] Hyperparameter Grid Search Complete.

K-Neighbors | Distance Metric | Test MAE (min) | Test RMSE (min)
---------------------------------------------------------------
K = 1       | Euclidean (p=2) | 3.42           | 4.38
K = 1       | Manhattan (p=1) | 3.31           | 4.25
K = 3       | Euclidean (p=2) | 2.91           | 3.71
K = 3       | Manhattan (p=1) | 2.78           | 3.55
K = 5       | Euclidean (p=2) | 2.85           | 3.62
K = 5       | Manhattan (p=1) | 2.69           | 3.42
K = 7       | Euclidean (p=2) | 2.72           | 3.48
K = 7       | Manhattan (p=1) | 2.58           | 3.31
K = 9       | Euclidean (p=2) | 2.76           | 3.51
K = 9       | Manhattan (p=1) | 2.63           | 3.36
K = 15      | Euclidean (p=2) | 2.94           | 3.73
K = 15      | Manhattan (p=1) | 2.81           | 3.58


TASK 5 — Optimal Model Selection & Residual Error AnalysisSelect the best hyperparameter configuration (K = 7, Manhattan Distance p=1). Compute prediction residuals (Residual = Y_actual - Y_predicted) for the test set. Print actual duration, predicted duration, and absolute residual error for the first 5 test samples.Expected Output:

[TASK 5 SUCCESS] Optimal Model Selected: K=7, Metric=Manhattan (p=1)

Sample Index | Actual Duration | Predicted Duration | Absolute Residual Error
-----------------------------------------------------------------------------
Sample 1     | 37.50 min       | 36.85 min          | 0.65 min
Sample 2     | 52.00 min       | 50.40 min          | 1.60 min
Sample 3     | 32.50 min       | 33.10 min          | 0.60 min
Sample 4     | 48.00 min       | 49.25 min          | 1.25 min
Sample 5     | 41.00 min       | 40.20 min          | 0.80 min


FINAL EXPECTED OUTPUT
--------------------
========== API-DRIVEN KNN REGRESSOR & DISTANCE HYPERPARAMETER ENGINE ==========

Data Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)
Master Dataset Records     : 333 Trip Records (Cleaned & Processed)
Features Included          : 3 Continuous Distance & Traffic Metrics (distance_km, traffic_density_index, pickup_hour)
Target Output              : trip_duration_min (Continuous Regression Target)

Model Training Metrics:
- Stratified Quantile Split: 266 Train Records / 67 Test Records
- Feature Preprocessing    : StandardScaler Applied (Mean = 0.00, Std = 1.00)
- Baseline Model (K=5, L2) : MAE = 2.85 min | RMSE = 3.62 min

Hyperparameter Tuning Grid:
- Best Distance Metric     : Manhattan Distance (p=1)
- Optimal K-Neighbors      : K = 7
- Optimized Test Performance: MAE = 2.58 min | RMSE = 3.31 min
- Performance Gain         : 9.47% Error Reduction over Baseline

Residual Performance Summary:
- Average Error Margin     : ±2.58 minutes per trip prediction
- Error Variance Bounds    : Maximum Residual Error = 5.12 min | Minimum Residual Error = 0.12 min

Conclusion:
By streaming spatial telemetry over HTTP, feature scaling ensures distance metrics are not biased toward higher-magnitude features like distance_km. Hyperparameter tuning demonstrates that Manhattan distance (L1) outperforms Euclidean distance (L2) for city grid layouts, achieving minimal trip estimation error at K=7.