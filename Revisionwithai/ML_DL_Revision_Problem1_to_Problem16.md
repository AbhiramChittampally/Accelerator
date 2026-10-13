# Machine Learning & Deep Learning Comprehensive Revision Guide (Problems 1 – 16)

---

## 🎯 Master ML/DL Exam Cheat Sheet

### 1. Machine Learning Paradigms
| Paradigm | Target Label $y$ Present? | Core Goal | Algorithms | Use Cases |
| :--- | :---: | :--- | :--- | :--- |
| **Supervised Learning (Classification)** | **Yes** (Discrete / Categories) | Map inputs $X \to$ class label $y \in \{0, 1\}$ or $\{C_1, C_2, \dots, C_k\}$ | Logistic Regression, Decision Trees, Random Forest, Gradient Boosting, k-NN | Churn prediction, fraud detection, patient triage, spam filter |
| **Supervised Learning (Regression)** | **Yes** (Continuous numeric) | Map inputs $X \to$ real-valued number $y \in \mathbb{R}$ | Linear Regression, Ridge/Lasso, k-NN Regressor, Random Forest Regressor | House price prediction, trip duration, salary estimation |
| **Unsupervised Learning** | **No** | Discover hidden structures, patterns, clusters, or lower-dimensional representations | K-Means, Hierarchical Clustering, DBSCAN, PCA, t-SNE | Customer segmentation, anomaly detection, dimension reduction |

---

### 2. Feature Preprocessing & Encoding Matrix
| Preprocessing Step | Technique | When to Use | Formula / Implementation | Exam Trap to Remember |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Value Imputation** | Mean / Median / Mode / Group-wise | Missing numerical or categorical values | Group-wise: `df.groupby('Tier')['Age'].transform('median')` | **Data Leakage:** Compute imputation statistics on **training set only**, then apply to test set! |
| **Nominal Encoding** | **One-Hot Encoding** (`pd.get_dummies` or `OneHotEncoder`) | Unordered categorical variables (e.g., Region: North, South, East) | Binary column per category (drop first to prevent multicollinearity in linear models) | Avoid for high-cardinality features (creates sparse dimensional explosion). |
| **Ordinal Encoding** | **Mapping / OrdinalEncoder** | Ordered categorical variables (e.g., Bronze: 1, Silver: 2, Gold: 3, Platinum: 4) | Integer mapping preserving hierarchy | Never use One-Hot on ordinal data; you destroy natural monotonic ordering. |
| **Standardization** | **`StandardScaler`** | Continuous features with varying scales, especially for distance/gradient models | $z = \frac{x - \mu}{\sigma}$ (Mean = 0, Std = 1) | **Mandatory** for k-NN, SVM, Logistic Regression, Neural Nets. **Not required** for Tree-based models (RF, GBDT). |
| **Min-Max Normalization** | **`MinMaxScaler`** | Bounded features between [0, 1] | $x_{\text{scaled}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$ | Sensitive to outliers (outliers compress standard values into a narrow range). |

---

### 3. Splitting & Validation Strategies
| Method | Description | When to Use | Scikit-Learn Class |
| :--- | :--- | :--- | :--- |
| **Random Split** | Uniform random allocation of indices | Balanced datasets, large sample sizes | `train_test_split(X, y, test_size=0.2, random_state=42)` |
| **Stratified Split** | Preserves target class proportions in train & test sets | **Imbalanced classification** | `train_test_split(..., stratify=y)` or `StratifiedShuffleSplit` |
| **K-Fold CV** | Splits data into $K$ equal folds; trains on $K-1$, validates on 1; repeats $K$ times | Regression or balanced classification | `KFold(n_splits=5, shuffle=True, random_state=42)` |
| **Stratified K-Fold CV**| Splits into $K$ folds while ensuring each fold has identical class ratios | **Standard benchmark for classification** | `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` |

---

### 4. Classification Metrics Reference
| Metric | Formula | When to Prioritize | Exam Interpretation |
| :--- | :---: | :--- | :--- |
| **Accuracy** | $\frac{TP + TN}{TP + TN + FP + FN}$ | Balanced classes only | **Deceptive on imbalanced data!** If 95% of transactions are genuine, a dummy model predicting all 0s achieves 95% accuracy while catching 0 frauds. |
| **Precision** | $\frac{TP}{TP + FP}$ | When False Positives ($FP$) are costly | High precision means: "When model predicts Positive, it is almost always correct" (e.g. spam detection). |
| **Recall (Sensitivity)**| $\frac{TP}{TP + FN}$ | When False Negatives ($FN$) are dangerous | High recall means: "Model catches almost all actual positive cases" (e.g. disease screening, fraud detection). |
| **F1-Score** | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | Imbalanced datasets | Harmonic mean of Precision and Recall. Balances both metrics. |
| **ROC-AUC** | Area under TPR vs FPR curve | Ranking ability across all thresholds | Measures class separability. Baseline random guess = 0.50; Perfect = 1.00. |

---

### 5. Regression Metrics Reference
| Metric | Formula | Unit | Sensitivity to Outliers |
| :--- | :---: | :---: | :---: |
| **MAE (Mean Absolute Error)** | $\frac{1}{n} \sum \|y_i - \hat{y}_i\|$ | Same as $y$ | Robust (linear penalty) |
| **MSE (Mean Squared Error)** | $\frac{1}{n} \sum (y_i - \hat{y}_i)^2$ | $(y)^2$ | Very High (quadratic penalty) |
| **RMSE (Root Mean Squared Error)** | $\sqrt{\text{MSE}}$ | Same as $y$ | High (penalizes large errors heavily) |
| **$R^2$ Score** | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | Unitless ($-\infty, 1.0]$) | Fraction of target variance explained by model |

