import numpy as np
import pandas as pd
import polars as pl
from functools import wraps
import polars as pl
import logging
import time
import os

start_time = time.time()

print("=" * 68)
print("      NATIONAL SMART HEALTHCARE ANALYTICS DASHBOARD")
print("=" * 68)

print("\nLoading Healthcare Datasets")
print("-" * 50)

try:

    hospitals = pd.read_csv("hospitals.csv")
    print("Hospitals Dataset          : Loaded Successfully")

    doctors = pd.read_csv("doctors.csv")
    print("Doctors Dataset            : Loaded Successfully")

    patients = pd.read_csv("patients.csv")
    print("Patients Dataset           : Loaded Successfully")

    appointments = pd.read_csv("appointments.csv")
    print("Appointments Dataset       : Loaded Successfully")

    laboratory = pd.read_csv("laboratory.csv")
    print("Laboratory Dataset         : Loaded Successfully")

    pharmacy = pd.read_csv("pharmacy.csv")
    print("Pharmacy Dataset           : Loaded Successfully")

    insurance = pd.read_csv("insurance.csv")
    print("Insurance Dataset          : Loaded Successfully")

except Exception as e:

    print("Dataset Loading Failed")
    print(e)
    exit()
datasets = {
    "Hospitals Dataset": hospitals,
    "Doctors Dataset": doctors,
    "Patients Dataset": patients,
    "Appointments Dataset": appointments,
    "Laboratory Dataset": laboratory,
    "Pharmacy Dataset": pharmacy,
    "Insurance Dataset": insurance
}

for df in datasets.values():

    df.columns = df.columns.str.strip()


print("\n" + "-" * 50)
print("Dataset Validation")
print("-" * 50)

datasets = {
    "Hospitals Dataset": hospitals,
    "Doctors Dataset": doctors,
    "Patients Dataset": patients,
    "Appointments Dataset": appointments,
    "Laboratory Dataset": laboratory,
    "Pharmacy Dataset": pharmacy,
    "Insurance Dataset": insurance
}

valid = True

for name, df in datasets.items():

    if df.empty:

        print(f"{name:<28}: Invalid")
        valid = False

    else:

        print(f"{name:<28}: Valid")

if not valid:

    print("\nDataset Validation Failed")
    exit()

print("\nAll datasets validated successfully.")


print("\n" + "=" * 68)
print("DATA QUALITY REPORT")
print("=" * 68)

print("\nMissing Values\n")

display_names = {
    "ConsultationFee": "Consultation Fee",
    "LabCost": "Laboratory Cost",
    "MedicineCost": "Medicine Cost",
    "InsuranceAmount": "Insurance Amount"
}

for df in datasets.values():

    missing = df.isnull().sum()

    for column, count in missing.items():

        if count > 0:

            print(f"{display_names.get(column,column):<28}: {count}")

duplicate_patients = patients.duplicated().sum()

print()
print(f"Duplicate Patient Records  : {duplicate_patients}")


for df in datasets.values():

    for column in df.columns:

        if df[column].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(df[column]):

                df[column] = df[column].fillna(df[column].mean())

            else:

                mode = df[column].mode()

                if not mode.empty:

                    df[column] = df[column].fillna(mode.iloc[0])

print("\nMissing values recovered successfully.")


patients = patients.drop_duplicates()

print("\nDuplicate records removed successfully.")


appointments["AppointmentDate"] = pd.to_datetime(
    appointments["AppointmentDate"]
)

appointments["AppointmentDate"] = (
    appointments["AppointmentDate"]
    .dt.strftime("%Y-%m-%d")
)

print("\nAppointment dates standardized successfully.")


print("\n" + "=" * 68)
print("HEALTHCARE DATA WAREHOUSE")
print("=" * 68)

warehouse = patients.merge(

    hospitals,

    on="HospitalID",

    how="left"

)

warehouse = warehouse.merge(

    doctors,

    on="HospitalID",

    how="left"

)

warehouse = warehouse.merge(

    appointments,

    on=["PatientID","DoctorID"],

    how="left"

)

warehouse = warehouse.merge(

    laboratory,

    on="PatientID",

    how="left"

)

warehouse = warehouse.merge(

    pharmacy,

    on="PatientID",

    how="left"

)

warehouse = warehouse.merge(

    insurance,

    on="PatientID",

    how="left"

)


for column in warehouse.columns:

    if pd.api.types.is_numeric_dtype(warehouse[column]):

        warehouse[column] = warehouse[column].fillna(0)


print()

print(f"Total Hospitals            : {len(hospitals)}")
print(f"Total Doctors              : {len(doctors)}")
print(f"Total Patients             : {len(patients)}")
print(f"Total Appointments         : {len(appointments)}")

print("\n" + "=" * 68)
print("MONTHLY HEALTHCARE REVENUE")
print("=" * 68)

warehouse["TotalRevenue"] = (
    warehouse["ConsultationFee"] +
    warehouse["LabCost"] +
    warehouse["MedicineCost"]
)

warehouse["AppointmentDate"] = pd.to_datetime(
    warehouse["AppointmentDate"]
)

warehouse["Month"] = warehouse["AppointmentDate"].dt.strftime("%Y-%m")

monthly = warehouse.groupby(
    "Month"
)["TotalRevenue"].sum()

print()

for month, revenue in monthly.items():

    print(f"{month:<28}{revenue:.2f}")



print("\nHighest Revenue Month\n")

