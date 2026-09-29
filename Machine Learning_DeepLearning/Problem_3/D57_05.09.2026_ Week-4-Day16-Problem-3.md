PROJECT 13 — ENTERPRISE LOGISTICS & FLEET DELAY ANALYTICS
---------------------------------------------------------

Platform: Google Colab
Language: Python
Libraries: Pandas, NumPy
Submission: Google Colab Notebook

Problem Statement:
-------------------
A national logistics firm struggles with delayed shipments across regions. 
Currently, regional managers evaluate shipping delays using simple rule-based thresholds.
You are tasked with integrating 3 distinct relational data sources (Shipments, Fleet Metadata, and Regional Weather Logs)
to analyze delay dynamics, evaluate rule-based accuracy, and 
establish feature-label matrices for future ML deployment.


Input Files & Data Setup
---------------------------
import pandas as pd
import numpy as np

# File 1: Shipments Data (50 Records)
shipments_data = {
    'Shipment_ID': [f'SHP_{100+i}' for i in range(50)],
    'Vehicle_ID': [f'VEH_{(i%10)+1}' for i in range(50)],
    'Region_ID': [f'REG_{(i%5)+1}' for i in range(50)],
    'Distance_KM': [120, 450, 80, 600, 310, 150, 520, 210, 750, 90, 340, 180, 620, 290, 410, 110, 800, 230, 500, 140, 380, 260, 710, 190, 440, 160, 680, 220, 530, 130, 360, 270, 740, 170, 490, 150, 650, 240, 580, 200, 420, 280, 790, 180, 460, 210, 630, 250, 510, 300],
    'Cargo_Weight_Tons': [5.2, 18.0, 2.1, 22.5, 12.0, 4.5, 19.8, 8.1, 24.0, 3.0, 14.2, 6.0, 21.0, 10.5, 16.0, 4.0, 25.0, 7.5, 18.5, 5.0, 13.5, 9.0, 23.0, 6.5, 17.0, 5.5, 22.0, 8.0, 19.0, 4.8, 13.0, 9.5, 24.5, 6.2, 17.5, 5.8, 21.5, 8.5, 20.0, 7.0, 15.5, 10.0, 24.8, 6.8, 16.5, 7.8, 21.2, 8.8, 18.8, 11.0],
    'Actual_Delay_Hours': [0.5, 4.2, 0.0, 6.5, 1.2, 0.0, 5.1, 0.8, 8.0, 0.0, 2.5, 0.2, 7.1, 1.0, 3.8, 0.0, 9.2, 0.5, 4.8, 0.1, 2.8, 0.9, 7.8, 0.3, 3.5, 0.1, 6.9, 0.6, 5.2, 0.0, 2.1, 0.7, 8.5, 0.2, 4.1, 0.0, 6.2, 0.8, 5.5, 0.4, 3.0, 1.1, 8.9, 0.3, 3.9, 0.7, 6.0, 1.0, 4.9, 1.5],
    'Is_Delayed': ['No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
}

# File 2: Fleet Metadata (10 Records)
fleet_data = {
    'Vehicle_ID': [f'VEH_{i}' for i in range(1, 11)],
    'Vehicle_Age_Years': [2, 8, 1, 12, 5, 3, 9, 4, 11, 2],
    'Maintenance_Score': [95, 62, 98, 45, 78, 88, 55, 82, 48, 91],
    'Driver_Experience_Yrs': [8, 3, 12, 2, 6, 9, 4, 7, 1, 10]
}

# File 3: Regional Weather Logs (5 Records)
weather_data = {
    'Region_ID': [f'REG_{i}' for i in range(1, 6)],
    'Weather_Condition': ['Clear', 'Heavy Rain', 'Fog', 'Clear', 'Storm'],
    'Traffic_Congestion_Index': [2.1, 8.5, 6.2, 3.0, 9.1]
}

df_shipments = pd.DataFrame(shipments_data)
df_fleet = pd.DataFrame(fleet_data)
df_weather = pd.DataFrame(weather_data)


TASKS TO IMPLEMENT
-----------------

TASK 1 — Multi-Source Data Merging: Join df_shipments, df_fleet, and df_weather on relational primary 
keys (Vehicle_ID, Region_ID) to build an integrated enterprise dataset.  

TASK 2 — Fleet Operational Profiling: Compute row count, total merged columns, memory footprint, 
and inspect schema data types. 

TASK 3 — Dynamic Feature & Target Separation: Extract numerical/categorical features while dropping non-predictive keys (Shipment_ID, Vehicle_ID, Region_ID). Define Is_Delayed as target.  

TASK 4 — Target Imbalance & Delay Distribution: Calculate the proportions of Is_Delayed (Yes vs. No) and calculate mean Distance_KM and Maintenance_Score grouped by target label.  

TASK 5 — Multi-Factor Rule Engine Evaluation: Execute enterprise rule: IF (Distance_KM > 400 AND Maintenance_Score < 60) OR Weather_Condition IN ['Storm', 'Heavy Rain'] THEN Prediction = 'Yes' ELSE 'No'. 

TASK 6 — Rule Confusion & Accuracy Assessment: Compute rule accuracy, total correct predictions, false positives, and false negatives.  

TASK 7 — Operational Failure Analysis: Identify complex edge cases where the rule failed and document why static conditional checks fall short of machine learning models. 


EXPECTED FINAL OUTPUT
-----------------------

========== ENTERPRISE LOGISTICS DELAY ANALYTICS ==========

Integrated Dataset Records : 50
Total Combined Features    : 11
Target Class Distribution   : No = 27 (54.0%), Yes = 23 (46.0%)

Group Metrics (Delayed vs On-Time):
- Mean Distance            : Delayed = 582.61 KM  | On-Time = 233.70 KM
- Mean Vehicle Maintenance : Delayed = 52.87 Score | On-Time = 85.19 Score

Rule Engine Evaluation:
- Rule Accuracy            : 92.00%
- False Positives          : 2
- False Negatives          : 2

Conclusion:
Multi-table integration reveals that severe weather and low maintenance score interact non-linearly with distance. An ML algorithm dynamically weights these interactions without hand-coded threshold rules.