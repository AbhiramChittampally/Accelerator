# copy your solution

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

def fetch_api_data(url):
  response = requests.get(url)
  response.raise_for_status()
  data = pd.read_csv(io.StringIO(response.text))
  return data

FLOW_LOGS_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"

penguin_df = fetch_api_data(FLOW_LOGS_API_ENDPOINT)

penguin_df.dropna(inplace=True)

penguin_df['Is_Anomalous'] = np.where(penguin_df['species'] == 'Adelie', 0, 1)

penguin_df.drop(['species','island','sex'],inplace=True,axis=1)

penguin_df.shape

penguin_df['Is_Anomalous'].value_counts()

penguin_df.head(3)

X=penguin_df.drop('Is_Anomalous',axis=1)
y=penguin_df['Is_Anomalous']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42,stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_size = X_train.shape[0]
X_test_size = X_test.shape[0]
y_train_size = y_train.shape[0]
y_test_size = y_test.shape[0]
y_train_counts = y_train.value_counts()
y_test_counts = y_test.value_counts()

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

y_prob = model.predict_proba(X_test_scaled)[:, 1]

model_intercept = model.intercept_
model_coefficients = model.coef_

print(model_intercept)

for col in X.columns:
  print(f"{col:<20} : {round(model_coefficients[0][X.columns.get_loc(col)],3)}")

for i in range(5):
  if y_prob[i]>0.5:
    print(f"Sample {i+1} | P(Anomalous) : {round(y_prob[i],4)} | Label : {y_test.iloc[i]} | Assigned : High Risk")
  else:
    print(f"Sample {i+1} | P(Anomalous) : {round(y_prob[i],4)} | Label : {y_test.iloc[i]} | Assigned : Low Risk")

thresholds = [0.30, 0.50, 0.70]
for threshold in thresholds:
  y_pred_threshold = (y_prob>=threshold).astype(int)
  accuracy = accuracy_score(y_test, y_pred_threshold)
  precision = precision_score(y_test, y_pred_threshold)
  recall = recall_score(y_test, y_pred_threshold)
  print(f"Threshold: {threshold} | Accuracy: {accuracy*100}% | Precision: {precision:.4f} | Recall: {recall:.4f}")


print("\n========== API-DRIVEN LOGISTIC REGRESSION & DECISION BOUNDARY ENGINE ==========")

print("\nData Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)")
print(f"Master Dataset Records     : {penguin_df.shape[0]} (Cleaned & Preprocessed)")

print(
    "Features Included          : "
    "4 Continuous Log Metrics "
    "(bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g)"
)

print(
    "Target Output              : "
    "Is_Anomalous "
    "(Binary Classification: 0 = Standard, 1 = Anomalous)"
)

print("\nModel Training Metrics:")
print(
    f"- Stratified Train Split   : {X_train_size} Records "
    f"({y_train_counts[0]} Normal / {y_train_counts[1]} Anomalous)"
)

print(
    f"- Stratified Test Split    : {X_test_size} Records "
    f"({y_test_counts[0]} Normal / {y_test_counts[1]} Anomalous)"
)

base_accuracy = accuracy_score(y_test, y_pred)

print(
    f"- Base Test Accuracy       : "
    f"{base_accuracy * 100:.1f}% (at Default 0.50 Threshold)"
)

# Probability profiling
max_prob = y_prob.max()
min_prob = y_prob.min()

# Find two largest absolute coefficients
coef_series = pd.Series(model.coef_[0], index=X.columns)
top_drivers = coef_series.abs().sort_values(ascending=False).index[:2]

print("\nSigmoid Probability Profiling:")
print(f"- Maximum Anomalous Prob   : {max_prob * 100:.2f}%")
print(f"- Minimum Anomalous Prob   : {min_prob * 100:.2f}%")

print(
    f"- Key Probability Drivers : "
    f"{top_drivers[0]} ({coef_series[top_drivers[0]]:+.4f}), "
    f"{top_drivers[1]} ({coef_series[top_drivers[1]]:+.4f})"
)

# Threshold evaluation
print("\nDecision Threshold Tuning:")

for threshold in thresholds:

    y_pred_threshold = (y_prob >= threshold).astype(int)

    accuracy = accuracy_score(y_test, y_pred_threshold)
    precision = precision_score(y_test, y_pred_threshold)
    recall = recall_score(y_test, y_pred_threshold)

    if threshold == 0.30:
        description = "Strict"
        explanation = "Maximizes detection for suspicious traffic"

    elif threshold == 0.50:
        description = "Normal"
        explanation = "Balanced baseline model performance"

    else:
        description = "Alert"
        explanation = "Minimizes false alarms and alert fatigue"

    print(
        f"- Threshold @ {threshold:.2f} ({description:<6}) : "
        f"{accuracy * 100:.1f}% Accuracy | "
        f"Precision: {precision:.4f} | "
        f"Recall: {recall:.4f} "
        f"({explanation})"
    )

print("\nConclusion:")
print(
    "By implementing dynamic REST API fetching, the data pipeline dynamically "
    "ingests raw security logs over HTTP. Logistic Regression maps continuous "
    "features to calibrated sigmoid probability scores, enabling security "
    "operations teams to tune decision boundaries based on system risk tolerance."
)