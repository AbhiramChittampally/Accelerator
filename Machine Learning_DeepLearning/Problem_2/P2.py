import pandas as pd

data = {
    "Customer_ID": ["C101", "C102", "C103", "C104", "C105", "C106", "C107"],
    "Account_Age_Days": [120, 450, 90, 300, 210, 60, 500],
    "Monthly_Spend": [45.5, 120.0, 25.0, 85.0, 60.0, 15.0, 200.0],
    "Support_Calls": [4, 0, 5, 1, 2, 6, 1],
    "Inactivity_Days": [35, 5, 40, 12, 20, 45, 8],
    "Churn": ["Yes", "No", "Yes", "No", "No", "Yes", "No"]
}

df = pd.DataFrame(data)

print("========= TASK 1: DATASET =========")
print(df)


print("\n========== TASK 2: DATASET INFORMATION ==========")

print("Number of Rows     :", df.shape[0])
print("Number of Columns : ", df.shape[1])

print("\nColumns:")
for column in df.columns:
    print(column)


print("\n============ TASK 3: FEATURES AND TARGET =========")

features = [
    "Account_Age_Days",
    "Monthly_Spend",
    "Support_Calls",
]

target = "Churn"

print("Features: ")
for feature in features:
    print(feature)

print("\nTarget: ")
print(target)

print("\nWhy Customer_ID is excluded:")
print("Customer_ID is an arbitary unique identifier and contains")
print("no meaningful predictive pattern for churn.")


print("\n======= TASK 4: CHURN STATUS COUNTS ========")

churn_counts = df["Churn"].value_counts()

print("Churn Status Counts: ")
print(churn_counts)


print("\n========TASK 5: AVERAGE INACTIVITY DAYS =======")

churned_avg = df[df["Churn"] == "Yes"]["Inactivity_Days"].mean()
retained_avg = df[df["Churn"] == "No"]["Inactivity_Days"].mean()

print("Average Inactivity Days:")
print(f"Churned Customers  : {churned_avg} days")
print(f"Retained Customers : {retained_avg} days")


print("\n========= TASK 6: RULE-BASED PREDICTION =========")


def predict_churn(inactivity_days, monthly_spend):
    if inactivity_days > 30 and monthly_spend < 50:
        return "Yes"
    else:
        return "No"


df["Prediction"] = df.apply(
    lambda row: predict_churn(
        row["Inactivity_Days"],
        row["Monthly_Spend"]
    ),
    axis=1
)

print("Customer_ID   Actual    Prediction")

for _, row in df.iterrows():
    print(
        f"{row['Customer_ID']:<14}"
        f"{row['Churn']:<10}"
        f"{row['Prediction']}"
    )


print("\n======== TASK 7: RULE ACCURACY =========")

correct_predictions = (
    df["Churn"] == df["Prediction"]
).sum()

total_predictions = len(df)

accuracy = (
    correct_predictions / total_predictions
) * 100

print("Correct Predictions :", correct_predictions)
print("Total Predictions :", total_predictions)
print(f"Rule-Based Accuracy : {accuracy: .0f}%")


print("\n========== TASK 8: NEW CUSTOMER SCENARIOS ===========")

customer_A = {
    "Inactivity_Days": 32,
    "Monthly_Spend": 150.0,
    "Support_Calls": 6
}

customer_B = {
    "Inactivity_Days": 28,
    "Monthly_Spend": 30.0,
    "Support_Calls": 8
}

prediction_A = predict_churn(
    customer_A["Inactivity_Days"],
    customer_A["Monthly_Spend"]
)

prediction_B = predict_churn(
    customer_B["Inactivity_Days"],
    customer_B["Monthly_Spend"]
)

print("Customer A Prediction :", prediction_A)
print("Customer B Prediction :", prediction_B)

print("\nAnalysis:")
print("Customer B has 8 support calls and relatively high inactivity")
print("but the rule outputs 'No' because inactivity is not above 30 days.")
print("This shows that rule-based systems can miss complex combinations")
print("of customer behavior.")


print("\n=========TASK 9: FEATURES & LABELS FOUNDATIONS===========")

print("FEATURES & LABELS FOUNDATIONS")
print()
print("Features (X) : Input measures provided to the model")
print("                 (e.g., Inactivity_Days, Support_Calls).")
print()
print("Target (y) : The ground-truth answer the model tries")
print("                  to learn/predict (e.g., Churn).")


print("========== CUSTOMER CHURN ANALYSIS ==========")


total_customers = df["Customer_ID"].count()

churned_customers = int(
    df["Churn"].value_counts().get("Yes", 0)
)

retained_customers = int(
    df["Churn"].value_counts().get("No", 0)
)


average_inactivity_churned = float(
    df.loc[df["Churn"] == "Yes", "Inactivity_Days"].mean()
)

average_inactivity_retained = float(
    df.loc[df["Churn"] == "No", "Inactivity_Days"].mean()
)


correct_predictions = int(
    (df["Churn"] == df["Prediction"]).sum()
)

total_predictions = len(df)

rule_accuracy = (
    correct_predictions / total_predictions
) * 100


print()
print("Total Customers        :", total_customers)

print("Churned Customers      :", churned_customers)
print("Retained Customers     :", retained_customers)

print()
print("Average Inactivity")
print("Churned                :", average_inactivity_churned, "days")
print("Retained               :", average_inactivity_retained, "days")

print()
print("Rule-Based Accuracy    :", rule_accuracy, "%")

print()
print("New Customer A Pred    :", prediction_A)
print("New Customer B Pred    :", prediction_B)


print()
print("Churned Customers: 3")
print("Retained Customers: 4")
print("Average Inactivity for Churned Customers: 40.0 days")
print("Average Inactivity for Retained Customers: 11.25 days")


print()
print("Conclusion:")
print("Hardcoded rules fail when missing complex interactions like high support calls.")
print("ML models dynamically balance all input features simultaneously.")