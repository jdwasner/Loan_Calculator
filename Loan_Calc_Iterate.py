"""
Created by Justin Wasner
Created On: Sat Dec 23 2023
Updated: Sat Dec 27 2025

Instructions:
*Ensure the .venv is activated in your terminal before running the script.*
    - Activate Virtual Env via ".\.venv\Scripts\Activate.ps1" in terminal
    
1. Input your loan information in 'Loan Info.csv' in the same directory as this script.
2. Adjust user inputs below as needed (monthly payment, date range).
3. Run the script to generate amortization tables and summary reports.
    - View Export Tables in the 'Export' folder created in the script directory.


"""
#%% Import Stuff

import sys
import os

# Get the folder path of the current script
folder_path = os.path.dirname(os.path.abspath(__file__))

# Add to sys.path if not already present
if folder_path not in sys.path:
    sys.path.insert(0, folder_path)


from Loan_Calc_FNs import *
import numpy as np
import pandas as pd

#%% User Inputs and Setup ~~~~~~~~~~~~~~~~~~~~

#Set Monthly Total
Payment = 2000

#Date Range
Start_Date = '2024-01-01'
End_Date = '2030-01-01'

#Set Starting Values for Weigths
weight_rate = 1.0
weight_monthly = 0.0
weight_total = 0.0

#Make range of payment totals to iterate over
Payment_Range = np.arange(1400,3000,100)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% Import Loan Info

path = os.path.dirname(os.path.abspath(__file__))
Loan_Info = pd.read_csv(os.path.join(path, 'Loan Info.csv'))

#%% Weight Distribution Iteration

#Make range of weights for rate and total
weight_rate_range = np.arange(0,1.05,0.05).tolist()
weight_rate_range = [round(val, 3) for val in weight_rate_range]
weight_total_range = sorted(weight_rate_range, reverse=True)

#Make weight coordinates (weight_rate, weight_total)
coordinates = list(zip(weight_rate_range, weight_total_range))

#Make empty df to store results
df_iter_table = pd.DataFrame(columns=['rate_weight','weight_total','Intrest_Total','Payments_Total', 'Months'])
df_iter_Priority = pd.DataFrame(columns = range(8))

#Iterate through coordinates
for coord in coordinates:
    print(coord)
    weight_rate = coord[0]
    weight_total = coord[1]
    
    #Pass coords, weight and loan info to fn
    result = Loan_Table(weight_rate, weight_monthly, weight_total, Payment, Loan_Info, Start_Date, End_Date)
    
    #Store fn results
    result_summary = result[0]
    result_table = result[1]
    result_months = result[3]
    intrest_total = result_summary.loc['Intrest','Sum']
    payment_total = result_summary.loc['Payment','Sum']
    new_row = {'rate_weight':weight_rate, 'weight_total':weight_total, 'Intrest_Total': intrest_total, 'Payments_Total':payment_total, 'Months':result_months}
    df_iter_table.loc[len(df_iter_table)] = new_row
    df_iter_Priority.loc[len(df_iter_Priority)] = result[2]
    
#%% Payment Range Iteration

#Make empty df to store results
df_iter_Payment = pd.DataFrame(columns = ['Monthly', 'Intrest_Total', 'Payments_Total', 'Months'])

#Input the best rates from prev iteration
#weight_rate = 1.0
#weight_monthly = 0.0
#weight_total = 0.0

for i in Payment_Range:
    
    print(i)
    
    result = Loan_Table(weight_rate, weight_monthly, weight_total, i, Loan_Info, Start_Date, End_Date)
    
    result_summary = result[0]
    result_table = result[1]
    result_months = result[3]
    
    intrest_total = result_summary.loc['Intrest','Sum']
    payment_total = result_summary.loc['Payment','Sum']
    
    new_row = {'Monthly':i,'Intrest_Total': intrest_total, 'Payments_Total':payment_total, 'Months':result_months}
    
    df_iter_Payment.loc[len(df_iter_Payment)] = new_row
    
#%% Save Results
# Create Export folder if it doesn't exist
export_folder = os.path.join(path, 'Export')
os.makedirs(export_folder, exist_ok=True)

df_iter_Payment.to_csv(os.path.join(export_folder, 'Monthly vs Total Cost.csv'))
df_iter_Priority.to_csv(os.path.join(export_folder, 'Loan Order Iterations.csv'))

best_table = Loan_Table(weight_rate, weight_monthly, weight_total, 2000, Loan_Info, Start_Date, End_Date)

best_table[1].to_csv(os.path.join(export_folder, 'Amortization Table.csv'))
best_table[0].to_csv(os.path.join(export_folder, 'Summary.csv'))
df_iter_table.to_csv(os.path.join(export_folder, 'Weight Iterations.csv'))



#%% Single Calculation

weight_rate = 1.0
weight_monthly = 0.0
weight_total = 0.0

total_pay = 2000

Example_Export = Loan_Table(weight_rate, weight_monthly, weight_total, total_pay, Loan_Info, Start_Date, End_Date)
    
    
    
    
    
    
    
    
    
    