"""
Project Title: Smart Hospital Patient Data Cleansing and Healthcare Intelligence Platform using NumPy and Pandas

Problem Statement:
A multi-specialty hospital maintains patient information in multiple CSV files.
Patient records are collected from different hospital branches. During synchronization, 
some records contain missing values, duplicate entries, and inconsistent treatment information.
Before generating analytical reports, the hospital management wants to clean the data and 
generate a Healthcare Intelligence Dashboard.

The available CSV files are:
Patient File Contains
Patient ID
Patient Name
Department
Age

Treatment File Contains
Patient ID
Consultation Cost
Lab Cost
Pharmacy Cost

Billing File Contains
Patient ID
Admission Date
Total Bill

Vitals File Contains
    Patient ID
    Blood Pressure
 Some records contain
    Missing Treatment Costs
    Missing Blood Pressure
    Duplicate Patient Records

The program should perform the following operations.
Step 1:Load all four CSV files using Pandas.
Step 2:Merge all DataFrames using Patient ID.
Step 3: Display the complete merged dataset.
Step 4:Display missing values using isnull().
Step 5:Fill missing Total Bill using the average bill of all patients using fillna().
Step 6:Recover missing Blood Pressure using interpolate().
Step 7:Remove duplicate patient records using drop_duplicates().
Step 8:Convert Admission Date into Datetime using pd.to_datetime().
Step 9:Set Admission Date as DatetimeIndex.
Step 10:Generate Monthly Hospital Revenue using resample().
Step 11:Generate Department-wise Revenue using groupby().
Step 12:Generate a Department-wise Revenue Pivot Table using pivot_table().
Step 13:Convert Treatment Columns
Consultation Cost
Lab Cost
Pharmacy Cost
into Long Format using melt().

Step 14:Reconstruct the original treatment table using pivot().
Step 15:Using loc() Display only Cardiology patients.
Step 16:Using iloc() Display second and third patient records.
Step 17: Using NumPy Vectorization
Calculate
Insurance Bonus
Insurance Bonus = Total Bill × 5%

Step 18:Using NumPy Broadcasting
Calculate:Final Bill = Total Bill + Insurance Bonus

Step 19:Display the department generating the highest revenue.

Step 20:Display the patient having the highest bill.

Requirements:
----------------
Read four CSV files.
Merge multiple DataFrames.
Use isnull().
Use fillna().
Use interpolate().
Use drop_duplicates().
Use pd.to_datetime().
Use DatetimeIndex.
Use resample().
Use groupby().
Use pivot_table().
Use melt().
Use pivot().
Use loc().
Use iloc().
Use NumPy Arrays.
Use Vectorization.
Use Broadcasting.


Input Files:
--------------
patients.csv
----------
PatientID,PatientName,Department,Age
P101,Ravi,Cardiology,45
P102,Priya,Neurology,38
P103,Rahul,Orthopedics,50
P104,Anu,Cardiology,42
P105,Kiran,Neurology,36
P105,Kiran,Neurology,36

Note: Last record is intentionally duplicated.
It will be removed using drop_duplicates().

treatments.csv
--------------
PatientID,ConsultationCost,LabCost,PharmacyCost
P101,500,1200,800
P102,600,1000,900
P103,550,1500,1000
P104,650,1100,850
P105,500,1300,950



billing.csv
--------------
PatientID,AdmissionDate,TotalBill
P101,2025-01-05,25000
P102,2025-01-18,
P103,2025-02-10,32000
P104,2025-02-20,28000
P105,2025-03-08,

Note:Missing bills for
P102
P105
These must be filled

vitals.csv
--------------
PatientID,BloodPressure
P101,120
P102,
P103,130
P104,
P105,125

Missing Blood Pressure:
P102
P104
These will be recovered 


case=1
output=
Complete Hospital Report
P101 Ravi Cardiology 45 500 1200 800 2025-01-05 25000.0 120.0
P102 Priya Neurology 38 600 1000 900 2025-01-18 nan nan
P103 Rahul Orthopedics 50 550 1500 1000 2025-02-10 32000.0 130.0
P104 Anu Cardiology 42 650 1100 850 2025-02-20 28000.0 nan
P105 Kiran Neurology 36 500 1300 950 2025-03-08 nan 125.0
P105 Kiran Neurology 36 500 1300 950 2025-03-08 nan 125.0

Missing Values
False False False False False False False False False False
False False False False False False False False True True
False False False False False False False False False False
False False False False False False False False False True
False False False False False False False False True False
False False False False False False False False True False

Recovered Dataset
P101 Ravi Cardiology 45 25000.0 120.0
P102 Priya Neurology 38 28333.33 125.0
P103 Rahul Orthopedics 50 32000.0 130.0
P104 Anu Cardiology 42 28000.0 127.5
P105 Kiran Neurology 36 28333.33 125.0

Monthly Hospital Revenue
2025-01 53333.33
2025-02 60000.0
2025-03 28333.33

Department Revenue
Cardiology 53000.0
Neurology 56666.67
Orthopedics 32000.0

Department Revenue Pivot Table

OrderDate    2025-01  2025-02  2025-03
Department
Cardiology    25000.0   28000.0      0.0
Neurology     28333.33      0.0 28333.33
Orthopedics       0.0   32000.0      0.0

Treatment Long Format
P101 Ravi ConsultationCost 500
P102 Priya ConsultationCost 600
P103 Rahul ConsultationCost 550
P104 Anu ConsultationCost 650
P105 Kiran ConsultationCost 500
P101 Ravi LabCost 1200
P102 Priya LabCost 1000
P103 Rahul LabCost 1500
P104 Anu LabCost 1100
P105 Kiran LabCost 1300
P101 Ravi PharmacyCost 800
P102 Priya PharmacyCost 900
P103 Rahul PharmacyCost 1000
P104 Anu PharmacyCost 850
P105 Kiran PharmacyCost 950

Reconstructed Treatment Dataset

Treatment PatientID PatientName ConsultationCost LabCost PharmacyCost
0 P101 Ravi 500 1200 800
1 P102 Priya 600 1000 900
2 P103 Rahul 550 1500 1000
3 P104 Anu 650 1100 850
4 P105 Kiran 500 1300 950

Cardiology Patients
P101 Ravi 25000.0
P104 Anu 28000.0

Second and Third Patients
P102 Priya Neurology
P103 Rahul Orthopedics

Insurance Bonus
1250.0
1416.67
1600.0
1400.0
1416.67

Final Bill
26250.0
29750.0
33600.0
29400.0
29750.0

Highest Revenue Department
Neurology 56666.67

Highest Bill Patient
P103 Rahul 32000.0
"""
import pandas as pd
import numpy as np

