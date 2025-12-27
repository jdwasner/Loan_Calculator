# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 19:23:41 2023

@author: Justin
"""

from Loan_Calc_Master import *
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

#User Inputs
weight_rate = 1.0
weight_monthly = 0.0
weight_total = 0.0

Payment = 2000

weight_rate_range = np.arange(0,1.05,0.05).tolist()
weight_rate_range = [round(val, 3) for val in weight_rate_range]
weight_total_range = sorted(weight_rate_range, reverse=True)

coordinates = list(zip(weight_rate_range, weight_total_range))

df_iter_table = pd.DataFrame(columns=['rate_weight','weight_total','Intrest_Total','Payments_Total', 'Months'])
df_iter_Priority = pd.DataFrame(columns = range(8))

for coord in coordinates:
    print(coord)
    weight_rate = coord[0]
    weight_total = coord[1]
    
    result = Loan_Table(weight_rate, weight_monthly, weight_total, Payment)
    
    result_summary = result[0]
    result_table = result[1]
    result_months = result[3]
    
    intrest_total = result_summary.loc['Intrest','Sum']
    payment_total = result_summary.loc['Payment','Sum']
    
    new_row = {'rate_weight':weight_rate, 'weight_total':weight_total, 'Intrest_Total': intrest_total, 'Payments_Total':payment_total, 'Months':result_months}
    df_iter_table.loc[len(df_iter_table)] = new_row
    df_iter_Priority.loc[len(df_iter_Priority)] = result[2]
    
   #%% 

Payment_Range = np.arange(1400,3000,100)
df_iter_Payment = pd.DataFrame(columns = ['Monthly', 'Intrest_Total', 'Payments_Total', 'Months'])

#Best Weights
weight_rate = 1.0
weight_monthly = 0.0
weight_total = 0.0

for i in Payment_Range:
    
    print(i)
    
    result = Loan_Table(weight_rate, weight_monthly, weight_total, i)
    
    result_summary = result[0]
    result_table = result[1]
    result_months = result[3]
    
    intrest_total = result_summary.loc['Intrest','Sum']
    payment_total = result_summary.loc['Payment','Sum']
    
    new_row = {'Monthly':i,'Intrest_Total': intrest_total, 'Payments_Total':payment_total, 'Months':result_months}
    
    df_iter_Payment.loc[len(df_iter_Payment)] = new_row
    
#%%
#path = os.path.dirname(__file__)
df_iter_Payment.to_csv('Export.csv')

df_iter_Priority.to_csv('Export2.csv')

best_table = Loan_Table(weight_rate, weight_monthly, weight_total, 2000)

best_table[1].to_csv('Export3.csv')
best_table[0].to_csv('Export4.csv')
df_iter_table.to_csv('Export5.csv')
    
    
    
    
    
    
    
    
    
    