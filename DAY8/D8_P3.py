"""
Problem Title: Smart Hospital Treatment Analytics using Pandas

Problem Statement:
A multi-specialty hospital maintains patient treatment
details in a CSV file.

The hospital management wants to analyze the treatment
cost incurred by different departments using Pandas.

Each patient record contains:

Patient ID
Patient Name
Department
Treatment Cost

The program should perform the following operations.

Step 1:Load the patient dataset using Pandas.

Step 2:Display the complete patient dataset.

Step 3:Using groupby() and agg(), calculate department-wise:

• Total Treatment Cost
• Average Treatment Cost
• Maximum Treatment Cost
• Minimum Treatment Cost

Step 4:Sort the departments in descending order of Total Treatment Cost.

Step 5: Display only those departments whose average treatment cost is greater than or equal to 50000.

Requirements
------------
1. Read patients.csv.
2. Create a Pandas DataFrame.
3. Use groupby().
4. Use agg().
5. Use sort_values().
6. Filter the aggregated result.

Input File
----------

patients.csv

Output Format
-------------
Patient Dataset

...

Department Statistics

Department Total Average Maximum Minimum

...

High Cost Departments

...

Sample patients.csv
-------------------

PatientID,PatientName,Department,TreatmentCost
P101,Ravi,Cardiology,60000
P102,Priya,Neurology,45000
P103,Rahul,Cardiology,70000
P104,Anu,Orthopedics,30000
P105,Kiran,Neurology,55000
P106,Ajay,Orthopedics,40000



case=1
output=
Patient Dataset
P101 Ravi Cardiology 60000
P102 Priya Neurology 45000
P103 Rahul Cardiology 70000
P104 Anu Orthopedics 30000
P105 Kiran Neurology 55000
P106 Ajay Orthopedics 40000

Department Statistics
Cardiology 130000 65000.0 70000 60000
Neurology 100000 50000.0 55000 45000
Orthopedics 70000 35000.0 40000 30000

High Cost Departments
Cardiology 65000.0
Neurology 50000.0
"""
import pandas as pd
df=pd.read_csv("patients.csv")
print("Patient Dataset")
print(df.to_string(index=False,header=False))

print("\nDepartment Statistics")
stats=df.groupby("Department")["TreatmentCost"].agg(["sum","mean","max","min"]).sort_values(by="sum",ascending=False)
print(stats.rename_axis(None).to_string(header=False))

print("\nHigh Cost Departments")
print(stats.loc[stats["mean"]>=50000]["mean"].to_string(header=False))