---
---

# Deep Dive: Problems 1 to 16

---

## 🔹 PROBLEM 1: Smart Employee Attendance Prediction
**File:** [`Machine Learning_DeepLearning/Problem_1/P1.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_1/P1.py) | [`Problem_1 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_1/D57_03.09.2026_%20Week-4-Day16-Problem-1.md)

### Core Concepts:
- **Supervised Binary Classification**: Input features $X$ map to binary label $y \in \{0, 1\}$ (`Present`: 1, `Absent`: 0).
- **Rule-Based System vs. Machine Learning**:
  - *Rule-Based*: Static, human-crafted `if-else` thresholds (e.g., `if Distance > 30 and Public_Transit == 0: Absent`). Fails on complex non-linear edge cases, cannot adapt automatically, brittle.
  - *Machine Learning*: Learns statistical decision boundaries directly from historical empirical data; handles probability confidence scores.
- **Feature Space Construction**:
  - Numerical inputs: `Distance_KM`, `Prior_Absences_Year`.
  - Binary categorical indicator: `Public_Transit_Access` (0 or 1).

### Key Takeaway for Test:
Rule-based systems have **zero learning capability** (no parameters $\theta$, no loss minimization). ML fits mathematical weights to features by minimizing an empirical loss function.

---

## 🔹 PROBLEM 2: E-Commerce Customer Churn Prediction
**File:** [`Machine Learning_DeepLearning/Problem_2/P2.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_2/P2.py) | [`Problem_2 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_2/D57_05.09.2026_%20Week-4-Day17-Problem-2.md)

### Core Concepts:
- **Churn Rate Calculation**:
  $$\text{Churn Rate} = \frac{\text{Total Churned Customers}}{\text{Total Customers}} \times 100$$
- **Feature Impact on Churn**:
  - `Days_Since_Last_Login`: Strong positive correlation with churn (inactive users leave).
  - `Customer_Support_Calls`: High call frequency signals dissatisfaction (high churn probability).
  - `Monthly_Spend_USD`: Higher engagement often inversely correlates with churn.
- **Supervised Binary Classification Architecture**:
  - $X = [\text{Monthly\_Spend}, \text{Days\_Since\_Last\_Login}, \text{Support\_Calls}]$
  - $y \in \{0, 1\}$ where $1 = \text{Churned}$.

---

## 🔹 PROBLEM 3: Enterprise Logistics & Fleet Delay Analytics
**File:** [`Machine Learning_DeepLearning/Problem_3/P3.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_3/P3.py) | [`Problem_3 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_3/D57_05.09.2026_%20Week-4-Day16-Problem-3.md)

### Core Concepts:
- **Multi-Source Relational Merging in Pandas**:
  ```python
  # Join Shipments with Fleet Metadata and Weather Logs
  df_merged = df_shipments.merge(df_fleet, on='Vehicle_ID', how='inner')
  df_merged = df_merged.merge(df_weather, on=['Origin_Hub', 'Dispatch_Date'], how='left')
  ```
- **Operational Profiling**:
  - Tracking fleet health: `Vehicle_Age_Years`, `Maintenance_Score`.
  - Environmental factors: `Precipitation_MM`, `Wind_Speed_KMPH`.