print(f"{monthly.idxmax():<28}{monthly.max():.2f}")

print("\n" + "=" * 68)
print("HOSPITAL REVENUE REPORT")
print("=" * 68)

hrr=warehouse.groupby("HospitalName")["TotalRevenue"].sum()
print(hrr.rename_axis(None).to_string())

print("\nHighest Revenue Hospital\n")
print(hrr.idxmax(),hrr.max())

print("\n" + "=" * 68)
print("STATE REVENUE REPORT")
print("=" * 68)

strr=warehouse.groupby("State")["TotalRevenue"].sum()
print()
print(strr.rename_axis(None).to_string())

print("\n" + "=" * 68)
print("SPECIALIZATION REPORT")
print("=" * 68)
spr=warehouse.groupby("Specialization")["TotalRevenue"].sum()
print(spr.rename_axis(None).to_string())

print("\n" + "=" * 68)
print("TOP PERFORMING DOCTORS")
print("=" * 68)
tpr=warehouse.groupby("DoctorName")["TotalRevenue"].sum().sort_values(ascending=False).head(3)
print(tpr.rename_axis(None).to_string())

print("\n" + "=" * 68)
print("TOP SPENDING PATIENTS")
print("=" * 68)
tsp=warehouse.groupby("PatientName")["TotalRevenue"].sum().sort_values(ascending=False).head(3)
print(tsp.rename_axis(None).to_string())
    

print("\n" + "=" * 68)
print("LABORATORY UTILIZATION")
print("=" * 68)

lu = (
    warehouse.groupby(["LabID", "TestName"], as_index=False)["LabCost"]
    .sum()
    .sort_values("LabID")
)

for _, row in lu.iterrows():
    print(f"{row['TestName']:<25}{row['LabCost']:>10.2f}")

print("\n" + "=" * 68)
print("PHARMACY UTILIZATION")
print("=" * 68)

pu = (
    warehouse.groupby(["PatientID", "PatientName"], as_index=False)["MedicineCost"]
    .sum()
    .sort_values("PatientID")
)


for _, row in pu.iterrows():
    print(f"{row['PatientName']:<25}{row['MedicineCost']:>10.2f}")
print("\n" + "=" * 68)
print("INSURANCE UTILIZATION")
print("=" * 68)

pu = (
    warehouse.groupby(["PatientID", "PatientName"], as_index=False)["InsuranceAmount"]
    .sum()
    .sort_values("PatientID")
)


for _, row in pu.iterrows():
    print(f"{row['PatientName']:<25}{row['InsuranceAmount']:>10.2f}")
    
    
print("\n" + "=" * 68)
print("RESOURCE OPTIMIZATION REPORT")
print("=" * 68)

rh=hrr.idxmax()

print("\nRecommended Hospital\n")
print(rh)

print("\nReason\n")

print("Highest Overall Revenue ")

print("\n" + "=" * 68)
print("UNIQUE MEDICAL SPECIALIZATIONS")
print("=" * 68)

print()

spec=warehouse["Specialization"].unique()
for sp in spec:
    print(sp)


def retry(max_attempts):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(1, max_attempts + 1):

                try:

                    return func(attempt, *args, **kwargs)

                except Exception as e:

                    print(f"\nAttempt {attempt} Failed")

                    if attempt == max_attempts:

                        print("\nInsurance data retrieval failed.")

            return None

        return wrapper

    return decorator

@retry(2)
def insurance_server(attempt):

    if attempt == 1:

        raise Exception("Temporary Failure")

    print("\nAttempt 2 Successful")

    print("\nInsurance data retrieved successfully.")
    
print("\n" + "=" * 68)
print("SYSTEM ACTIVITIES")
print("=" * 68)

print("\nInsurance Server")

insurance_server()    



try:

    with open("HealthcareReport.txt", "w") as file:

        file.write("National Smart Healthcare Analytics Report\n")

        file.write("=" * 50 + "\n\n")

        file.write("Hospital Revenue Report\n")

        for hospital, revenue in hrr.items():
            file.write(f"{hospital:<25}{revenue:.2f}\n")

    print("\nHealthcare Report Generated Successfully.")

    print("\nHealthcareReport.txt Saved Successfully.")

except Exception as e:

    print(e)
   
   
print("\n" + "=" * 68)
print("PERFORMANCE REPORT")
print("=" * 68)

end_time=time.time()

print("\nExecution Time\n")

print(f"{end_time-start_time:.3f} Seconds")


print("\n" + "=" * 68)
print("POLARS LAZY ANALYTICS")
print("=" * 68)

print("\n" + "=" * 68)
print("POLARS LAZY ANALYTICS")
print("=" * 68)

# Convert complex/nullable types (like 'Int64') to simple NumPy types (like 'int64')
warehouse_simple = warehouse.convert_dtypes(dtype_backend="numpy_nullable")

# Now Polars can convert it without PyArrow
warehouse_pl = pl.from_pandas(warehouse_simple)


lazy = (

    warehouse_pl

    .lazy()

    .group_by("HospitalName")

    .agg(

        pl.col("TotalRevenue").sum()

    )

    .sort("TotalRevenue", descending=True)

)

result = lazy.collect()

print("\nHighest Revenue Hospital\n")

print(result["HospitalName"][0])

print("\nRevenue\n")

print(f"{result['TotalRevenue'][0]:.2f}")

print("\nLazy Execution Completed Successfully")