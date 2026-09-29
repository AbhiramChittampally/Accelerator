# copy your solution

import pandas as pd
import numpy as np

from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def run_pipeline():

    # ============================================================
    # INPUT DATA
    # ============================================================

    policyholder_data = {
        'Policy_ID': [f'POL_{700+i}' for i in range(50)],
        'Driver_Age': [22, 45, 34, 60, 28, 50, 19, 41, 33, 55,
                       24, 48, 31, 62, 26, 52, 20, 43, 36, 58,
                       23, 46, 32, 61, 27, 51, 21, 42, 35, 56,
                       25, 49, 30, 63, 29, 53, 22, 44, 37, 59,
                       24, 47, 33, 64, 28, 54, 20, 40, 38, 57],
        'Credit_Score': [610, 750, 680, 810, 640, 780, 580, 720, 690, 790,
                         620, 760, 670, 820, 630, 770, 590, 730, 700, 800,
                         615, 755, 675, 815, 635, 775, 585, 725, 695, 795,
                         625, 765, 665, 825, 645, 785, 600, 735, 705, 805,
                         618, 758, 678, 818, 638, 778, 592, 722, 698, 788]
    }

    vehicle_data = {
        'Policy_ID': [f'POL_{700+i}' for i in range(50)],
        'Vehicle_Age_Yrs': [12, 3, 7, 1, 9, 2, 14, 4, 6, 2,
                            11, 2, 8, 1, 10, 3, 13, 5, 6, 1,
                            12, 3, 7, 1, 9, 2, 14, 4, 5, 2,
                            10, 2, 8, 1, 9, 3, 13, 4, 6, 1,
                            11, 3, 7, 1, 10, 2, 14, 5, 6, 2],
        'Annual_Mileage_KM': [22000, 11000, 15000, 8000, 18000, 9500, 25000, 12000, 14000, 9000,
                              21000, 10500, 16000, 7500, 19000, 9800, 24000, 12500, 14500, 8500,
                              22500, 11200, 15200, 8200, 18200, 9600, 25500, 12200, 13800, 9100,
                              20500, 10800, 16200, 7800, 18800, 10000, 24500, 12800, 14200, 8800,
                              21800, 11100, 15800, 8100, 18500, 9700, 25200, 12100, 14100, 9200]
    }

    claim_data = {
        'Policy_ID': [f'POL_{700+i}' for i in range(50)],
        'Made_Claim': [1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
    }

    df_policy = pd.DataFrame(policyholder_data)
    df_vehicle = pd.DataFrame(vehicle_data)
    df_claim = pd.DataFrame(claim_data)


    # ============================================================
    # TASK 1 — RELATIONAL INSURANCE DATA MERGING
    # ============================================================

    master_df = df_policy.merge(
        df_vehicle,
        on="Policy_ID",
        how="inner"
    )

    master_df = master_df.merge(
        df_claim,
        on="Policy_ID",
        how="inner"
    )

    print("\n========== TASK 1 — MASTER INSURANCE DATASET ==========")
    print(master_df.head())


    # ============================================================
    # FEATURE AND TARGET EXTRACTION
    # ============================================================

    X = master_df.drop(
        columns=["Policy_ID", "Made_Claim"]
    )

    y = master_df["Made_Claim"]

    claim_count = y.value_counts().get(1, 0)
    no_claim_count = y.value_counts().get(0, 0)

    claim_percentage = y.mean() * 100
    no_claim_percentage = 100 - claim_percentage


    # ============================================================
    # TASK 2 — STANDARD 5-FOLD CROSS-VALIDATION
    # ============================================================

    kfold = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    kfold_claim_percentages = []

    print("\n========== TASK 2 — K-FOLD CROSS-VALIDATION ==========")
    print("K-Fold Splitting Summary (5 Folds):")

    for fold, (train_idx, validation_idx) in enumerate(
        kfold.split(X),
        start=1
    ):

        y_validation = y.iloc[validation_idx]

        validation_size = len(validation_idx)
        validation_claims = y_validation.sum()
        validation_percentage = y_validation.mean() * 100

        kfold_claim_percentages.append(
            validation_percentage
        )

        print(
            f"- Fold {fold} Validation : "
            f"{validation_size} Records | "
            f"Target Claims: {validation_claims} "
            f"({validation_percentage:.1f}%)"
        )

    kfold_min = min(kfold_claim_percentages)
    kfold_max = max(kfold_claim_percentages)

    print(
        f"Target Variance     : Claim ratio varies across folds "
        f"({kfold_min:.1f}% to {kfold_max:.1f}%)."
    )


    # ============================================================
    # TASK 3 — STRATIFIED 5-FOLD CROSS-VALIDATION
    # ============================================================

    stratified_kfold = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    stratified_claim_percentages = []

    print("\n========== TASK 3 — STRATIFIED K-FOLD ==========")
    print("Stratified K-Fold Splitting Summary (5 Folds):")

    for fold, (train_idx, validation_idx) in enumerate(
        stratified_kfold.split(X, y),
        start=1
    ):

        y_validation = y.iloc[validation_idx]

        validation_size = len(validation_idx)
        validation_claims = y_validation.sum()
        validation_percentage = y_validation.mean() * 100

        stratified_claim_percentages.append(
            validation_percentage
        )

        print(
            f"- Fold {fold} Validation : "
            f"{validation_size} Records | "
            f"Target Claims: {validation_claims} "
            f"({validation_percentage:.1f}%)"
        )

    stratified_min = min(stratified_claim_percentages)
    stratified_max = max(stratified_claim_percentages)

    print(
        f"Target Variance     : Claim ratio is maintained across "
        f"validation folds ({stratified_min:.1f}% to "
        f"{stratified_max:.1f}%)."
    )


    # ============================================================
    # TASK 4 — LOGISTIC REGRESSION CROSS-VALIDATION
    # ============================================================

    model = LogisticRegression(
        max_iter=1000
    )

    accuracy_scores = []

    print("\n========== TASK 4 — LOGISTIC REGRESSION ==========")
    print("Logistic Regression 5-Fold Accuracy Scores:")

    for fold, (train_idx, validation_idx) in enumerate(
        stratified_kfold.split(X, y),
        start=1
    ):

        X_train = X.iloc[train_idx]
        X_validation = X.iloc[validation_idx]

        y_train = y.iloc[train_idx]
        y_validation = y.iloc[validation_idx]

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_validation
        )

        fold_accuracy = accuracy_score(
            y_validation,
            predictions
        )

        accuracy_scores.append(
            fold_accuracy
        )

        print(
            f"- Fold {fold} : "
            f"{fold_accuracy * 100:.1f}%"
        )

    mean_accuracy = np.mean(
        accuracy_scores
    )

    std_accuracy = np.std(
        accuracy_scores
    )

    print(
        f"Mean Validation Accuracy : "
        f"{mean_accuracy * 100:.1f}% "
        f"(+/- {std_accuracy * 100:.1f}%)"
    )


    # ============================================================
    # TASK 5 — OVERFITTING & UNDERFITTING DIAGNOSTICS
    # ============================================================

    print("\n========== TASK 5 — OVERFITTING DIAGNOSTICS ==========")

    print("DIAGNOSTIC MATRIX:")

    print(
        "1. Underfitting  : High Training Error, "
        "High Validation Error (Model is too simple)."
    )

    print(
        "2. Overfitting   : Very Low Training Error, "
        "High Validation Error (Model memorizes noise)."
    )

    print(
        "3. Optimal Model : Low Training Error, "
        "Low Validation Error (Model generalizes well)."
    )


    # ============================================================
    # FINAL EXPECTED OUTPUT
    # ============================================================

    print("\n")
    print(
        "========== CROSS-VALIDATION "
        "& OVERFITTING DIAGNOSTICS =========="
    )

    print(
        "\nMaster Insurance Dataset Records :",
        len(master_df)
    )

    print(
        "Features (X)                     : "
        + ", ".join(X.columns)
    )

    print(
        "Target (y)                       : "
        f"Made_Claim ({claim_percentage:.1f}% Positive Rate)"
    )

    print("\nCross-Validation Comparison:")

    print(
        f"- Standard K-Fold (5 Splits)     : "
        f"Validation positive rate: "
        f"{kfold_min:.1f}% - {kfold_max:.1f}%"
    )

    print(
        f"- Stratified K-Fold (5 Splits)   : "
        f"Validation positive rate: "
        f"{stratified_min:.1f}% - {stratified_max:.1f}%"
    )

    print("\nBaseline Evaluation Results:")

    print(
        f"- Mean CV Accuracy Score          : "
        f"{mean_accuracy * 100:.1f}% "
        f"(+/- {std_accuracy * 100:.1f}%)"
    )

    print("\nConclusion:")

    print(
        "Stratified K-Fold Cross-Validation ensures "
        "consistent evaluation on imbalanced risk data "
        "by maintaining label distributions across "
        "cross-validation folds."
    )

    return {
        "master_df": master_df,
        "X": X,
        "y": y,
        "kfold_claim_percentages": kfold_claim_percentages,
        "stratified_claim_percentages": stratified_claim_percentages,
        "accuracy_scores": accuracy_scores,
        "mean_accuracy": mean_accuracy,
        "std_accuracy": std_accuracy
    }


if __name__ == "__main__":
    run_pipeline()