d1=pd.read_csv('patients.csv')
d2=pd.read_csv('treatments.csv')
d3=pd.read_csv('billing.csv')
d4=pd.read_csv('vitals.csv')

mer1=pd.merge(d1,d2,on="PatientID")
mer2=pd.merge(mer1,d3,on="PatientID")
merged=pd.merge(mer2,d4,on="PatientID")

print("Complete Hospital Report")
print(merged.to_string(index=False,header=False))

print("\nMissing Values")
print(merged.isnull().to_string(index=False,header=False))

print("\nRecovered Dataset")
merged["TotalBill"]=merged["TotalBill"].fillna(merged["TotalBill"].mean())
merged["BloodPressure"]=merged["BloodPressure"].interpolate()
merged=merged.drop_duplicates()
merged["TotalB"]=merged["TotalBill"].apply(lambda x:f"{x:.1f}" if x==int(x) else f"{x:.2f}")
print(merged[["PatientID","PatientName","Department","Age","TotalB","BloodPressure"]].to_string(index=False,header=False))

merged["AdmissionDate"]=pd.to_datetime(merged["AdmissionDate"])
merged.index=pd.DatetimeIndex(merged["AdmissionDate"])
print("\nMonthly Hospital Revenue")
rev=merged.resample("M")["TotalBill"].sum()
rev.index=rev.index.strftime("%Y-%m")
for month,val in rev.items():
    if val==int(val):
        val=f"{val:.1f}"
    else:
        val=f"{val:.2f}"
    print(month, val)

print("\nDepartment Revenue")
df=merged.groupby('Department')['TotalBill'].sum()
for idx,val in df.items():
    if val==int(val):
        val=f"{val:.1f}"
    else:
        val=f"{val:.2f}"
    print(idx,val)

merged["OrderDate"]=merged["AdmissionDate"].dt.strftime("%Y-%m") 
print("\nDepartment Revenue Pivot Table\n")
p=pd.pivot_table(merged, index="Department", values="TotalBill",columns=["OrderDate"],aggfunc="sum",fill_value=0)
p=p.applymap(lambda x:f"{x:.1f}" if x==int(x) else f"{x:.2f}")
p.reset_index()    
print(p.to_string())

print("\nTreatment Long Format")
melted=pd.melt(merged,id_vars=["PatientID","PatientName"],value_vars=["ConsultationCost","LabCost","PharmacyCost"],var_name="Treatment",value_name="total")
print(melted.to_string(index=False,header=False))

print("\nReconstructed Treatment Dataset\n")
re=pd.pivot_table(melted,values="total",columns="Treatment",index=["PatientID","PatientName"]).reset_index()
print(re.to_string())

print("\nCardiology Patients")
cp=merged.loc[merged.Department=="Cardiology",["PatientID","PatientName","TotalBill"]]
print(cp.to_string(index=False,header=False))

print("\nSecond and Third Patients")
print(merged.iloc[1:3][["PatientID","PatientName","Department"]].to_string(index=False,header=False))

print("\nInsurance Bonus")
ib=np.array(merged["TotalBill"])*0.05
for i in ib:
    if i==int(i):
        print(f"{i:.1f}")
    else:
        print(f"{i:.2f}")

print("\nFinal Bill")
fb=np.array(merged["TotalBill"])+ib
for i in fb:
    if i==int(i):
        print(f"{i:.1f}")
    else:
        print(f"{i:.2f}")
 
print("\nHighest Revenue Department")
print(df.idxmax(),np.round(df.max(),2))

print("\nHighest Bill Patient")
maxi=merged[["PatientID","PatientName","TotalBill"]].sort_values(by="TotalBill",ascending=False)
pid,name,bill=maxi.iloc[0]
print(pid,name,bill)