- **Target Imbalance**:
  - Measuring class distribution using `df['Delayed'].value_counts(normalize=True)`.
  - Rare delays mean standard accuracy is insufficient.

---

## 🔹 PROBLEM 4: Financial Credit Card Fraud & Risk Auditing
**File:** [`Machine Learning_DeepLearning/Problem_4/P4.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_4/P4.py) | [`Problem_4 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_4/D58_07.09.2026_WEEK-4%20_DAY16%20%20PROBLEM-4.md)

### Core Concepts:
- **4-Table Enterprise Relational Integration**:
  1. `Transactions` (Fact table: `Tx_ID`, `Account_ID`, `Device_ID`, `Amount_USD`)
  2. `Account Metadata` (Dimension: `Account_Age_Days`, `Risk_Score`)
  3. `Terminal Devices` (Dimension: `Device_Trust_Level`, `OS_Version`)
  4. `Risk Blacklists` (Audit: `Is_Blacklisted_Entity`)
- **Schema Validation & Foreign Key Integrity**:
  - Verifying null counts post-merge: `df.isnull().sum()`.
  - Inner vs Left join decision based on whether unlisted devices/accounts should be retained or flagged.

---

## 🔹 PROBLEM 5: Multi-Class Patient Triage Classification
**File:** [`Machine Learning_DeepLearning/Problem_5/P5.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_5/P5.py) | [`Problem_5 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_5/D58_07.09.2026_WEEK-4%20_DAY17%20%20PROBLEM-5.md)

### Core Concepts:
- **Multi-Class vs Binary Classification**:
  - Target $y \in \{\text{'Low'}, \text{'Medium'}, \text{'Critical'}\}$ ($K = 3$ classes).
- **Group-Wise Feature Profiles**:
  ```python
  df.groupby('Triage_Level')[['Heart_Rate_BPM', 'Systolic_BP', 'Oxygen_Sat_Pct']].mean()
  ```
  - Critical patients display physiological deterioration: low oxygen saturation ($< 90\%$), abnormal BP, high heart rate.
- **Multi-Class Algorithm Selection**:
  - Multinomial Logistic Regression (using Softmax): $P(y = c \mid x) = \frac{e^{w_c^T x}}{\sum_{j=1}^K e^{w_j^T x}}$
  - Decision Trees / Random Forests (natively support multi-class via split criterion).

---

## 🔹 PROBLEM 6: Real Estate Asset Valuation (Regression)
**File:** [`Machine Learning_DeepLearning/Problem_6/P6.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_6/P6.py) | [`Problem_6 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_6/D59_08.09.2026_WEEK-4%20_DAY17%20%20PROBLEM-6.md)

### Core Concepts:
- **Continuous Target Space**:
  - $y = \text{Sale\_Price\_USD} \in \mathbb{R}^+$ (Regression task, NOT classification).
- **Pearson Correlation Matrix ($r$)**:
  $$r_{xy} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
  - Identifies linear relationships: `Living_Area_SqFt` ($r \approx +0.85$ strong positive), `Property_Age_Years` ($r < 0$ negative).
- **Multicollinearity Diagnostic**:
  - High correlation between two predictors (e.g. `Bedrooms` and `Bathrooms`) indicates redundant information.

---

## 🔹 PROBLEM 7: Customer Behavior Clustering (Unsupervised Learning)
**File:** [`Machine Learning_DeepLearning/Problem_7/P7.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_7/P7.py) | [`Problem_7 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_7/D59_08.09.2026_WEEK-4%20_DAY17%20%20PROBLEM-7.md)

### Core Concepts:
- **Absence of Ground Truth Target $y$**:
  - The objective is grouping samples based on geometric similarity in feature space.
- **Why Feature Scaling is Mandatory for Clustering**:
  - Euclidean distance: $d(p, q) = \sqrt{\sum (p_i - q_i)^2}$.
  - If `Annual_Spend` ranges from $\$100$ to $\$50,000$ and `Login_Frequency` ranges from $1$ to $30$, spend will completely dominate the distance computation! Scaling normalizes all axes equally.
- **Cluster Centroid Profiling**:
  - Once clusters are formed, calculate the mean of each feature per cluster to define human-interpretable personas (e.g., Cluster 0 = "Power Users", Cluster 1 = "Casual Browsers").

---

