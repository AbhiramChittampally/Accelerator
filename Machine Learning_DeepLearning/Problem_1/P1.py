# copy your solution
import pandas as pd

data = {
    "Employee_ID": ["E101", "E102", "E103", "E104", "E105"],
    "Distance_KM": [5, 18, 7, 22, 10],
    "Travel_Time_Min": [20, 65, 30, 75, 40],
    "Previous_Late_Count": [1, 5, 0, 7, 2],
    "Weather": ["Clear", "Rain", "Clear", "Rain", "Cloudy"],
    "Transport": ["Bus", "Bus", "Car", "Bus", "Bike"],
    "Late": ["No", "Yes", "No", "Yes", "No"]
}

df = pd.DataFrame(data)

df
df.shape

number_of_rows = df.shape[0]
number_of_columns = df.shape[1]

print("Number of Rows:", number_of_rows)
print("Number of Columns:", number_of_columns)

df.columns

features = [
    "Distance_KM",
    "Travel_Time_Min",
    "Previous_Late_Count",
    "Weather",
    "Transport"
]

target = "Late"

df["Late"].value_counts()

df.groupby("Late")["Travel_Time_Min"].mean()

# TASK 6: Apply Rule-Based Prediction

df["Prediction"] = (
    (df["Distance_KM"] > 15) &
    (df["Travel_Time_Min"] > 60)
)

df["Prediction"] = df["Prediction"].map({True: "Yes", False: "No"})

df[["Employee_ID", "Late", "Prediction"]]

# TASK 7: Calculate Rule Accuracy
correct_predictions = (df["Late"] == df["Prediction"]).sum()
total_predictions = len(df)

accuracy = correct_predictions / total_predictions

print("Correct Predictions :", correct_predictions)
print("Total Predictions   :", total_predictions)
print(f"Rule-Based Accuracy : {accuracy * 100:.0f}%")

# TASK 8 — Predict for a New Employee

distance_km = 20
travel_time_min = 70
previous_late_count = 3
weather = "Rain"
transport = "Bus"

if (distance_km > 15 and
    travel_time_min > 60):

    prediction_1 = "Yes"
else:
    prediction_1 = "No"

print("New Employee Details")
print("--------------------")
print("Distance (KM):", distance_km)
print("Travel Time (Min):", travel_time_min)
print("Previous Late Count:", previous_late_count)
print("Weather:", weather)
print("Transport:", transport)

print("\nPrediction:", prediction_1)

# TASK 9 — Test Another New Employee

distance_km = 12
travel_time_min = 55
previous_late_count = 6
weather = "Rain"
transport = "Bus"

if (distance_km > 15 and
    travel_time_min > 60):

    prediction_2 = "Yes"
else:
    prediction_2 = "No"

print("Employee Distance :", distance_km, "KM")
print("Travel Time       :", travel_time_min, "Minutes")
print("Prediction:", prediction_2)

if prediction_2 == "No":
    print("Employee is predicted as not late by the current rule.")
else:
    print("Employee is predicted as late by the current rule.")

print("Does this guarantee the employee will be on time? No")

# TASK 10 — Rule-Based System vs Machine Learning

print("==========================================")
print("       RULE-BASED SYSTEM")
print("==========================================")

print("Programmer manually defines conditions.")
print()
print("Example:")
print("Distance > 15")
print("AND Travel Time > 60 -> Late")

print()
print("==========================================")
print("       MACHINE LEARNING SYSTEM")
print("==========================================")

print("Model learns patterns from historical data.")
print()
print("The programmer provides data and the expected")
print("outcome, and the model learns relationships")
print("from the data.")

print()
print("==========================================")
print("WHY MACHINE LEARNING MAY BE MORE USEFUL")
print("==========================================")

print("When the company has 50 additional attributes,")
print("writing hundreds of rules manually becomes:")
print("- Time-consuming")
print("- Difficult to maintain")
print("- Difficult to handle complex relationships")
print("- More likely to miss important patterns")

print()
print("A Machine Learning approach can:")
print("- Use many features together")
print("- Learn patterns automatically from historical data")
print("- Discover relationships that may not be obvious")
print("- Make predictions for new employees")

print()
print("==========================================")
print("   EMPLOYEE ATTENDANCE ANALYSIS")
print("==========================================")

total_employees = 5
late_employees = 2
not_late_employees = 3

average_travel_time_late = 70.0
average_travel_time_not_late = 30.0

new_employee_1 = "Late"
new_employee_2 = "Not Late"

print()
print("Total Employees        :", total_employees)
print("Late Employees         :", late_employees)
print("Not Late Employees     :", not_late_employees)

print()
print("Average Travel Time")
print("Late                   :", average_travel_time_late, "minutes")
print("Not Late               :", average_travel_time_not_late, "minutes")

print()
print("Rule-Based Accuracy    : 100%")

print()
print("New Employee 1")
print("Prediction             :", new_employee_1)

print()
print("New Employee 2")
print("Prediction             :", new_employee_2)

print()
print("Conclusion:")
print("A rule-based system depends on manually defined conditions.")
print("A Machine Learning system can learn patterns from historical data")
print("and use multiple features to make predictions.")

# FINAL EXPECTED OUTPUT

print("=" * 55)
print("          EMPLOYEE ATTENDANCE ANALYSIS")
print("=" * 55)

print()

print("Total Employees        :", len(df))

print()
print("Late Employees         :", (df["Late"] == "Yes").sum())
print("Not Late Employees     :", (df["Late"] == "No").sum())

late_avg = df[df["Late"] == "Yes"]["Travel_Time_Min"].mean()
not_late_avg = df[df["Late"] == "No"]["Travel_Time_Min"].mean()

print()
print("Average Travel Time")
print("Late                   :", late_avg, "minutes")
print("Not Late               :", not_late_avg, "minutes")

print()
print("Rule-Based Accuracy    :", f"{accuracy * 100:.0f}%")

print()
print("New Employee 1")
print("Prediction             :", "Late" if prediction_1 == "Yes" else "Not Late")

print()
print("New Employee 2")
print("Prediction             :", "Late" if prediction_2 == "Yes" else "Not Late")

print()
print("Conclusion:")
print("A rule-based system depends on manually defined conditions.")
print("A Machine Learning system can learn patterns from historical data")
print("and use multiple features to make predictions.")