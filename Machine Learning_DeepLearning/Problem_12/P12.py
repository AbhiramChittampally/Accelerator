# copy your solution

import requests
import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, precision_score, recall_score

def fetch_telemetry_data(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(io.StringIO(response.text))  
    return data
  except requests.RequestException as e:
    print(f"Error fetching data: {e}")

HOST_TELEMETRY_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

telemetry_df = fetch_telemetry_data(HOST_TELEMETRY_API_ENDPOINT)

print(telemetry_df.head())

telemetry_df.rename(columns={
    'sepal_length' : 'cpu_usage_pct',
    'sepal_width' : 'memory_usage_pct',
    'petal_length' : 'disk_io_rate',
    'petal_width' : 'network_latency_ms'
},inplace=True)

telemetry_df['Is_Failure'] = np.where(telemetry_df['species'] == 'setosa', 0, 1)

telemetry_df.drop(columns=['species'],inplace=True)

print(telemetry_df.head())

X = telemetry_df.drop(columns=['Is_Failure'],axis=1)
y = telemetry_df['Is_Failure']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

X_train_size = X_train.shape[0]
X_test_size = X_test.shape[0]
y_train_counts = y_train.value_counts()
y_test_counts = y_test.value_counts()

model = DecisionTreeClassifier(criterion='gini',random_state=42)
model.fit(X_train,y_train)
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

train_accuracy = accuracy_score(y_train,train_pred)
test_accuracy = accuracy_score(y_test,test_pred)
accuracy_gap = train_accuracy - test_accuracy

print(train_accuracy*100,test_accuracy*100)
print(accuracy_gap*100)

print((y_train==train_pred).value_counts())

print((y_test==test_pred).value_counts())

feature_importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)
for col in X.columns:
  print(f"{col:<15} : {feature_importance[X.columns.get_loc(col)]:.4f}")

rules = export_text(
    model,
    feature_names=list(X.columns)
)
print(rules)

pruned_model = DecisionTreeClassifier(
    criterion='gini',
    random_state=42,
    max_depth=2,
    min_samples_leaf=5
)
pruned_model.fit(X_train,y_train)
train_pred_pruned = pruned_model.predict(X_train)
test_pred_pruned = pruned_model.predict(X_test)

pruned_train_accuracy = accuracy_score(y_train,train_pred_pruned)
pruned_test_accuracy = accuracy_score(y_test,test_pred_pruned)
pruned_accuracy_gap = pruned_train_accuracy - pruned_test_accuracy

print(pruned_train_accuracy*100,pruned_test_accuracy*100) 
print(pruned_accuracy_gap*100)

print("\n========== API-DRIVEN DECISION TREE & OVERFITTING ENGINE ==========")

print("\nData Ingestion Status      : REST API Ingestion Successful (HTTP 200 OK)")
print(f"Master Dataset Records     : {telemetry_df.shape[0]} Telemetry Logs")
print("Features Included          : 4 Continuous Metrics (cpu_usage_pct, memory_usage_pct, disk_io_rate, network_latency_ms)")
print("Target Output              : Is_Failure (Binary Classification: 0 = Normal, 1 = Failure)")

print("\nModel Training Metrics:")
print(
    f"- Stratified Train Split   : {X_train_size} Records "
    f"({y_train_counts[0]} Normal / {y_train_counts[1]} Failure)"
)
print(
    f"- Stratified Test Split    : {X_test_size} Records "
    f"({y_test_counts[0]} Normal / {y_test_counts[1]} Failure)"
)
print(
    f"- Unpruned Tree Accuracy   : "
    f"Train = {train_accuracy * 100:.2f}% | "
    f"Test = {test_accuracy * 100:.2f}%"
)

print("\nFeature Importance Profiling:")

primary_feature = feature_importance.index[0]
secondary_feature = feature_importance.index[1]

print(
    f"- Primary Root Split Feature: "
    f"{primary_feature} "
    f"(Gini Importance = {feature_importance.iloc[0]:.4f})"
)

print(
    f"- Secondary Split Feature   : "
    f"{secondary_feature} "
    f"(Gini Importance = {feature_importance.iloc[1]:.4f})"
)

# print("\nExtracted Tree Decision Structure:")
# print(export_text(model, feature_names=list(X.columns)))

print("\nHyperparameter Pruning & Regularization:")
print(
    f"- Baseline Unpruned Tree    : "
    f"{test_accuracy * 100:.2f}% Test Accuracy "
    f"(Train/Test Gap = {accuracy_gap * 100:.2f}%)"
)

print(
    f"- Pruned Tree (max_depth=2) : "
    f"{pruned_test_accuracy * 100:.2f}% Test Accuracy "
    f"(Train/Test Gap = {pruned_accuracy_gap * 100:.2f}%)"
)

print("\nConclusion:")
print(
    "By fetching telemetry data dynamically over HTTP REST endpoints, "
    "the pipeline evaluates system health in real time. "
    "Decision Trees provide interpretable decision rules, while "
    "max_depth and min_samples_leaf control model complexity and "
    "help reduce overfitting."
)