## 🔹 PROBLEM 8: End-to-End Data Preparation & Encoding Pipeline
**File:** [`Machine Learning_DeepLearning/Problem_8/P8.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_8/P8.py) | [`Problem_8 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_8/D60_09.09.2026_WEEK-4%20_DAY18%20%20PROBLEM-8.md)

### Core Concepts:
1. **Group-Wise Missing Value Imputation**:
   ```python
   # Impute missing Age using median Age within each Account_Tier
   df['Age'] = df.groupby('Account_Tier')['Age'].transform(lambda x: x.fillna(x.median()))
   ```
2. **Outlier Detection & Capping (IQR Method)**:
   $$\text{IQR} = Q_3 - Q_1, \quad \text{Lower} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Upper} = Q_3 + 1.5 \times \text{IQR}$$
   - Values outside boundaries are capped/clipped rather than deleted to retain sample count.
3. **Encoding Strategy**:
   - **Ordinal Encoding**: `Account_Tier` $\to$ `{'Bronze': 1, 'Silver': 2, 'Gold': 3, 'Platinum': 4}`.
   - **One-Hot Encoding**: `Region` $\to$ `North`, `South`, `East`, `West` via `pd.get_dummies(..., drop_first=True)`.
4. **Standardization**:
   ```python
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X_continuous)
   ```

---

## 🔹 PROBLEM 9: Train-Test Splitting & Stratified Sampling Audit
**File:** [`Machine Learning_DeepLearning/Problem_9/P9.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_9/P9.py) | [`Problem_9 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_9/D60_09.09.2026_WEEK-4%20_DAY18%20%20PROBLEM-9.md)

### Core Concepts:
- **Random vs. Stratified Splitting**:
  ```python
  # Random Split (May cause distribution drift in rare classes)
  X_tr_rnd, X_te_rnd, y_tr_rnd, y_te_rnd = train_test_split(X, y, test_size=0.2, random_state=42)

  # Stratified Split (Guarantees matching class proportions)
  X_tr_str, X_te_str, y_tr_str, y_te_str = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
  ```
- **Distribution Drift Analysis**:
  - If rare disease class is $10\%$ in total data:
    - Random split might yield $14\%$ in train and $0\%$ in test (severe failure!).
    - Stratified split enforces exactly $10\%$ in train and $10\%$ in test.
- **Data Leakage Prohibition**: Preprocessing parameters (e.g., mean, std) must be calculated on `X_train` only and used to transform `X_test`.

---

## 🔹 PROBLEM 10: Cross-Validation & Overfitting Diagnostics
**File:** [`Machine Learning_DeepLearning/Problem_10/P10.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_10/P10.py) | [`Problem_10 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_10/D60_09.09.2026_WEEK-4%20_DAY18%20%20PROBLEM-10.md)

### Core Concepts:
- **K-Fold vs. Stratified K-Fold**:
  ```python
  from sklearn.model_selection import StratifiedKFold
  skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
  for train_idx, val_idx in skf.split(X, y):
      X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
      y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]
  ```
- **Overfitting Diagnostics**:
  - **High Bias (Underfitting)**: Both Train Accuracy and Validation Accuracy are low.
  - **High Variance (Overfitting)**: Train Accuracy $\approx 99\%$, but Validation Accuracy $\approx 65\%$ (huge divergence).
  - **Well-Generalized Model**: Train and Validation scores are close and sufficiently high.

---

## 🔹 PROBLEM 11: Real-Time Network Security Logistic Regression Engine
**File:** [`Machine Learning_DeepLearning/Problem_11/P11.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_11/P11.py) | [`Problem_11 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_11/D61_10.09.2026_WEEK-4%20_DAY19%20%20PROBLEM-11.md)

### Core Concepts:
- **Sigmoid Activation Function**:
  $$\sigma(z) = \frac{1}{1 + e^{-z}}, \quad \text{where } z = w^T x + b$$
  - Maps any real number $z \in (-\infty, +\infty)$ to a probability $P(y = 1 \mid x) \in [0, 1]$.
- **Probability Profiling & Custom Threshold Tuning**:
  ```python
  # Predict continuous probabilities
  y_prob = model.predict_proba(X_test_scaled)[:, 1]

  # Apply custom decision threshold (e.g. 0.3 for security sensitivity)
  y_pred_custom = (y_prob >= 0.3).astype(int)
  ```
  - Lowering threshold ($0.5 \to 0.3$): Increases **Recall** (catches more anomalies), decreases **Precision** (more false alarms).
  - Raising threshold ($0.5 \to 0.7$): Increases **Precision**, decreases **Recall**.
