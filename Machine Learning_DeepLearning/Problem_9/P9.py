# copy your solution

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split


def run_pipeline():

    # ============================================================
    # INPUT DATA
    # ============================================================

    demographics_data = {
        'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
        'Age': [45, 62, 29, 71, 55, 38, 67, 42, 59, 31,
                48, 65, 26, 73, 52, 35, 69, 41, 58, 33,
                50, 61, 28, 70, 54, 39, 66, 44, 60, 30,
                47, 64, 27, 72, 53, 36, 68, 43, 57, 32,
                49, 63, 25, 74, 51, 37, 70, 40, 56, 34],
        'Gender': ['F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
                   'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
                   'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
                   'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M',
                   'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M']
    }

    vitals_data = {
        'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
        'BMI': [24.5, 31.2, 21.0, 34.8, 28.1, 23.4, 32.5, 26.0, 29.8, 22.1,
                25.3, 30.8, 20.5, 35.2, 27.9, 23.0, 33.1, 25.8, 29.1, 21.8,
                26.1, 31.5, 20.8, 34.2, 28.5, 23.9, 32.0, 26.4, 29.5, 22.5,
                25.0, 31.0, 20.2, 35.6, 27.5, 23.2, 33.5, 25.5, 28.8, 22.0,
                25.8, 31.8, 20.0, 36.0, 28.2, 23.6, 32.8, 26.2, 29.0, 22.3],
        'Blood_Pressure_Systolic': [120, 145, 115, 160, 132, 122, 150, 128, 138, 118,
                                    122, 142, 112, 162, 130, 120, 152, 126, 136, 116,
                                    124, 144, 114, 158, 134, 121, 148, 127, 137, 117,
                                    121, 141, 111, 165, 129, 119, 154, 125, 135, 115,
                                    123, 143, 110, 164, 131, 122, 151, 126, 134, 116]
    }

    diagnostics_data = {
        'Patient_ID': [f'PAT_{500+i}' for i in range(50)],
        'Biomarker_Level': [1.2, 8.5, 0.8, 9.1, 2.1, 1.0, 7.8, 1.5, 3.2, 0.9,
                            1.4, 7.9, 0.7, 9.5, 2.3, 1.1, 8.2, 1.6, 3.0, 0.8,
                            1.3, 8.1, 0.6, 9.0, 2.0, 1.2, 7.5, 1.4, 3.1, 0.9,
                            1.1, 8.3, 0.5, 9.8, 2.2, 1.0, 8.0, 1.5, 2.9, 0.7,
                            1.3, 8.4, 0.4, 9.6, 2.4, 1.1, 7.7, 1.6, 2.8, 0.8],
        'Has_Condition': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                          0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                          0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                          0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
                          0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
    }

    df_demo = pd.DataFrame(demographics_data)
    df_vitals = pd.DataFrame(vitals_data)
    df_diag = pd.DataFrame(diagnostics_data)


    # ============================================================
    # TASK 1 — MULTI-TABLE DIAGNOSTIC INTEGRATION
    # ============================================================

    master_df = df_demo.merge(
        df_vitals,
        on="Patient_ID",
        how="inner"
    )

    master_df = master_df.merge(
        df_diag,
        on="Patient_ID",
        how="inner"
    )

    print("\n========== TASK 1 — MASTER DIAGNOSTIC DATASET ==========")
    print(master_df.head())


    # ============================================================
    # TASK 2 — TARGET IMBALANCE & FEATURE EXTRACTION
    # ============================================================

    class_counts = (
        master_df["Has_Condition"]
        .value_counts()
        .sort_index()
    )

    class_percentages = (
        master_df["Has_Condition"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    negative_count = class_counts.get(0, 0)
    positive_count = class_counts.get(1, 0)

    negative_percentage = class_percentages.get(0, 0)
    positive_percentage = class_percentages.get(1, 0)

    X = master_df.drop(
        columns=["Patient_ID", "Has_Condition"]
    )

    y = master_df["Has_Condition"]

    print("\n========== TASK 2 — TARGET IMBALANCE ==========")

    print("Class Distribution (Has_Condition):")

    print(
        f"- Negative (0) : {negative_count} patients "
        f"({negative_percentage:.1f}%)"
    )

    print(
        f"- Positive (1) : {positive_count} patients "
        f"({positive_percentage:.1f}%)"
    )


    # ============================================================
    # TASK 3 — NON-STRATIFIED RANDOM SPLIT
    # ============================================================

    train_random, test_random = train_test_split(
        master_df,
        test_size=0.20,
        random_state=42
    )

    random_train_counts = (
        train_random["Has_Condition"]
        .value_counts()
        .sort_index()
    )

    random_train_percentages = (
        train_random["Has_Condition"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    random_test_counts = (
        test_random["Has_Condition"]
        .value_counts()
        .sort_index()
    )

    random_test_percentages = (
        test_random["Has_Condition"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    random_test_positive_percentage = (
        random_test_percentages.get(1, 0)
    )

    random_drift = (
        random_test_positive_percentage
        - positive_percentage
    )

    print("\n========== TASK 3 — NON-STRATIFIED RANDOM SPLIT ==========")

    print("Non-Stratified Split (80/20):")

    print(
        f"- Training Set Size : {len(train_random)} records"
    )

    print(
        f"  - Negative (0)    : "
        f"{random_train_counts.get(0, 0)} "
        f"({random_train_percentages.get(0, 0):.1f}%)"
    )

    print(
        f"  - Positive (1)    : "
        f"{random_train_counts.get(1, 0)} "
        f"({random_train_percentages.get(1, 0):.1f}%)"
    )

    print(
        f"- Testing Set Size  : {len(test_random)} records"
    )

    print(
        f"  - Negative (0)    : "
        f"{random_test_counts.get(0, 0)} "
        f"({random_test_percentages.get(0, 0):.1f}%)"
    )

    print(
        f"  - Positive (1)    : "
        f"{random_test_counts.get(1, 0)} "
        f"({random_test_percentages.get(1, 0):.1f}%)"
    )

    print(
        f"Drift Analysis      : Positive class proportion "
        f"shifted from {positive_percentage:.1f}% in full dataset "
        f"to {random_test_positive_percentage:.1f}% in test set."
    )


    # ============================================================
    # TASK 4 — STRATIFIED TRAIN-TEST SPLIT
    # ============================================================

    X_train_strat, X_test_strat, y_train_strat, y_test_strat = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42
    )

    strat_train_counts = (
        y_train_strat
        .value_counts()
        .sort_index()
    )

    strat_train_percentages = (
        y_train_strat
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    strat_test_counts = (
        y_test_strat
        .value_counts()
        .sort_index()
    )

    strat_test_percentages = (
        y_test_strat
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    strat_test_positive_percentage = (
        strat_test_percentages.get(1, 0)
    )

    print("\n========== TASK 4 — STRATIFIED SPLIT ==========")

    print("Stratified Split (80/20):")

    print(
        f"- Training Set Size : {len(X_train_strat)} records"
    )

    print(
        f"  - Negative (0)    : "
        f"{strat_train_counts.get(0, 0)} "
        f"({strat_train_percentages.get(0, 0):.1f}%)"
    )

    print(
        f"  - Positive (1)    : "
        f"{strat_train_counts.get(1, 0)} "
        f"({strat_train_percentages.get(1, 0):.1f}%)"
    )

    print(
        f"- Testing Set Size  : {len(X_test_strat)} records"
    )

    print(
        f"  - Negative (0)    : "
        f"{strat_test_counts.get(0, 0)} "
        f"({strat_test_percentages.get(0, 0):.1f}%)"
    )

    print(
        f"  - Positive (1)    : "
        f"{strat_test_counts.get(1, 0)} "
        f"({strat_test_percentages.get(1, 0):.1f}%)"
    )

    print(
        f"Drift Analysis      : Class ratios "
        f"preserved across both splits "
        f"({strat_test_percentages.get(0, 0):.1f}% / "
        f"{strat_test_percentages.get(1, 0):.1f}%)."
    )


    # ============================================================
    # TASK 5 — FEATURE ISOLATION & SHAPE AUDIT
    # ============================================================

    X_train = X_train_strat
    X_test = X_test_strat
    y_train = y_train_strat
    y_test = y_test_strat

    print("\n========== TASK 5 — FEATURE & TARGET SHAPES ==========")

    print("Final Matrix Dimensions:")

    print("- X_train Shape :", X_train.shape)
    print("- X_test Shape  :", X_test.shape)
    print("- y_train Shape :", y_train.shape)
    print("- y_test Shape  :", y_test.shape)


    # ============================================================
    # FINAL EXPECTED OUTPUT
    # ============================================================

    print("\n")
    print(
        "========== TRAIN-TEST SPLITTING "
        "& STRATIFIED SAMPLING AUDIT =========="
    )

    print(
        "\nMaster Diagnostic Dataset Records :",
        len(master_df)
    )

    print(
        "Target Label Class Ratio          : "
        f"{negative_percentage:.1f}% Negative (0) | "
        f"{positive_percentage:.1f}% Positive (1)"
    )

    print("\nSampling Methodology Comparison:")

    print(
        "- Standard Random Split (80/20)   : "
        f"Test set shifted to "
        f"{random_test_percentages.get(0, 0):.1f}% Negative / "
        f"{random_test_percentages.get(1, 0):.1f}% Positive "
        "(Distribution Drift)"
    )

    print(
        "- Stratified Random Split (80/20) : "
        f"Test set maintained "
        f"{strat_test_percentages.get(0, 0):.1f}% Negative / "
        f"{strat_test_percentages.get(1, 0):.1f}% Positive ratio"
    )

    print("\nFinal Prepared Matrices:")

    print(
        "- Training Features (X_train)     : "
        f"{X_train.shape[0]} Rows, "
        f"{X_train.shape[1]} Numerical/Categorical Features"
    )

    print(
        "- Testing Features (X_test)       : "
        f"{X_test.shape[0]} Rows, "
        f"{X_test.shape[1]} Numerical/Categorical Features"
    )

    print("\nConclusion:")

    print(
        "For imbalanced datasets, Stratified Sampling "
        "is used to reduce class distribution drift "
        "between training and evaluation phases."
    )

    return {
        "master_df": master_df,
        "train_random": train_random,
        "test_random": test_random,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }


if __name__ == "__main__":
    run_pipeline()