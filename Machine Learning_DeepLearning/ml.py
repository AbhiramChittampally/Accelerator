"""
================================================================================
MACHINE LEARNING REFERENCE IMPLEMENTATIONS & CODE COOKBOOK
================================================================================
A structured, end-to-end boilerplate and reference guide covering:
  1. Baseline Machine Learning & Data Splitting
  2. Multimodal & Unstructured Data Ingestion (Text, Images, Live APIs)
  3. Data Cleaning, Imputation & Feature Scaling
  4. Feature Engineering, Categorical Encoding & Selection
  5. Mathematical & Statistical Foundations from Scratch
  6. Linear Algebra with NumPy
  7. Calculus, Derivatives & Optimization from Scratch
  8. Exploratory Data Analysis (EDA) & Data Visualization
  9. Supervised Learning: Regression Models & Metrics
 10. Supervised Learning: Classification Models & Pipelines
 11. Classification Evaluation Metrics & Hyperparameter Tuning
 12. Unsupervised Learning: Clustering (K-Means, Hierarchical, DBSCAN, GMM, etc.)
 13. Unsupervised Learning: Dimensionality Reduction (PCA, SVD, LDA, t-SNE, UMAP)
 14. Unsupervised Learning: Association Rule Mining (Apriori & FP-Growth)
 15. Unsupervised Learning: Topic Modeling (LDA & NMF)
 16. Bias-Variance Diagnosis & Learning Curves (learning_curve)
 17. Advanced Ensemble Learning: AdaBoost, GBM, XGBoost, LightGBM, CatBoost & Stacking
 18. Advanced Feature Engineering: Target Encoding with Smoothing, Power Transforms & Discretization
 19. Modern Hyperparameter Optimization: Optuna with Bayesian TPE & Pruning
 20. Machine Learning Experiment Tracking: MLflow Architecture & Logging
 21. Model Interpretability & Explainability (XAI): Permutation Importance & SHAP / PDP
 22. Semi-Supervised Learning: Pseudo-Labeling with SelfTrainingClassifier
 23. End-to-End Capstone Production Pipeline: Customer Churn Prediction
================================================================================
"""

# ==============================================================================
# 1. BASELINE MACHINE LEARNING & DATA SPLITTING
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.1 Simple End-to-End ML Pipeline (Linear Regression on Housing Data)
# ------------------------------------------------------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib

# Load housing dataset
df_houses = pd.read_csv("houses.csv")

# Clean missing rows
df_houses = df_houses.dropna()

# Separate feature matrix X and target vector y
X_houses = df_houses[["sqft", "bedrooms", "age_years"]]
y_houses = df_houses["sale_price"]

# Split into 80% training and 20% testing
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(
    X_houses,
    y_houses,
    test_size=0.2,
    random_state=42
)

# Initialize and train linear regression model
baseline_model = LinearRegression()
baseline_model.fit(X_train_h, y_train_h)

# Generate predictions on unseen test data
house_predictions = baseline_model.predict(X_test_h)

# Evaluate using Mean Absolute Error (MAE)
mae_score = mean_absolute_error(y_test_h, house_predictions)
print(f"Mean Absolute Error: ${mae_score:,.0f}")

# Persist trained model artifact to disk
joblib.dump(baseline_model, "house_price_model.pkl")


# ------------------------------------------------------------------------------
# 1.2 Standard 3-Way Split: 70% Train, 15% Validation, 15% Test
# ------------------------------------------------------------------------------
from sklearn.model_selection import train_test_split
import pandas as pd

# Load dataset
df_split = pd.read_csv("houses.csv")

# Separate features and target
X_raw = df_split.drop("sale_price", axis=1)
y_raw = df_split["sale_price"]

# Step 1: Carve out 15% for final untouched test set
X_temp, X_test_split, y_temp, y_test_split = train_test_split(
    X_raw,
    y_raw,
    test_size=0.15,
    random_state=42
)

# Step 2: Split remaining 85% into 70% train and 15% validation
# Note: 0.15 / 0.85 ≈ 0.176
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
    X_temp,
    y_temp,
    test_size=0.176,
    random_state=42
)

print(f"Train size: {len(X_train_split)} (70%)")
print(f"Validation size: {len(X_val_split)} (15%)")
print(f"Test size: {len(X_test_split)} (15%)")


# ------------------------------------------------------------------------------
# 1.3 Generic 3-Way Train/Validation/Test Split Template
# ------------------------------------------------------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split

# Load generic dataset
df_generic = pd.read_csv("data.csv")

# Separate features and target
X_gen = df_generic.drop("target", axis=1)
y_gen = df_generic["target"]

# Carve out final test set (15%)
X_temp_gen, X_test_gen, y_temp_gen, y_test_gen = train_test_split(
    X_gen,
    y_gen,
    test_size=0.15,
    random_state=42
)

# Split remaining 85% into training (70% total) and validation (15% total)
X_train_gen, X_val_gen, y_train_gen, y_val_gen = train_test_split(
    X_temp_gen,
    y_temp_gen,
    test_size=0.176,
    random_state=42
)

print("Training shape:", X_train_gen.shape)
print("Validation shape:", X_val_gen.shape)
print("Test shape:", X_test_gen.shape)


# ------------------------------------------------------------------------------
# 1.4 Chronological Train/Test Split for Time Series Data
# ------------------------------------------------------------------------------
import pandas as pd

# Load time-series dataset with datetime parsing
df_ts = pd.read_csv(
    "stock_prices.csv",
    parse_dates=["date"]
)

# Critical: Sort chronologically to prevent temporal leakage
df_ts = df_ts.sort_values("date")

# Determine chronological split boundary (80% train, 20% test)
split_index = int(len(df_ts) * 0.8)

# Historical observations -> Training
train_ts = df_ts.iloc[:split_index]

# Future observations -> Testing
test_ts = df_ts.iloc[split_index:]

print(f"Time Series Train points: {len(train_ts)}, Test points: {len(test_ts)}")


# ==============================================================================
# 2. MULTIMODAL & UNSTRUCTURED DATA INGESTION
# ==============================================================================

# ------------------------------------------------------------------------------
# 2.1 Text Feature Extraction using Bag of Words (CountVectorizer)
# ------------------------------------------------------------------------------
from sklearn.feature_extraction.text import CountVectorizer

reviews = [
    "Great product, loved it",
    "Terrible quality, disappointed",
    "Good value for money"
]

# Instantiate CountVectorizer
vectorizer = CountVectorizer()

# Tokenize and build vocabulary matrix
X_text = vectorizer.fit_transform(reviews)

print("Vocabulary mapping:", vectorizer.vocabulary_)
print("Feature matrix shape:", X_text.shape)


# ------------------------------------------------------------------------------
# 2.2 Image Preprocessing & Pixel Normalization (PIL & NumPy)
# ------------------------------------------------------------------------------
from PIL import Image
import numpy as np

# Load raw image from disk
img = Image.open("cat.jpg")

# Standardize dimensions to expected model resolution (e.g., 224x224)
img_resized = img.resize((224, 224))

# Convert image object into a NumPy pixel array (Height x Width x Channels)
img_array = np.array(img_resized)

# Normalize pixel values from [0, 255] to [0.0, 1.0] for neural network stability
img_normalized = img_array / 255.0

print("Normalized Image Array Shape:", img_normalized.shape)


# ------------------------------------------------------------------------------
# 2.3 Live Data Ingestion via REST API with Retry & Exponential Backoff
# ------------------------------------------------------------------------------
import requests
import pandas as pd
import time

API_KEY = "your_key_here"

CITIES = [
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Kolkata"
]

results = []

