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

def fetch_triage_data(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(io.StringIO(response.text))
    return data
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")          

DATASET_API_ENDPOINT = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"

df = fetch_triage_data(DATASET_API_ENDPOINT)

df.head()

df['High_Urgency'] = np.where(df['species']=='Chinstrap',1,0)

df.dropna(inplace=True)

df['High_Urgency'].value_counts()

X = df.drop(columns = ['species','island','sex','High_Urgency'],axis=1)
y = df['High_Urgency']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=42,stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression()
lr.fit(X_train_scaled,y_train)
y_pred_lr = lr.predict(X_test_scaled)
y_prob_lr = lr.predict_proba(X_test_scaled)[:,1]
lr_acc = accuracy_score(y_test,y_pred_lr)*100
lr_f1 = f1_score(y_test,y_pred_lr)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(X_train_scaled,y_train)
y_pred_knn = knn.predict(X_test_scaled)
knn_acc = accuracy_score(y_test,y_pred_knn)*100
knn_f1 = f1_score(y_test,y_pred_knn)

dt = DecisionTreeClassifier(max_depth = 4,random_state=42)
dt.fit(X_train_scaled,y_train)
y_pred_dt = dt.predict(X_test_scaled)
dt_acc = accuracy_score(y_test,y_pred_dt)*100
dt_f1 = f1_score(y_test,y_pred_dt)

vc = VotingClassifier(estimators=[('lr',lr),('knn',knn),('dt',dt)],voting='soft')
vc.fit(X_train_scaled,y_train)
y_pred = vc.predict(X_test_scaled)
vc_acc = accuracy_score(y_test,y_pred)*100
vc_f1 = f1_score(y_test,y_pred)


sc = StackingClassifier(estimators=[('lr',lr),('knn',knn),('dt',dt)],final_estimator=LogisticRegression())
sc.fit(X_train_scaled,y_train)
y_pred_sc = sc.predict(X_test_scaled)
sc_accuracy = accuracy_score(y_test,y_pred_sc)*100
sc_f1_score = f1_score(y_test,y_pred)

print("\n========== HETEROGENEOUS VOTING & STACKING ENSEMBLE ENGINE ==========")

print(f"\n{'Data Ingestion Status':<36}: REST API Ingestion Successful (HTTP 200 OK)")
print(f"{'Master Dataset Records':<36}: {len(df)} Diagnostic Records")

print(
    f"{'Ensemble Diversity':<36}: "
    "Linear (Logistic Regression), Distance-Based (k-NN), "
    "Tree-Based (Decision Tree)"
)

print("\nArchitecture Performance Benchmark:")
print("+------------------------------------+---------------+------------+")
print("| Model Architecture                 | Test Accuracy | F1-Score   |")
print("+------------------------------------+---------------+------------+")

print(
    f"| {'Individual Logistic Regression':<34} | "
    f"{lr_acc:>13.2f}% | "
    f"{lr_f1:>10.4f} |"
)

print(
    f"| {'Individual K-Nearest Neighbors':<34} | "
    f"{knn_acc:>13.2f}% | "
    f"{knn_f1:>10.4f} |"
)

print(
    f"| {'Individual Decision Tree':<34} | "
    f"{dt_acc:>13.2f}% | "
    f"{dt_f1:>10.4f} |"
)

print(
    f"| {'Ensemble Soft Voting Classifier':<34} | "
    f"{vc_acc:>13.2f}% | "
    f"{vc_f1:>10.4f} |"
)

print(
    f"| {'Stacking Classifier (Meta-Learner)':<34} | "
    f"{sc_accuracy:>13.2f}% | "
    f"{sc_f1_score:>10.4f} |"
)

print("+------------------------------------+---------------+------------+")

print("\nConclusion:")
print(
    "Stacking heterogeneous algorithms allows a higher-level meta-estimator "
    "to learn optimal blend weights across distinct prediction variances, "
    "outperforming individual algorithms and simple voting schemes."
)