- **Log-Odds Interpretation of Coefficients ($w_i$)**:
  - Positive $w_i$: Increases probability of anomaly.
  - Odds ratio = $e^{w_i}$.

---

## 🔹 PROBLEM 12: API-Driven Decision Tree & Feature Importance
**File:** [`Machine Learning_DeepLearning/Problem_12/P12.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_12/P12.py) | [`Problem_12 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_12/D61_10.09.2026_WEEK-4%20_DAY19%20%20PROBLEM-12.md)

### Core Concepts:
- **Split Impurity Metrics**:
  - **Gini Impurity**: $Gini(p) = 1 - \sum_{i=1}^C p_i^2$ (computational default in scikit-learn).
  - **Entropy**: $H(p) = -\sum_{i=1}^C p_i \log_2(p_i)$.
  - **Information Gain**: Reduction in impurity after splitting: $IG(D, A) = Impurity(D) - \sum \frac{\|D_v\|}{\|D\|} Impurity(D_v)$.
- **Pruning to Eliminate Overfitting**:
  - *Unpruned Tree* (`max_depth=None`): Splits until every leaf is pure $\to$ Train accuracy $= 100\%$, Test accuracy drops significantly (Overfitting).
  - *Pruned Tree* (`max_depth=3`): Restricts tree complexity $\to$ Prevents memorization, improves test generalization.
- **Tree Visualization & Feature Importance**:
  ```python
  from sklearn.tree import export_text
  print(export_text(model, feature_names=list(X.columns)))
  # Feature importance sums to 1.0
  print(model.feature_importances_)
  ```

---

## 🔹 PROBLEM 13: API-Driven KNN Regressor & Distance Metrics
**File:** [`Machine Learning_DeepLearning/Problem_13/P13.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_13/P13.py) | [`Problem_13 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_13/D61_10.09.2026_WEEK-4%20_DAY19%20%20PROBLEM-13.md)

### Core Concepts:
- **K-Nearest Neighbors Algorithm**:
  - Non-parametric, lazy learner (stores training data, computes distances at inference time).
  - Continuous target prediction: takes average of $K$ nearest neighbors: $\hat{y} = \frac{1}{K} \sum_{i=1}^K y_i$.
- **Distance Metrics ($p$-parameter in Minkowski)**:
  - **Euclidean Distance** ($p=2$): Straight-line $L_2$ norm: $d = \sqrt{\sum (x_i - y_i)^2}$.
  - **Manhattan Distance** ($p=1$): Grid-like $L_1$ norm: $d = \sum \|x_i - y_i\|$.
- **Effect of Hyperparameter $K$**:
  - $K = 1$: Memorizes closest point $\to$ High Variance / Overfitting (noisy decision boundaries).
  - Very large $K \approx N$: Predicts dataset mean $\to$ High Bias / Underfitting.
- **Metric Evaluation**:
  - Evaluated using **MAE** and **RMSE**.

---

## 🔹 PROBLEM 14: Imbalanced Fraud Detection via Class-Weighted Random Forests
**File:** [`Machine Learning_DeepLearning/Problem_14/P14.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_14/P14.py) | [`Problem_14 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_14/Problem_14.md)

### Core Concepts:
- **The Accuracy Paradox**:
  - On a dataset with 90% non-fraud and 10% fraud, a model predicting "Never Fraud" gets 90% accuracy but has **0% Recall**.
- **Class-Weighted Cost-Sensitive Learning**:
  ```python
  from sklearn.ensemble import RandomForestClassifier
  # Standard model
  std_rf = RandomForestClassifier(random_state=42)

  # Balanced model
  balanced_rf = RandomForestClassifier(class_weight='balanced', random_state=42)
  ```
  - `class_weight='balanced'` automatically adjusts loss weights inversely proportional to class frequencies:
    $$w_c = \frac{N}{K \cdot N_c}$$
  - Forces the ensemble to penalize misclassifying the minority fraud class much more heavily.
- **Comparison Outcome**:
  - `balanced_rf` significantly increases **Recall** and **F1-Score** for fraud detection.

---

## 🔹 PROBLEM 15: Gradient Boosting & Early Stopping Optimization
**File:** [`Machine Learning_DeepLearning/Problem_15/P15.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_15/P15.py) | [`Problem_15 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_15/Problem_15.md)