for city in CITIES:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # Implement retry loop with exponential backoff
    for attempt in range(3):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results.append({
                "city": city,
                "temp_c": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["main"]
            })
            break  # Success: break out of retry loop

        except requests.RequestException as e:
            wait = 2 ** attempt
            print(f"Attempt {attempt + 1} failed for {city}: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    time.sleep(1)  # Respect API rate limits

df_weather = pd.DataFrame(results)
print(df_weather)


# ------------------------------------------------------------------------------
# 2.4 Generic REST API Fetch Template with Exponential Backoff
# ------------------------------------------------------------------------------
import requests
import pandas as pd
import time

API_KEY = "your_api_key"
url = "https://api.example.com/data"
params = {"api_key": API_KEY}
results_api = []

for attempt in range(3):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results_api.append({
            "feature1": data["feature1"],
            "feature2": data["feature2"]
        })
        break

    except requests.RequestException as e:
        wait = 2 ** attempt
        print(f"Request failed: {e}. Retrying in {wait} seconds.")
        time.sleep(wait)

df_api = pd.DataFrame(results_api)
print(df_api)


# ==============================================================================
# 3. DATA CLEANING, IMPUTATION & FEATURE SCALING
# ==============================================================================

# ------------------------------------------------------------------------------
# 3.1 Tabular Data Inspection & Feature/Target Separation
# ------------------------------------------------------------------------------
import pandas as pd

# Load CSV data
df_data = pd.read_csv("data.csv")

# Inspect structural attributes
print("Head:")
print(df_data.head())
print("Shape:", df_data.shape)
print("Columns:", df_data.columns)
print("Info:")
print(df_data.info())
print("Summary Statistics:")
print(df_data.describe())

# Separate features and target
X_tabular = df_data[["feature1", "feature2", "feature3"]]
y_tabular = df_data["target"]


# ------------------------------------------------------------------------------
# 3.2 Standalone IQR-Based Outlier Capping Function
# ------------------------------------------------------------------------------
def cap_outliers(series: pd.Series) -> pd.Series:
    """Caps numerical outliers using the 1.5 * IQR rule."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return series.clip(lower=lower_bound, upper=upper_bound)


# ------------------------------------------------------------------------------
# 3.3 Comprehensive Tabular Data Cleaning Pipeline
# ------------------------------------------------------------------------------
import pandas as pd

# Load dirty dataset
df_clean = pd.read_csv("data.csv")

# 1. Audit missing values and duplicates
print("Missing values per column:\n", df_clean.isnull().sum())
print("Duplicate rows:", df_clean.duplicated().sum())

# 2. Impute numerical columns using median (robust to outliers)
numeric_cols = ["age", "income", "sqft"]
for col in numeric_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# 3. Impute categorical columns using mode (most frequent category)
categorical_cols = ["city", "category"]
for col in categorical_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# 4. Remove records where target variable is missing
df_clean = df_clean.dropna(subset=["target"])

# 5. Drop duplicate rows
df_clean = df_clean.drop_duplicates()

# 6. Apply IQR outlier capping on designated numerical features
for col in ["income", "target"]:
    if col in df_clean.columns:
        df_clean[col] = cap_outliers(df_clean[col])

print("Cleaned shape:", df_clean.shape)


# ------------------------------------------------------------------------------
# 3.4 Feature Scaling: StandardScaler vs. MinMaxScaler (Leak-Proof Split First)
# ------------------------------------------------------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load dataset
df_scale = pd.read_csv("data.csv")
X_sc = df_scale[["feature1", "feature2", "feature3"]]
y_sc = df_scale["target"]

# CRITICAL: Always split data BEFORE scaling to prevent data leakage
X_train_sc, X_test_sc, y_train_sc, y_test_sc = train_test_split(
    X_sc,
    y_sc,
    test_size=0.2,
    random_state=42
)

# 1. Standardization (Z-score: mean = 0, std = 1)
scaler = StandardScaler()
# Fit strictly on training set, then transform both train and test
X_train_scaled = scaler.fit_transform(X_train_sc)
X_test_scaled = scaler.transform(X_test_sc)

# 2. Min-Max Normalization (bounded strictly between 0 and 1)
minmax = MinMaxScaler(feature_range=(0, 1))
X_train_norm = minmax.fit_transform(X_train_sc)
X_test_norm = minmax.transform(X_test_sc)

print("Standardized Train Mean (approx 0):", X_train_scaled.mean(axis=0))
print("Standardized Train Std (approx 1):", X_train_scaled.std(axis=0))
print("Normalized Train Min (0):", X_train_norm.min(axis=0))
print("Normalized Train Max (1):", X_train_norm.max(axis=0))


# ==============================================================================
# 4. FEATURE ENGINEERING, ENCODING & SELECTION
# ==============================================================================

# ------------------------------------------------------------------------------
# 4.1 Temporal Features, Derived Interactions, Encoding & Filter Selection
# ------------------------------------------------------------------------------
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.feature_selection import SelectKBest, f_regression

df_fe = pd.read_csv("data.csv")

# 1. Temporal feature extraction
df_fe["order_date"] = pd.to_datetime(df_fe["order_date"])
df_fe["hour"] = df_fe["order_date"].dt.hour
df_fe["day_of_week"] = df_fe["order_date"].dt.dayofweek
df_fe["is_weekend"] = df_fe["day_of_week"].isin([5, 6]).astype(int)
df_fe["month"] = df_fe["order_date"].dt.month

# 2. Domain-specific ratios & interaction features
df_fe["unit_price"] = df_fe["total_amount"] / df_fe["quantity"]
df_fe["price_per_sqft"] = df_fe["sale_price"] / df_fe["sqft"]
df_fe["bedrooms_per_sqft"] = df_fe["bedrooms"] / df_fe["sqft"]
df_fe["bedrooms_x_sqft"] = df_fe["bedrooms"] * df_fe["sqft"]

# 3. Ordinal Encoding for ranked categorical features
education_order = [["High School", "Bachelor", "Master", "PhD"]]
ord_enc = OrdinalEncoder(categories=education_order)
df_fe[["education_encoded"]] = ord_enc.fit_transform(df_fe[["education"]])

# 4. One-Hot Encoding for nominal categorical features
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
city_encoded = ohe.fit_transform(df_fe[["city"]])
city_cols = ohe.get_feature_names_out(["city"])
city_df = pd.DataFrame(city_encoded, columns=city_cols, index=df_fe.index)

# Merge one-hot columns back into main DataFrame
df_fe = pd.concat([df_fe, city_df], axis=1)

# 5. Filter-based Feature Selection via SelectKBest
X_fe = df_fe.drop(columns=["target", "order_date", "education", "city"])
y_fe = df_fe["target"]

selector = SelectKBest(score_func=f_regression, k=min(10, X_fe.shape[1]))
X_selected = selector.fit_transform(X_fe, y_fe)
selected_feature_names = X_fe.columns[selector.get_support()].tolist()

print("Selected features:", selected_feature_names)
print("Final feature matrix shape:", X_selected.shape)


# ==============================================================================
# 5. MATHEMATICAL & STATISTICAL FOUNDATIONS FROM SCRATCH
# ==============================================================================

# ------------------------------------------------------------------------------
# 5.1 Central Tendency: Mean, Median & Mode with NumPy and Pandas
# ------------------------------------------------------------------------------
import numpy as np
import pandas as pd

# Basic numeric array
raw_nums = np.array([10, 20, 20, 30, 40, 50])

print("NumPy Mean:", np.mean(raw_nums))
print("NumPy Median:", np.median(raw_nums))
print("Pandas Mode:", pd.Series(raw_nums).mode().tolist())

# DataFrame example highlighting sensitivity to extreme outliers
df_stats = pd.DataFrame({
    "age": [22, 25, 25, 30, 35, 40, 80],
    "salary": [30000, 35000, 40000, 45000, 50000, 55000, 5000000]
})

print("\n--- Age Statistics ---")
print("Mean:", df_stats["age"].mean())
print("Median:", df_stats["age"].median())
print("Mode:", df_stats["age"].mode().tolist())

print("\n--- Salary Statistics (Outlier Effect) ---")
print("Mean (Pulled by $5M outlier):", df_stats["salary"].mean())
print("Median (Robust to $5M outlier):", df_stats["salary"].median())
print("Mode:", df_stats["salary"].mode().tolist())


# ------------------------------------------------------------------------------
# 5.2 Measures of Spread: Variance, Standard Deviation, Covariance & Correlation
# ------------------------------------------------------------------------------
import pandas as pd

df_study = pd.DataFrame({
    "study_hours": [1, 2, 3, 4, 5],
    "marks": [40, 50, 60, 70, 80],
    "sleep_hours": [8, 8, 7, 6, 6]
})

print("Variance (s²):\n", df_study.var())
print("\nStandard Deviation (s):\n", df_study.std())
print("\nCovariance Matrix:\n", df_study.cov())
print("\nCorrelation Matrix (Pearson r ∈ [-1, 1]):\n", df_study.corr())


# ------------------------------------------------------------------------------
# 5.3 Probability Foundations & Empirical Simulation
# ------------------------------------------------------------------------------
import numpy as np

# Basic theoretical probability: favorable / total
favorable = 3
total = 6
prob_a = favorable / total
print("Theoretical P(A):", prob_a)

# Complement rule: P(A') = 1 - P(A)
prob_not_a = 1 - prob_a
print("Complement P(not A):", prob_not_a)

# Joint probability for independent events: P(A ∩ B) = P(A) * P(B)
p_A = 0.50
p_B = 0.25
p_independent_joint = p_A * p_B
print("P(A ∩ B) [Independent]:", p_independent_joint)

# Conditional probability: P(A | B) = P(A ∩ B) / P(B)
p_A_and_B = 0.30
p_B_given = 0.50
p_A_given_B = p_A_and_B / p_B_given
print("P(A | B):", p_A_given_B)

# Empirical simulation (Law of Large Numbers)
coin_flips = np.random.choice(["Heads", "Tails"], size=10000)
empirical_heads_prob = np.sum(coin_flips == "Heads") / len(coin_flips)
print("Empirical P(Heads) over 10,000 trials:", empirical_heads_prob)


# ------------------------------------------------------------------------------
# 5.4 Bayes' Theorem in Practice: Medical Diagnostic Example
# ------------------------------------------------------------------------------
# Prior: Base rate of disease in population P(D)
prior_disease = 0.01

# Sensitivity (Likelihood): P(Positive | Disease)
sensitivity = 0.99

# False Positive Rate: P(Positive | No Disease)
false_positive_rate = 0.01

# Prior for no disease P(D')
prior_no_disease = 1.0 - prior_disease

# Total Evidence: Marginal probability of a positive test P(+)
prob_positive = (sensitivity * prior_disease) + (false_positive_rate * prior_no_disease)

# Posterior: P(Disease | Positive test) using Bayes' Theorem
posterior_disease = (sensitivity * prior_disease) / prob_positive

print("Total Probability of Positive Test P(+):", prob_positive)
print(f"Posterior Probability of Disease Given Positive Test P(D|+): {posterior_disease:.4f} ({posterior_disease * 100:.1f}%)")


# ==============================================================================
# 6. LINEAR ALGEBRA WITH NUMPY
# ==============================================================================

# ------------------------------------------------------------------------------
# 6.1 Scalars, Vectors, Matrices, Tensors & Arithmetic
# ------------------------------------------------------------------------------
import numpy as np

# Scalar (0D)
scalar_val = 5

# Vectors (1D)
vec_a = np.array([1, 2, 3])
vec_b = np.array([4, 5, 6])

# Matrices (2D)
mat_A = np.array([[1, 2], [3, 4]])
mat_B = np.array([[5, 6], [7, 8]])

# Tensor (3D)
tensor_3d = np.random.rand(2, 3, 4)

print("Vector shape:", vec_a.shape)
print("Matrix shape:", mat_A.shape)
print("Tensor shape:", tensor_3d.shape)

# Element-wise operations
print("Vector Addition:", vec_a + vec_b)
print("Scalar Multiplication:", 5 * vec_a)
print("Element-wise Product (*):", vec_a * vec_b)

# Dot Product (vector-vector inner product)
print("Dot product (a · b):", vec_a @ vec_b)

# Matrix Multiplication (@ operator)
print("Matrix Multiplication (A @ B):\n", mat_A @ mat_B)

# Transposition
print("Matrix Transpose (A.T):\n", mat_A.T)


# ------------------------------------------------------------------------------
# 6.2 Machine Learning Weighted Sum Prediction via Matrix Multiplication
# ------------------------------------------------------------------------------
# Features: 3 samples with 3 features each (e.g., experience, score1, score2)
features_matrix = np.array([
    [5, 90, 70],
    [3, 80, 60],
    [7, 95, 85]
])

# Learned weight vector
weights_vector = np.array([2.0, 0.5, 3.0])

# Compute predictions: y_hat = X @ w
linear_predictions = features_matrix @ weights_vector
print("Predictions from X @ w:", linear_predictions)


# ==============================================================================
# 7. CALCULUS & OPTIMIZATION FROM SCRATCH
# ==============================================================================

# ------------------------------------------------------------------------------
# 7.1 Analytical vs. Numerical Derivatives (Finite Differences)
# ------------------------------------------------------------------------------
def func_sq(x):
    return x ** 2

val_x = 3.0
print("Function value f(3):", func_sq(val_x))

# Analytical derivative: d/dx (x²) = 2x
analytical_deriv = 2 * val_x
print("Analytical Derivative:", analytical_deriv)

# Numerical derivative via forward finite difference
step_h = 1e-6
numerical_deriv = (func_sq(val_x + step_h) - func_sq(val_x)) / step_h
print("Numerical Derivative:", numerical_deriv)


# ------------------------------------------------------------------------------
# 7.2 Multivariable Partial Derivatives & Gradient Vector
# ------------------------------------------------------------------------------
# Function: f(x, y) = x² + y²
x_coord, y_coord = 3.0, 4.0

# Partial derivatives: ∂f/∂x = 2x, ∂f/∂y = 2y
df_dx = 2 * x_coord
df_dy = 2 * y_coord
grad_vec = np.array([df_dx, df_dy])

print("Gradient Vector [∂f/∂x, ∂f/∂y]:", grad_vec)


# ------------------------------------------------------------------------------
# 7.3 Chain Rule & ML Backpropagation Example
# ------------------------------------------------------------------------------
# Forward pass: z = w * x; a = z²; loss = (a - target)²
sample_x = 2.0
weight_w = 3.0
true_y = 10.0

# 1. Forward Pass
z_val = weight_w * sample_x
pred_a = z_val ** 2
loss_val = (pred_a - true_y) ** 2

# 2. Backward Pass via Chain Rule
dL_da = 2 * (pred_a - true_y)  # ∂Loss / ∂a
da_dz = 2 * z_val              # ∂a / ∂z
dz_dw = sample_x               # ∂z / ∂w

dL_dw = dL_da * da_dz * dz_dw  # ∂Loss / ∂w via Chain Rule

print("Forward Loss:", loss_val)
print("Gradient dL/dw:", dL_dw)


# ------------------------------------------------------------------------------
# 7.4 Linear Regression with Gradient Descent from Scratch
# ------------------------------------------------------------------------------
import numpy as np

# Training dataset: y = 2x
X_gd = np.array([1, 2, 3, 4, 5], dtype=float)
y_gd = np.array([2, 4, 6, 8, 10], dtype=float)

# Parameter initialization
param_w = 0.0
param_b = 0.0
lr = 0.01
epochs = 1000

for epoch in range(epochs):
    # 1. Forward pass
    y_pred_gd = param_w * X_gd + param_b

    # 2. Calculate error and MSE loss
    error_gd = y_pred_gd - y_gd
    loss_mse = np.mean(error_gd ** 2)

    # 3. Compute partial gradients
    dw = np.mean(2 * X_gd * error_gd)
    db = np.mean(2 * error_gd)

    # 4. Parameter update rule: θ ← θ - η * ∇L
    param_w -= lr * dw
    param_b -= lr * db

print(f"Scratch GD Results -> Weight: {param_w:.4f}, Bias: {param_b:.4f}, Final Loss: {loss_mse:.6f}")


# ------------------------------------------------------------------------------
# 7.5 Multi-Parameter Optimization Demonstrations
# ------------------------------------------------------------------------------
# 1D Quadratic minimization: L(w) = w²
opt_w = 5.0
alpha_lr = 0.1
for step in range(20):
    grad_w = 2 * opt_w
    opt_w -= alpha_lr * grad_w

print(f"Optimized 1D parameter w: {opt_w:.6f} (Minimum is 0.0)")

# 2D Quadratic minimization: L(w1, w2) = w1² + w2²
weights_2d = np.array([4.0, 3.0])
for step in range(20):
    grad_2d = 2 * weights_2d
    weights_2d -= alpha_lr * grad_2d

print(f"Optimized 2D weights: {weights_2d}")


# ==============================================================================
# 8. EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATION
# ==============================================================================

# ------------------------------------------------------------------------------
# 8.1 Univariate Distribution Visualization: Histograms & Box Plots
# ------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_viz = pd.DataFrame({
    "age": [21, 22, 23, 24, 25, 25, 26, 27, 28, 29, 30, 32, 35, 40, 55],
    "salary": [25000, 28000, 30000, 32000, 35000, 36000, 38000, 40000, 42000, 45000, 50000, 55000, 60000, 70000, 500000]
})

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.histplot(df_viz["salary"], bins=8, kde=True)
plt.title("Salary Distribution (Histogram + KDE)")

plt.subplot(1, 2, 2)
sns.boxplot(x=df_viz["salary"])
plt.title("Salary Box Plot (Highlighting Outlier)")
plt.tight_layout()
plt.close()  # Close plot to allow non-blocking execution in scripted runs


# ------------------------------------------------------------------------------
# 8.2 Outlier Detection & IQR Visualization Pipeline
# ------------------------------------------------------------------------------
target_feature = "salary"
q1 = df_viz[target_feature].quantile(0.25)
q2 = df_viz[target_feature].quantile(0.50)  # Median
q3 = df_viz[target_feature].quantile(0.75)
iqr_val = q3 - q1

lower_fence = q1 - 1.5 * iqr_val
upper_fence = q3 + 1.5 * iqr_val

outliers_detected = df_viz[(df_viz[target_feature] < lower_fence) | (df_viz[target_feature] > upper_fence)]
print(f"Q1: {q1}, Median: {q2}, Q3: {q3}, IQR: {iqr_val}")
print(f"Fences: [{lower_fence}, {upper_fence}]")
print("Detected Outliers:\n", outliers_detected)


# ------------------------------------------------------------------------------
# 8.3 Multivariate EDA Suite: Scatter, Line, Pair Plots & Heatmap
# ------------------------------------------------------------------------------
df_eda = pd.read_csv("data.csv")

# 1. Scatter Plot (Two numerical variables)
sns.scatterplot(data=df_eda, x="feature_1", y="feature_2", hue="category")
plt.title("Feature 1 vs Feature 2 Grouped by Category")
plt.close()

# 2. Line Plot (Temporal or ordered trends)
sns.lineplot(data=df_eda, x="time", y="value")
plt.title("Metric Trend Over Time")
plt.close()

# 3. Correlation Heatmap
corr_matrix = df_eda.select_dtypes(include="number").corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.close()

# 4. Bar & Count Plots for Categoricals
sns.barplot(data=df_eda, x="category", y="target")
plt.title("Average Target by Category")
plt.close()


# ==============================================================================
# 9. SUPERVISED LEARNING: REGRESSION MODELS & METRICS
# ==============================================================================

# ------------------------------------------------------------------------------
# 9.1 Simple Linear Regression with Scikit-Learn
# ------------------------------------------------------------------------------
import numpy as np
from sklearn.linear_model import LinearRegression

# Feature matrix must be 2D
X_simple_reg = np.array([[1000], [1200], [1500], [1800], [2000]])
y_simple_reg = np.array([30, 35, 45, 55, 60])

sk_lin_model = LinearRegression()
sk_lin_model.fit(X_simple_reg, y_simple_reg)

pred_val = sk_lin_model.predict([[1600]])
print("Predicted price for 1600 sqft:", pred_val[0])


# ------------------------------------------------------------------------------
# 9.2 Regression Evaluation Metrics: MAE, MSE, RMSE, R²
# ------------------------------------------------------------------------------
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X_eval_reg = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y_eval_reg = np.array([30, 40, 50, 60, 70, 80, 90, 100, 110, 120])

X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(X_eval_reg, y_eval_reg, test_size=0.2, random_state=42)

reg_eval_model = LinearRegression()
reg_eval_model.fit(X_tr_r, y_tr_r)
y_pred_r = reg_eval_model.predict(X_te_r)

mae = mean_absolute_error(y_te_r, y_pred_r)
mse = mean_squared_error(y_te_r, y_pred_r)
rmse = np.sqrt(mse)
r2 = r2_score(y_te_r, y_pred_r)

print(f"Regression Metrics -> MAE: {mae:.2f}, MSE: {mse:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}")


# ------------------------------------------------------------------------------
# 9.3 Polynomial Regression Pipeline with Non-linear Data
# ------------------------------------------------------------------------------
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline

np.random.seed(42)
weeks = np.linspace(1, 100, 200).reshape(-1, 1)
sales = 50 + 2.5 * weeks.ravel() - 0.02 * (weeks.ravel() ** 2) + np.random.normal(0, 5, size=200)

X_tr_poly, X_te_poly, y_tr_poly, y_te_poly = train_test_split(weeks, sales, test_size=0.2, random_state=42)

poly_pipe = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression())
])

poly_pipe.fit(X_tr_poly, y_tr_poly)
y_pred_poly = poly_pipe.predict(X_te_poly)

print(f"Polynomial Regression RMSE: {np.sqrt(mean_squared_error(y_te_poly, y_pred_poly)):.2f}")
print(f"Polynomial Regression R²: {r2_score(y_te_poly, y_pred_poly):.4f}")


# ------------------------------------------------------------------------------
# 9.4 Regularized Regression: Ridge (L2) & Adjusted R² Calculation
# ------------------------------------------------------------------------------
from sklearn.linear_model import Ridge, Lasso

ridge_pipe = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
    ("regressor", Ridge(alpha=1.0))
])

ridge_pipe.fit(X_tr_poly, y_tr_poly)
y_pred_ridge = ridge_pipe.predict(X_te_poly)

r2_ridge = r2_score(y_te_poly, y_pred_ridge)
n_samples = len(y_te_poly)
d_features = X_te_poly.shape[1]

# Adjusted R² formula: 1 - [(1 - R²)(n - 1) / (n - d - 1)]
adj_r2 = 1.0 - ((1.0 - r2_ridge) * (n_samples - 1) / (n_samples - d_features - 1))
print(f"Ridge R²: {r2_ridge:.4f}, Adjusted R²: {adj_r2:.4f}")


# ==============================================================================
# 10. SUPERVISED LEARNING: CLASSIFICATION MODELS & PIPELINES
# ==============================================================================

# ------------------------------------------------------------------------------
# 10.1 Simple Logistic Regression with Scikit-Learn
# ------------------------------------------------------------------------------
from sklearn.linear_model import LogisticRegression

X_log = np.array([[1], [2], [3], [4], [5], [6]])
y_log = np.array([0, 0, 0, 1, 1, 1])

clf_log = LogisticRegression()
clf_log.fit(X_log, y_log)

print("Class Prediction for 4.5:", clf_log.predict([[4.5]])[0])
print("Probabilities [P(0), P(1)]:", clf_log.predict_proba([[4.5]])[0])


# ------------------------------------------------------------------------------
# 10.2 Production Supervised Pipeline with ColumnTransformer
# ------------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df_clf = pd.read_csv("data.csv")
X_clf = df_clf.drop(columns=["target"])
y_clf = df_clf["target"]

num_cols = X_clf.select_dtypes(include=np.number).columns.tolist()
cat_cols = X_clf.select_dtypes(exclude=np.number).columns.tolist()

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

full_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

full_pipeline.fit(X_train_c, y_train_c)
print("Pipeline Test Accuracy:", full_pipeline.score(X_test_c, y_test_c))


# ------------------------------------------------------------------------------
# 10.3 Stratified Train/Val/Test Split & Stratified K-Fold Cross-Validation
# ------------------------------------------------------------------------------
from sklearn.model_selection import train_test_split, StratifiedKFold

X_strat = np.random.randn(1000, 10)
y_strat = np.random.choice([0, 1], size=1000, p=[0.8, 0.2])

# Split into 70% train and 30% temp
X_tr_s, X_tmp_s, y_tr_s, y_tmp_s = train_test_split(
    X_strat, y_strat, test_size=0.30, random_state=42, stratify=y_strat
)

# Split temp into 15% validation and 15% test
X_val_s, X_te_s, y_val_s, y_te_s = train_test_split(
    X_tmp_s, y_tmp_s, test_size=0.50, random_state=42, stratify=y_tmp_s
)

# Set up Stratified 5-Fold Cross-Validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(skf.split(X_tr_s, y_tr_s)):
    print(f"Fold {fold + 1}: Train samples={len(train_idx)}, Val samples={len(val_idx)}")


# ------------------------------------------------------------------------------
# 10.4 Handling Class Imbalance with SMOTE & Imbalanced-Learn Pipeline
# ------------------------------------------------------------------------------
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import classification_report

imb_pipe = ImbPipeline([
    ("scaler", StandardScaler()),
    ("smote", SMOTE(random_state=42)),
    ("model", LogisticRegression(max_iter=1000))
])

imb_pipe.fit(X_tr_s, y_tr_s)
y_pred_imb = imb_pipe.predict(X_te_s)
print("\nClassification Report with SMOTE Resampling:\n", classification_report(y_te_s, y_pred_imb))


# ------------------------------------------------------------------------------
# 10.5 Classical Classification Algorithm Benchmark Comparison
# ------------------------------------------------------------------------------
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

benchmark_models = {
    "KNN": Pipeline([("scaler", StandardScaler()), ("model", KNeighborsClassifier(n_neighbors=5))]),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM (RBF Kernel)": Pipeline([("scaler", StandardScaler()), ("model", SVC(kernel="rbf", C=1.0))]),
    "Gaussian Naive Bayes": GaussianNB()
}

print("\n--- Classification Benchmark ---")
for name, model in benchmark_models.items():
    model.fit(X_tr_s, y_tr_s)
    acc = model.score(X_te_s, y_te_s)
    print(f"{name:22s} Accuracy: {acc:.4f}")


# ==============================================================================
# 11. CLASSIFICATION METRICS & HYPERPARAMETER TUNING
# ==============================================================================

# ------------------------------------------------------------------------------
# 11.1 Full Metric Suite for Imbalanced Classification
# ------------------------------------------------------------------------------
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score
)

cm = confusion_matrix(y_te_s, y_pred_imb)
acc = accuracy_score(y_te_s, y_pred_imb)
prec = precision_score(y_te_s, y_pred_imb, zero_division=0)
rec = recall_score(y_te_s, y_pred_imb, zero_division=0)
f1 = f1_score(y_te_s, y_pred_imb, zero_division=0)

print("\nConfusion Matrix:\n", cm)
print(f"Accuracy: {acc:.4f}")
print(f"Precision (TP / (TP + FP)): {prec:.4f}")
print(f"Recall (TP / (TP + FN)): {rec:.4f}")
print(f"F1-Score: {f1:.4f}")


# ------------------------------------------------------------------------------
# 11.2 Leak-Proof Hyperparameter Tuning with RandomizedSearchCV
# ------------------------------------------------------------------------------
from sklearn.model_selection import RandomizedSearchCV
from sklearn.impute import SimpleImputer

# Build modular ColumnTransformer
num_pre = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pre = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

comp_preprocessor = ColumnTransformer([
    ("num", num_pre, ["age", "salary"]),
    ("cat", cat_pre, ["city", "education"])
])

search_pipe = Pipeline([
    ("preprocessor", comp_preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])

# Define hyperparameter exploration distributions
param_dist = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [3, 5, 10, None],
    "classifier__min_samples_split": [2, 5, 10],
    "classifier__class_weight": ["balanced", "balanced_subsample"]
}

# Tune strictly on training set using cross-validation
random_search = RandomizedSearchCV(
    estimator=search_pipe,
    param_distributions=param_dist,
    n_iter=5,
    cv=3,
    scoring="roc_auc",
    random_state=42
)

# Fit on training split
random_search.fit(X_train_c, y_train_c)
print("Best Hyperparameters:", random_search.best_params_)
print("Best CV ROC-AUC:", random_search.best_score_)


# ------------------------------------------------------------------------------
# 11.3 Multi-Layer Perceptron (MLPClassifier) with Early Stopping Pipeline
# ------------------------------------------------------------------------------
from sklearn.neural_network import MLPClassifier

mlp_model = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    max_iter=500,
    early_stopping=True,          # Halts training when validation loss stops improving
    validation_fraction=0.1,     # Reserves 10% of training data for validation monitoring
    n_iter_no_change=10,         # Patience: epochs to wait before stopping
    tol=1e-4,
    random_state=42
)

mlp_pipe = Pipeline([
    ("preprocessor", comp_preprocessor),
    ("classifier", mlp_model)
])

mlp_pipe.fit(X_train_c, y_train_c)
print(f"MLP Early Stopping triggered at epoch: {mlp_pipe.named_steps['classifier'].n_iter_}")


# ==============================================================================
# 12. UNSUPERVISED LEARNING: CLUSTERING
# ==============================================================================

# ------------------------------------------------------------------------------
# 12.1 Simple K-Means Clustering on Synthetic Blobs
# ------------------------------------------------------------------------------
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X_blobs, _ = make_blobs(n_samples=300, n_features=2, centers=3, cluster_std=1.0, random_state=42)

kmeans_simple = KMeans(n_clusters=3, n_init=10, random_state=42)
cluster_labels_simple = kmeans_simple.fit_predict(X_blobs)

print("Cluster Centers:\n", kmeans_simple.cluster_centers_)
print("Inertia (Within-Cluster Sum of Squares):", kmeans_simple.inertia_)
print("Silhouette Score:", silhouette_score(X_blobs, cluster_labels_simple))


# ------------------------------------------------------------------------------
# 12.2 Finding Optimal K via the Elbow Method
# ------------------------------------------------------------------------------
inertias = []
k_range = range(2, 9)

for k in k_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X_blobs)
    inertias.append(km.inertia_)

plt.figure(figsize=(6, 3))
plt.plot(k_range, inertias, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia (WCSS)")
plt.title("Elbow Method for Optimal K")
plt.close()


# ------------------------------------------------------------------------------
# 12.3 Agglomerative Hierarchical Clustering & Dendrogram with SciPy
# ------------------------------------------------------------------------------
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram

scaler_agg = StandardScaler()
X_blobs_scaled = scaler_agg.fit_transform(X_blobs)

# Generate linkage matrix using Ward's minimum variance method
linkage_matrix = linkage(X_blobs_scaled, method="ward")

plt.figure(figsize=(8, 4))
dendrogram(linkage_matrix, truncate_mode="lastp", p=12)
plt.title("Hierarchical Clustering Dendrogram (Truncated)")
plt.xlabel("Cluster Size")
plt.ylabel("Ward Distance")
plt.close()

# Fit Agglomerative Clustering
agg_model = AgglomerativeClustering(n_clusters=3, linkage="ward")
agg_labels = agg_model.fit_predict(X_blobs_scaled)


# ------------------------------------------------------------------------------
# 12.4 Density-Based Clustering: DBSCAN & OPTICS
# ------------------------------------------------------------------------------
from sklearn.cluster import DBSCAN, OPTICS

# DBSCAN with epsilon radius and minimum sample threshold
dbscan_model = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan_model.fit_predict(X_blobs_scaled)

n_clusters_db = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise_db = list(dbscan_labels).count(-1)
print(f"DBSCAN -> Discovered Clusters: {n_clusters_db}, Noise points: {n_noise_db}")

# OPTICS (Density clustering across multiple scales)
optics_model = OPTICS(min_samples=5, xi=0.05)
optics_labels = optics_model.fit_predict(X_blobs_scaled)
print("OPTICS labels unique:", set(optics_labels))


# ------------------------------------------------------------------------------
# 12.5 Gaussian Mixture Models (GMM) with BIC Model Selection
# ------------------------------------------------------------------------------
from sklearn.mixture import GaussianMixture

bic_scores = {}
for k in range(1, 6):
    gmm = GaussianMixture(n_components=k, covariance_type="full", random_state=42)
    gmm.fit(X_blobs_scaled)
    bic_scores[k] = gmm.bic(X_blobs_scaled)

best_k_gmm = min(bic_scores, key=bic_scores.get)
print(f"Optimal GMM Components by BIC: {best_k_gmm}")

final_gmm = GaussianMixture(n_components=best_k_gmm, covariance_type="full", random_state=42)
gmm_labels = final_gmm.fit_predict(X_blobs_scaled)
gmm_probs = final_gmm.predict_proba(X_blobs_scaled)

print("First sample soft probabilities:", gmm_probs[0])


# ------------------------------------------------------------------------------
# 12.6 Scalable & Mode-Seeking Clustering: BIRCH & Mean Shift
# ------------------------------------------------------------------------------
from sklearn.cluster import Birch, MeanShift, estimate_bandwidth

# 1. BIRCH (CF Tree Compression)
birch_model = Birch(threshold=0.5, branching_factor=50, n_clusters=3)
birch_labels = birch_model.fit_predict(X_blobs_scaled)
print(f"BIRCH subclusters generated: {len(birch_model.subcluster_centers_)}")

# 2. Mean Shift with automatic bandwidth estimation
bw = estimate_bandwidth(X_blobs_scaled, quantile=0.2)
ms_model = MeanShift(bandwidth=bw, bin_seeding=True)
ms_labels = ms_model.fit_predict(X_blobs_scaled)
print(f"Mean Shift automatically discovered {len(ms_model.cluster_centers_)} cluster centers.")


# ==============================================================================
# 13. UNSUPERVISED LEARNING: DIMENSIONALITY REDUCTION
# ==============================================================================

# ------------------------------------------------------------------------------
# 13.1 Principal Component Analysis (PCA) & Variance Analysis
# ------------------------------------------------------------------------------
from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)  # Retain 95% of cumulative variance
X_pca_reduced = pca.fit_transform(X_blobs_scaled)

print("Original Features:", X_blobs_scaled.shape[1])
print("Retained Features:", pca.n_components_)
print("Explained Variance Ratio per PC:", pca.explained_variance_ratio_)
print("Cumulative Variance:", np.sum(pca.explained_variance_ratio_))


# ------------------------------------------------------------------------------
# 13.2 PCA from Scratch via NumPy Eigendecomposition
# ------------------------------------------------------------------------------
# 1. Zero-center the data
X_centered = X_blobs_scaled - np.mean(X_blobs_scaled, axis=0)

# 2. Compute sample covariance matrix
cov_matrix = np.cov(X_centered, rowvar=False)

# 3. Compute eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

# 4. Sort in descending order
sort_indices = np.argsort(eigenvalues)[::-1]
eigenvalues_sorted = eigenvalues[sort_indices]
eigenvectors_sorted = eigenvectors[:, sort_indices]

# 5. Project data onto the first principal component
X_scratch_pca = X_centered @ eigenvectors_sorted[:, :1]
print("Scratch PCA Projected Shape:", X_scratch_pca.shape)


# ------------------------------------------------------------------------------
# 13.3 Dimensionality Reduction Benchmark: PCA, SVD, LDA, t-SNE & UMAP
# ------------------------------------------------------------------------------
from scipy.sparse import csr_matrix
from sklearn.datasets import load_digits, load_iris
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import TSNE
import umap

digits = load_digits()
X_dig = digits.data
y_dig = digits.target
X_dig_scaled = StandardScaler().fit_transform(X_dig)

# 1. PCA
pca_dig = PCA(n_components=2).fit_transform(X_dig_scaled)

# 2. Truncated SVD (Ideal for sparse matrices without centering)
svd_dig = TruncatedSVD(n_components=2).fit_transform(csr_matrix(X_dig))

# 3. LDA (Supervised: uses target labels to maximize class separation)
lda_dig = LinearDiscriminantAnalysis(n_components=2).fit_transform(X_dig, y_dig)

# 4. t-SNE (Non-linear manifold visualization; preserves local neighborhoods)
tsne_dig = TSNE(n_components=2, perplexity=30, random_state=42).fit_transform(X_dig_scaled[:500])

# 5. UMAP (Non-linear; preserves both local and global structure; supports transform on new data)
umap_dig = umap.UMAP(n_components=2, random_state=42).fit_transform(X_dig_scaled[:500])

print(f"Benchmark Shapes -> PCA: {pca_dig.shape}, SVD: {svd_dig.shape}, LDA: {lda_dig.shape}, t-SNE: {tsne_dig.shape}, UMAP: {umap_dig.shape}")


# ==============================================================================
# 14. UNSUPERVISED LEARNING: ASSOCIATION RULE MINING
# ==============================================================================

# ------------------------------------------------------------------------------
# 14.1 Apriori & FP-Growth with mlxtend
# ------------------------------------------------------------------------------
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

# One-hot encoded transaction database
transactions_df = pd.DataFrame({
    "Milk":   [1, 1, 0, 1, 1, 0, 1, 0],
    "Bread":  [1, 1, 1, 0, 1, 1, 1, 1],
    "Butter": [1, 0, 1, 0, 1, 0, 1, 0],
    "Beer":   [0, 1, 1, 1, 0, 1, 0, 1]
})

# 1. Apriori Algorithm (Frequent itemsets with minimum support threshold)
apriori_itemsets = apriori(transactions_df, min_support=0.30, use_colnames=True)

# 2. FP-Growth Algorithm (Memory-efficient pattern growth without candidate generation)
fpgrowth_itemsets = fpgrowth(transactions_df, min_support=0.30, use_colnames=True)

# 3. Generate Association Rules evaluated by Lift
rules_df = association_rules(fpgrowth_itemsets, metric="lift", min_threshold=1.0)
rules_sorted = rules_df[["antecedents", "consequents", "support", "confidence", "lift"]].sort_values(by="lift", ascending=False)

print("\n--- Discovered Association Rules ---")
print(rules_sorted.head())

# Filter strong actionable rules (Confidence >= 60%, Lift > 1.0)
strong_rules = rules_sorted[(rules_sorted["confidence"] >= 0.60) & (rules_sorted["lift"] > 1.0)]
print("\nStrong Rules (Confidence >= 0.60):\n", strong_rules)


# ==============================================================================
# 15. UNSUPERVISED LEARNING: TOPIC MODELING
# ==============================================================================

# ------------------------------------------------------------------------------
# 15.1 Topic Modeling Benchmark: LDA (Probabilistic) vs. NMF (Matrix Factorization)
# ------------------------------------------------------------------------------
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

corpus_docs = [
    "Cybersecurity breaches exploit software network vulnerabilities",
    "Bank credit card fraud detection using machine learning algorithms",
    "Network intrusion detection systems monitor suspicious IP traffic",
    "Financial loan risk models predict credit default probability",
    "Deep learning neural networks process high dimensional image features"
] * 10

# --------------------------------------------------
# Latent Dirichlet Allocation (LDA)
# --------------------------------------------------
# Step 1: Compute raw count term frequencies
count_vec = CountVectorizer(stop_words="english")
X_count_matrix = count_vec.fit_transform(corpus_docs)

# Step 2: Fit Bayesian generative LDA model
lda_model = LatentDirichletAllocation(n_components=2, random_state=42)
lda_model.fit(X_count_matrix)

# --------------------------------------------------
# Non-Negative Matrix Factorization (NMF)
# --------------------------------------------------
# Step 1: Compute TF-IDF matrix
tfidf_vec = TfidfVectorizer(stop_words="english")
X_tfidf_matrix = tfidf_vec.fit_transform(corpus_docs)

# Step 2: Fit additive matrix factorization: V ≈ W * H
nmf_model = NMF(n_components=2, init="nndsvda", random_state=42)
W_matrix = nmf_model.fit_transform(X_tfidf_matrix)  # Documents x Topics
H_matrix = nmf_model.components_                    # Topics x Vocabulary words

print("\n--- LDA Extracted Topics ---")
count_vocab = count_vec.get_feature_names_out()
for idx, topic in enumerate(lda_model.components_):
    top_words = [count_vocab[i] for i in topic.argsort()[:-6:-1]]
    print(f"Topic {idx + 1}: {', '.join(top_words)}")

print("\n--- NMF Extracted Topics ---")
tfidf_vocab = tfidf_vec.get_feature_names_out()
for idx, topic in enumerate(H_matrix):
    top_words = [tfidf_vocab[i] for i in topic.argsort()[:-6:-1]]
    print(f"Topic {idx + 1}: {', '.join(top_words)}")

print(f"\nMatrix Shapes -> Document-Term: {X_count_matrix.shape}, NMF W: {W_matrix.shape}, NMF H: {H_matrix.shape}")


# ==============================================================================
# 16. BIAS-VARIANCE DIAGNOSIS & LEARNING CURVES
# ==============================================================================
print("\n" + "=" * 80)
print("16. BIAS-VARIANCE DIAGNOSIS & LEARNING CURVES")
print("=" * 80)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import learning_curve

# Generate synthetic binary classification dataset
X_bv, y_bv = make_classification(
    n_samples=1200,
    n_features=20,
    n_informative=12,
    n_redundant=4,
    random_state=42
)

def evaluate_learning_curve(model, X, y, model_name="Model", cv_folds=5):
    """
    Computes and analyzes training vs. validation learning curves across
    increasing training sample sizes to diagnose High Bias vs. High Variance.
    """
    train_sizes, train_scores, val_scores = learning_curve(
        estimator=model,
        X=X,
        y=y,
        train_sizes=np.linspace(0.1, 1.0, 6),
        cv=cv_folds,
        scoring="accuracy",
        n_jobs=-1,
        random_state=42
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    print(f"\n--- Learning Curve Diagnostics: {model_name} ---")
    print(f"{'Train Size':>12} | {'Train Acc (Mean +/- Std)':>24} | {'Val Acc (Mean +/- Std)':>24} | {'Generalization Gap':>18}")
    print("-" * 86)
    for n, t_m, t_s, v_m, v_s in zip(train_sizes, train_mean, train_std, val_mean, val_std):
        gap = t_m - v_m
        print(f"{n:>12} | {t_m:6.3f} +/- {t_s:5.3f}           | {v_m:6.3f} +/- {v_s:5.3f}           | {gap:14.3f}")

    # Automated Diagnostic Assessment
    final_gap = train_mean[-1] - val_mean[-1]
    final_train = train_mean[-1]
    final_val = val_mean[-1]

    if final_train < 0.75 and final_val < 0.75:
        diagnosis = "HIGH BIAS (Underfitting) -> Both training and validation accuracy are low. Add model capacity or features!"
    elif final_gap > 0.10:
        diagnosis = "HIGH VARIANCE (Overfitting) -> Large generalization gap. Add data, regularize, or prune model complexity!"
    else:
        diagnosis = "WELL-BALANCED (Optimal Tradeoff) -> Model generalizes well with minimal overfitting gap."

    print(f"Diagnostic Conclusion: {diagnosis}")
    return train_sizes, train_mean, val_mean

# 1. High Bias Model Candidate: Underparameterized Logistic Regression with heavy L2 penalty
model_underfit = LogisticRegression(C=0.001, max_iter=200, random_state=42)
evaluate_learning_curve(model_underfit, X_bv, y_bv, model_name="Underfit Logistic Regression (C=0.001)")

# 2. High Variance Model Candidate: Unpruned Deep Decision Tree
model_overfit = DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=42)
evaluate_learning_curve(model_overfit, X_bv, y_bv, model_name="Overfit Decision Tree (Unpruned)")


# ==============================================================================
# 17. ADVANCED ENSEMBLE LEARNING: BOOSTING, STACKING & VOTING
# ==============================================================================
print("\n" + "=" * 80)
print("17. ADVANCED ENSEMBLE LEARNING (BOOSTING, STACKING & VOTING)")
print("=" * 80)

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier
)
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from sklearn.model_selection import train_test_split
import pandas as pd

# Split dataset into train and test sets
X_train_ens, X_test_ens, y_train_ens, y_test_ens = train_test_split(
    X_bv, y_bv, test_size=0.25, random_state=42, stratify=y_bv
)

# ------------------------------------------------------------------------------
# 17.1 AdaBoost (Adaptive Boosting with Decision Stumps)
# ------------------------------------------------------------------------------
adaboost_clf = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=100,
    learning_rate=0.8,
    random_state=42
)
adaboost_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.2 Scikit-Learn Gradient Boosting Machine (GBM)
# ------------------------------------------------------------------------------
gbm_clf = GradientBoostingClassifier(
    n_estimators=150,
    learning_rate=0.08,
    max_depth=4,
    subsample=0.8,
    random_state=42
)
gbm_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.3 XGBoost (eXtreme Gradient Boosting with 2nd-order Taylor & Regularization)
# ------------------------------------------------------------------------------
xgb_clf = XGBClassifier(
    n_estimators=150,
    learning_rate=0.08,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,    # L1 regularization
    reg_lambda=1.0,   # L2 regularization
    eval_metric="logloss",
    random_state=42
)
xgb_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.4 LightGBM (Leaf-Wise Growth & Histogram Binning)
# ------------------------------------------------------------------------------
lgbm_clf = LGBMClassifier(
    n_estimators=150,
    learning_rate=0.08,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    verbose=-1,
    random_state=42
)
lgbm_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.5 CatBoost (Symmetric Oblivious Trees & Ordered Boosting)
# ------------------------------------------------------------------------------
catboost_clf = CatBoostClassifier(
    iterations=150,
    learning_rate=0.08,
    depth=4,
    verbose=0,
    random_state=42
)
catboost_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.6 Stacking Classifier (Meta-Learner on Out-Of-Fold Predictions)
# ------------------------------------------------------------------------------
base_estimators = [
    ("rf", RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)),
    ("xgb", XGBClassifier(n_estimators=100, max_depth=4, eval_metric="logloss", random_state=42)),
    ("lgb", LGBMClassifier(n_estimators=100, num_leaves=25, verbose=-1, random_state=42))
]
stacking_clf = StackingClassifier(
    estimators=base_estimators,
    final_estimator=LogisticRegression(C=1.0, max_iter=200),
    cv=5,
    n_jobs=-1
)
stacking_clf.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 17.7 Soft Voting Classifier (Weighted Ensemble Probability Averaging)
# ------------------------------------------------------------------------------
voting_clf = VotingClassifier(
    estimators=[
        ("xgb", xgb_clf),
        ("lgb", lgbm_clf),
        ("cat", catboost_clf)
    ],
    voting="soft",
    weights=[1.0, 1.2, 1.2]
)
voting_clf.fit(X_train_ens, y_train_ens)

# Benchmark Comparison
all_ensembles = {
    "AdaBoost": adaboost_clf,
    "GradientBoosting (GBM)": gbm_clf,
    "XGBoost": xgb_clf,
    "LightGBM": lgbm_clf,
    "CatBoost": catboost_clf,
    "Stacking (Meta-Learner)": stacking_clf,
    "Soft Voting Ensemble": voting_clf
}

print(f"{'Ensemble Model':>26} | {'Test Accuracy':>14} | {'Test ROC-AUC':>14}")
print("-" * 60)
for name, clf in all_ensembles.items():
    preds = clf.predict(X_test_ens)
    probs = clf.predict_proba(X_test_ens)[:, 1]
    acc = accuracy_score(y_test_ens, preds)
    auc = roc_auc_score(y_test_ens, probs)
    print(f"{name:>26} | {acc:14.4f} | {auc:14.4f}")


# ==============================================================================
# 18. ADVANCED FEATURE ENGINEERING & TARGET ENCODING
# ==============================================================================
print("\n" + "=" * 80)
print("18. ADVANCED FEATURE ENGINEERING (TARGET ENCODING, POWER TRANSFORMS, BINNING)")
print("=" * 80)

from sklearn.preprocessing import TargetEncoder, PowerTransformer, KBinsDiscretizer

# Create synthetic dataset with high-cardinality categories and skewed numerical features
np.random.seed(42)
n_rows = 1000

categories = ["City_" + str(np.random.choice(["NYC", "LA", "CHI", "MIA", "HOU", "PHX", "SEA", "DEN"], p=[0.3, 0.25, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02])) for _ in range(n_rows)]
skewed_income = np.random.exponential(scale=50000, size=n_rows) + 15000  # Highly right-skewed
skewed_balance = np.random.lognormal(mean=7, sigma=1.2, size=n_rows)     # Heavy-tailed

# Generate target influenced by city and income
target_prob = (skewed_income > 60000).astype(float) * 0.4 + (np.array(categories) == "City_NYC").astype(float) * 0.3
target_y = (np.random.rand(n_rows) < target_prob).astype(int)

df_fe = pd.DataFrame({
    "city": categories,
    "income": skewed_income,
    "balance": skewed_balance
})

X_train_fe, X_test_fe, y_train_fe, y_test_fe = train_test_split(
    df_fe, target_y, test_size=0.25, random_state=42
)

# ------------------------------------------------------------------------------
# 18.1 Smoothed Out-of-Fold Target Encoding (Scikit-Learn 1.3+)
# ------------------------------------------------------------------------------
# TargetEncoder uses internal cross-validation and m-estimate smoothing to prevent target leakage
target_enc = TargetEncoder(smooth="auto", cv=5)
encoded_city_train = target_enc.fit_transform(X_train_fe[["city"]], y_train_fe)
encoded_city_test = target_enc.transform(X_test_fe[["city"]])

print(f"Target Encoding Sample (Train):")
sample_preview = pd.DataFrame({
    "Original City": X_train_fe["city"].iloc[:6].values,
    "Target Encoded Value": encoded_city_train[:6, 0]
})
print(sample_preview.to_string(index=False))

# ------------------------------------------------------------------------------
# 18.2 Power Transformations: Box-Cox & Yeo-Johnson
# ------------------------------------------------------------------------------
# Yeo-Johnson handles zero and negative numbers; Box-Cox requires strictly positive
pt_yeo = PowerTransformer(method="yeo-johnson", standardize=True)
income_transformed = pt_yeo.fit_transform(X_train_fe[["income"]])

print(f"\nPower Transformation Skewness Correction:")
print(f"  Income Skewness Before Transformation: {pd.Series(X_train_fe['income']).skew():.4f}")
print(f"  Income Skewness After Yeo-Johnson:     {pd.Series(income_transformed[:, 0]).skew():.4f}")

# ------------------------------------------------------------------------------
# 18.3 Quantile Discretization (KBinsDiscretizer)
# ------------------------------------------------------------------------------
discretizer = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="quantile", random_state=42)
balance_binned = discretizer.fit_transform(X_train_fe[["balance"]])

print(f"\nQuantile Discretization Bin Edges for 'balance':")
for idx, edge in enumerate(discretizer.bin_edges_[0]):
    print(f"  Bin Boundary {idx}: {edge:,.2f}")


# ==============================================================================
# 19. MODERN HYPERPARAMETER OPTIMIZATION: OPTUNA & BAYESIAN OPTIMIZATION
# ==============================================================================
print("\n" + "=" * 80)
print("19. MODERN HYPERPARAMETER OPTIMIZATION (OPTUNA & BAYESIAN TPE)")
print("=" * 80)

import optuna
from optuna.samplers import TPESampler
from optuna.pruners import MedianPruner

# Suppress verbose Optuna logging for clean console output
optuna.logging.set_verbosity(optuna.logging.WARNING)

def objective(trial):
    """
    Optuna objective function for tuning LightGBM with Bayesian TPE.
    Defines search space and reports intermediate cross-validation scores.
    """
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 200),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 15, 63),
        "max_depth": trial.suggest_int("max_depth", 3, 8),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
        "verbose": -1,
        "random_state": 42
    }

    # Evaluate candidate using 3-fold cross validation
    from sklearn.model_selection import StratifiedKFold
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    auc_scores = []

    for step, (tr_idx, val_idx) in enumerate(skf.split(X_train_ens, y_train_ens)):
        X_tr, y_tr = X_train_ens[tr_idx], y_train_ens[tr_idx]
        X_va, y_va = X_train_ens[val_idx], y_train_ens[val_idx]

        clf = LGBMClassifier(**params)
        clf.fit(X_tr, y_tr)
        val_probs = clf.predict_proba(X_va)[:, 1]
        step_auc = roc_auc_score(y_va, val_probs)
        auc_scores.append(step_auc)

        # Report intermediate metric for automated pruning
        trial.report(step_auc, step=step)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return np.mean(auc_scores)

# Initialize Optuna Study with TPE (Tree-structured Parzen Estimator) and Median Pruner
study = optuna.create_study(
    direction="maximize",
    sampler=TPESampler(seed=42),
    pruner=MedianPruner(n_startup_trials=3, n_warmup_steps=1)
)

print("Starting Optuna Bayesian Hyperparameter Optimization (15 Trials)...")
study.optimize(objective, n_trials=15, show_progress_bar=False)

print(f"\nOptimization Finished!")
print(f"Best Trial Number:      {study.best_trial.number}")
print(f"Best Mean CV ROC-AUC:   {study.best_value:.4f}")
print("Best Hyperparameters:")
for param, val in study.best_params.items():
    if isinstance(val, float):
        print(f"  {param:<20}: {val:.5f}")
    else:
        print(f"  {param:<20}: {val}")


# ==============================================================================
# 20. MACHINE LEARNING EXPERIMENT TRACKING: MLFLOW
# ==============================================================================
print("\n" + "=" * 80)
print("20. MACHINE LEARNING EXPERIMENT TRACKING (MLFLOW ARCHITECTURE)")
print("=" * 80)

try:
    import mlflow
    import mlflow.sklearn

    mlflow.set_experiment("Tabular_Ensemble_Benchmark")
    with mlflow.start_run(run_name="LGBM_Optuna_Best_Trial"):
        # Log Best Hyperparameters
        for param, val in study.best_params.items():
            mlflow.log_param(param, val)

        # Train and log final model
        best_lgbm = LGBMClassifier(**study.best_params, verbose=-1, random_state=42)
        best_lgbm.fit(X_train_ens, y_train_ens)

        test_preds = best_lgbm.predict(X_test_ens)
        test_probs = best_lgbm.predict_proba(X_test_ens)[:, 1]

        # Log Evaluation Metrics
        mlflow.log_metric("test_accuracy", accuracy_score(y_test_ens, test_preds))
        mlflow.log_metric("test_roc_auc", roc_auc_score(y_test_ens, test_probs))

        # Log Model Artifact
        mlflow.sklearn.log_model(best_lgbm, artifact_path="model")
        print("Successfully logged run and artifacts to active MLflow Tracking Server.")

except ImportError:
    print("[NOTE] 'mlflow' is not installed in the active environment.")
    print("Standard Production MLflow Code Pattern demonstrated below:")
    code_snippet = """
    import mlflow
    import mlflow.sklearn

    mlflow.set_experiment("Churn_Prediction_Production")
    with mlflow.start_run(run_name="Champion_Model_v1"):
        # 1. Log parameters
        mlflow.log_param("learning_rate", 0.05)
        mlflow.log_param("max_depth", 5)

        # 2. Train model and evaluate
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

        # 3. Log metrics over time / iterations
        mlflow.log_metric("test_accuracy", score)

        # 4. Log serialized model artifact
        mlflow.sklearn.log_model(model, artifact_path="model")

    # To inspect runs visually in the browser:
    # Run command: mlflow ui --port 5000
    """
    print(code_snippet)


# ==============================================================================
# 21. MODEL INTERPRETABILITY & EXPLAINABILITY (XAI)
# ==============================================================================
print("\n" + "=" * 80)
print("21. MODEL INTERPRETABILITY & EXPLAINABILITY (PERMUTATION IMPORTANCE & SHAP)")
print("=" * 80)

from sklearn.inspection import permutation_importance, PartialDependenceDisplay

# Train interpretable Random Forest baseline
rf_explainer_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_explainer_model.fit(X_train_ens, y_train_ens)

# ------------------------------------------------------------------------------
# 21.1 Permutation Feature Importance (Unbiased Validation Importance)
# ------------------------------------------------------------------------------
# Computed on unseen TEST data to measure true drop in performance upon feature corruption
perm_importance = permutation_importance(
    rf_explainer_model,
    X_test_ens,
    y_test_ens,
    n_repeats=10,
    scoring="roc_auc",
    random_state=42
)

# Compare MDI (Gini Importance) vs. Permutation Importance
print("\nTop 5 Most Important Features Comparison:")
print(f"{'Feature Index':>14} | {'MDI (Gini Importance)':>24} | {'Permutation Score Drop':>24}")
print("-" * 68)

sorted_perm_indices = perm_importance.importances_mean.argsort()[::-1][:5]
for idx in sorted_perm_indices:
    mdi = rf_explainer_model.feature_importances_[idx]
    perm_drop = perm_importance.importances_mean[idx]
    perm_std = perm_importance.importances_std[idx]
    print(f"Feature {idx:>6} | {mdi:24.4f} | {perm_drop:14.4f} +/- {perm_std:.4f}")

# ------------------------------------------------------------------------------
# 21.2 SHAP (SHapley Additive exPlanations)
# ------------------------------------------------------------------------------
try:
    import shap
    explainer = shap.TreeExplainer(rf_explainer_model)
    shap_values = explainer.shap_values(X_test_ens[:100])

    print("\n[SHAP Analysis Successful]")
    print(f"SHAP Values Array Shape: {np.array(shap_values).shape}")
    print("Mean Absolute SHAP Value (Top 3 Features):")
    mean_abs_shap = np.mean(np.abs(shap_values[1]), axis=0)
    top_shap_idx = mean_abs_shap.argsort()[::-1][:3]
    for rank, idx in enumerate(top_shap_idx, 1):
        print(f"  Rank {rank}: Feature {idx} -> Mean |SHAP| = {mean_abs_shap[idx]:.4f}")

except ImportError:
    print("\n[NOTE] 'shap' is not installed in the active environment (pip install shap).")
    print("Standard Production SHAP Code Pattern:")
    shap_snippet = """
    import shap
    # 1. Initialize TreeExplainer for tree ensembles (Random Forest, XGBoost, LightGBM)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # 2. Global Feature Importance Summary (Beeswarm Plot)
    shap.summary_plot(shap_values, X_test)

    # 3. Local Single-Prediction Explanation (Waterfall Plot)
    shap.plots.waterfall(shap_values[0])
    """
    print(shap_snippet)


# ==============================================================================
# 22. SEMI-SUPERVISED LEARNING & SELF-TRAINING
# ==============================================================================
print("\n" + "=" * 80)
print("22. SEMI-SUPERVISED LEARNING (PSEUDO-LABELING WITH SELFTRAININGCLASSIFIER)")
print("=" * 80)

from sklearn.semi_supervised import SelfTrainingClassifier, LabelSpreading

# Simulate scenario: 90% of training data is UNLABELED (marked as -1)
rng = np.random.RandomState(42)
y_train_semi = np.copy(y_train_ens)

unlabeled_fraction = 0.85
unlabeled_mask = rng.rand(len(y_train_semi)) < unlabeled_fraction
y_train_semi[unlabeled_mask] = -1

n_labeled = np.sum(y_train_semi != -1)
n_unlabeled = np.sum(y_train_semi == -1)
print(f"Semi-Supervised Dataset Distribution:")
print(f"  Total Training Samples: {len(y_train_semi)}")
print(f"  Labeled Samples:        {n_labeled} ({n_labeled / len(y_train_semi):.1%})")
print(f"  Unlabeled Samples (-1): {n_unlabeled} ({n_unlabeled / len(y_train_semi):.1%})")

# 1. Baseline: Train Supervised Classifier ONLY on the 15% labeled instances
X_labeled_only = X_train_ens[y_train_semi != -1]
y_labeled_only = y_train_semi[y_train_semi != -1]

baseline_clf = LogisticRegression(max_iter=300, random_state=42)
baseline_clf.fit(X_labeled_only, y_labeled_only)
baseline_test_acc = baseline_clf.score(X_test_ens, y_test_ens)

# 2. Self-Training Classifier: Pseudo-labels confident unlabeled samples (Threshold = 0.80)
self_training_clf = SelfTrainingClassifier(
    estimator=LogisticRegression(max_iter=300, random_state=42),
    threshold=0.80,
    criterion="threshold",
    max_iter=10,
    verbose=False
)
self_training_clf.fit(X_train_ens, y_train_semi)
self_training_test_acc = self_training_clf.score(X_test_ens, y_test_ens)

# 3. Label Spreading: Graph-based diffusion using RBF kernel
label_spreading_clf = LabelSpreading(kernel="rbf", alpha=0.2, max_iter=30)
label_spreading_clf.fit(X_train_ens, y_train_semi)
label_spreading_test_acc = label_spreading_clf.score(X_test_ens, y_test_ens)

print(f"\n--- Semi-Supervised Performance Comparison on Unseen Test Set ---")
print(f"  Supervised Baseline (15% labeled data only): {baseline_test_acc:.4f}")
print(f"  SelfTrainingClassifier (Pseudo-Labeling):     {self_training_test_acc:.4f} (+{self_training_test_acc - baseline_test_acc:+.4f})")
print(f"  LabelSpreading (Graph Laplacian Diffusion):   {label_spreading_test_acc:.4f} (+{label_spreading_test_acc - baseline_test_acc:+.4f})")


# ==============================================================================
# 23. END-TO-END CAPSTONE PRODUCTION PIPELINE: CUSTOMER CHURN PREDICTION
# ==============================================================================
print("\n" + "=" * 80)
print("23. END-TO-END CAPSTONE PRODUCTION PIPELINE (CUSTOMER CHURN)")
print("=" * 80)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, average_precision_score, brier_score_loss

# ------------------------------------------------------------------------------
# 23.1 Generate Realistic Enterprise Customer Churn Dataset
# ------------------------------------------------------------------------------
np.random.seed(42)
n_customers = 2500

tenure_months = np.random.exponential(scale=24, size=n_customers).clip(1, 72)
monthly_charges = np.random.normal(loc=65, scale=25, size=n_customers).clip(18, 120)
total_charges = tenure_months * monthly_charges + np.random.normal(0, 50, size=n_customers)

contract_types = np.random.choice(["Month-to-month", "One year", "Two year"], size=n_customers, p=[0.55, 0.25, 0.20])
payment_methods = np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"], size=n_customers)
internet_service = np.random.choice(["DSL", "Fiber optic", "No"], size=n_customers, p=[0.4, 0.45, 0.15])

# Introduce realistic missing values (5% missing in total_charges and payment_methods)
total_charges[np.random.rand(n_customers) < 0.05] = np.nan
payment_methods = [pm if np.random.rand() > 0.05 else None for pm in payment_methods]

# Synthetic Churn Probability (Imbalanced target: ~25% churn)
churn_logits = (
    - 0.05 * tenure_months
    + 0.03 * monthly_charges
    + (contract_types == "Month-to-month") * 1.2
    - (contract_types == "Two year") * 1.5
    + (internet_service == "Fiber optic") * 0.8
    - 1.5
)
churn_prob = 1 / (1 + np.exp(-churn_logits))
churn_target = (np.random.rand(n_customers) < churn_prob).astype(int)

df_churn = pd.DataFrame({
    "tenure": tenure_months,
    "monthly_charges": monthly_charges,
    "total_charges": total_charges,
    "contract": contract_types,
    "payment_method": payment_methods,
    "internet_service": internet_service
})

print(f"Customer Churn Dataset Shape: {df_churn.shape}")
print(f"Churn Target Class Distribution: 0 (Retained) = {np.mean(churn_target == 0):.1%}, 1 (Churned) = {np.mean(churn_target == 1):.1%}")

# Train/Test Split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    df_churn, churn_target, test_size=0.20, random_state=42, stratify=churn_target
)

# ------------------------------------------------------------------------------
# 23.2 Leak-Free Preprocessing Pipeline via ColumnTransformer
# ------------------------------------------------------------------------------
numerical_cols = ["tenure", "monthly_charges", "total_charges"]
categorical_cols = ["contract", "payment_method", "internet_service"]

# Numerical Pipeline: Median Imputation -> Yeo-Johnson Power Transform -> Standard Scaling
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("power_trans", PowerTransformer(method="yeo-johnson")),
    ("scaler", StandardScaler())
])

# Categorical Pipeline: Most Frequent Imputation -> Smoothed Target Encoding
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("target_enc", TargetEncoder(smooth="auto", cv=5))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_pipeline, numerical_cols),
        ("cat", cat_pipeline, categorical_cols)
    ]
)

# ------------------------------------------------------------------------------
# 23.3 Imbalanced-Aware Gradient Boosting Model
# ------------------------------------------------------------------------------
# Calculate scale_pos_weight to balance positive class penalty: (# negative / # positive)
scale_pos_weight_value = np.sum(y_train_c == 0) / np.sum(y_train_c == 1)

churn_model = XGBClassifier(
    n_estimators=120,
    learning_rate=0.06,
    max_depth=4,
    scale_pos_weight=scale_pos_weight_value,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", churn_model)
])

# Fit full pipeline strictly on training data
full_pipeline.fit(X_train_c, y_train_c)

# ------------------------------------------------------------------------------
# 23.4 Probability Calibration (Platt Sigmoidal Scaling)
# ------------------------------------------------------------------------------
calibrated_churn_pipeline = CalibratedClassifierCV(
    estimator=full_pipeline,
    method="sigmoid",
    cv=3
)
calibrated_churn_pipeline.fit(X_train_c, y_train_c)

# ------------------------------------------------------------------------------
# 23.5 Production Evaluation Suite
# ------------------------------------------------------------------------------
test_preds_churn = calibrated_churn_pipeline.predict(X_test_c)
test_probs_churn = calibrated_churn_pipeline.predict_proba(X_test_c)[:, 1]

uncalibrated_probs = full_pipeline.predict_proba(X_test_c)[:, 1]

print("\n--- Model Evaluation on Unseen Test Customers ---")
print(f"  ROC-AUC Score:             {roc_auc_score(y_test_c, test_probs_churn):.4f}")
print(f"  PR-AUC (Average Precision):{average_precision_score(y_test_c, test_probs_churn):.4f}")
print(f"  Brier Score (Uncalibrated):{brier_score_loss(y_test_c, uncalibrated_probs):.4f}")
print(f"  Brier Score (Calibrated):  {brier_score_loss(y_test_c, test_probs_churn):.4f} (Lower is better)")

print("\nClassification Detailed Report:")
print(classification_report(y_test_c, test_preds_churn, target_names=["Retained", "Churned"]))

# ------------------------------------------------------------------------------
# 23.6 Model Serialization for Production Deployment
# ------------------------------------------------------------------------------
import joblib
capstone_model_path = "churn_pipeline_production.joblib"
joblib.dump(calibrated_churn_pipeline, capstone_model_path)
print(f"Successfully serialized production-ready model pipeline to '{capstone_model_path}'.")

print("\n" + "=" * 80)
print("ALL MACHINE LEARNING CURRICULUM MODULES (SECTIONS 1 TO 23) COMPLETED SUCCESSFULLY")
print("=" * 80)