### Core Concepts:
- **Gradient Boosting Mechanism (Sequential Ensembling)**:
  - Unlike Random Forests (which build independent trees in parallel), Gradient Boosting builds trees sequentially:
    $$F_m(x) = F_{m-1}(x) + \eta \cdot h_m(x)$$
  - Each new tree $h_m(x)$ fits the **pseudo-residuals** (negative gradient of the loss function) of the previous ensemble.
  - $\eta$ is the `learning_rate`.
- **Early Stopping Hyperparameters**:
  ```python
  from sklearn.ensemble import GradientBoostingClassifier
  gb = GradientBoostingClassifier(
      n_estimators=300,
      learning_rate=0.05,
      validation_fraction=0.15,  # 15% withheld internally for validation
      n_iter_no_change=5,        # Stop if no improvement after 5 iterations
      tol=1e-4,                  # Minimum threshold to qualify as improvement
      random_state=42
  )
  ```
  - Automatically terminates tree additions when validation loss plateaus, guaranteeing optimal bias-variance balance.

---

## 🔹 PROBLEM 16: Heterogeneous Voting & Stacking Ensemble Engine
**File:** [`Machine Learning_DeepLearning/Problem_16/P16.py`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_16/P16.py) | [`Problem_16 MD`](file:///C:/Users/Abhiram%20Chittampally/Documents/ACC/Machine%20Learning_DeepLearning/Problem_16/Problem_16.md)

### Core Concepts:
1. **Base Estimators Diversity**:
   - Ensemble combines 3 fundamentally different mathematical architectures:
     - `lr`: Logistic Regression (linear boundary)
     - `knn`: K-Nearest Neighbors (instance/distance-based local boundary)
     - `dt`: Decision Tree (orthogonal axis-aligned recursive splits)
2. **Hard Voting vs. Soft Voting**:
   - **Hard Voting** (`voting='hard'`): Majority rule on predicted discrete class labels ($y \in \{0, 1\}$).
   - **Soft Voting** (`voting='soft'`): Averages predicted probabilities:
     $$\hat{P}(c) = \frac{1}{M} \sum_{m=1}^M P_m(c)$$
     Selects class with highest average probability. **Soft voting is superior** because it rewards confident predictions.
3. **Stacking Classifier (`StackingClassifier`)**:
   ```python
   from sklearn.ensemble import StackingClassifier
   estimators = [('lr', lr), ('knn', knn), ('dt', dt)]
   stacking = StackingClassifier(
       estimators=estimators,
       final_estimator=LogisticRegression(),
       cv=5
   )
   ```
   - Uses cross-validation to generate out-of-fold predictions from base learners.
   - A meta-learner (`final_estimator`) trains on these predictions to learn which model to trust in which regions of the feature space.

---
---

## 💡 Top 6 Machine Learning Exam Traps

1. **Feature Scaling on Tree Models vs. Distance Models:**
   - **Trees (Decision Tree, Random Forest, GBDT)**: Completely invariant to monotonic feature scaling! Scaling does not change split points.
   - **Distance/Gradient Models (k-NN, Logistic Regression, Neural Nets)**: Scaling is **strictly mandatory**.

2. **The Accuracy Trap on Imbalanced Data:**
   - Always report **Precision, Recall, F1-Score, or ROC-AUC** for imbalanced datasets. Never judge an imbalanced classifier on Accuracy alone!

3. **Data Leakage in Normalization/Imputation:**
   - Never fit a scaler or imputer on the full dataset before splitting:
     - ❌ `X_scaled = scaler.fit_transform(X); train_test_split(X_scaled)` (Data Leakage!)
     - ✅ `train_test_split(X); scaler.fit(X_train); scaler.transform(X_train); scaler.transform(X_test)`

4. **Underfitting vs. Overfitting Diagnostic Table:**
   - `Train High, Test Low` $\to$ **Overfitting (High Variance)**. Fix: prune tree, add regularization, dropout, increase training data, reduce features.
   - `Train Low, Test Low` $\to$ **Underfitting (High Bias)**. Fix: use a more complex model, engineer features, decrease regularization.

5. **Decision Threshold Tuning:**
   - Default threshold is $0.5$. Lowering the threshold detects **more positives** (higher Recall, lower Precision). Raising threshold requires higher confidence (higher Precision, lower Recall).

6. **Voting vs. Stacking:**
   - **Voting**: Combines base models via a fixed heuristic (simple average or majority vote). No extra weights are learned.
   - **Stacking**: Trains a **meta-model** to dynamically learn optimal combination weights.
