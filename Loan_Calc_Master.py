# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:23:16 2023

@author: u102720
"""

import Loan_Calc_FNs as FNs
import pandas as pd
import os
import numpy as np

#%%


def Loan_Table(weight_rate, weight_monthly, weight_total, Total_Payment):

    
#%%
    path = os.path.dirname(__file__)
    
    #User Inputs
    #weight_rate = 0.5
    #weight_monthly = 0.0
    #weight_total = 0.5

    #Total_Payment = 2000
    
    Loan_Info = pd.read_csv(path+'\\Loan Info.csv')
    
    df_loan = Loan_Info
    df_loan['nper'] = df_loan.apply(FNs.nper_calc, axis=1)
    df_loan['Total_Max'] = df_loan['nper']*df_loan['Monthly']
    df_loan['Rank_Rate'] = (df_loan['Rate'].rank())*weight_rate
    df_loan['Rank_Monthly'] = (df_loan['Monthly'].rank())*weight_monthly
    df_loan['Rank_Total'] = (df_loan['Current'].rank(ascending=False))*weight_total
    df_loan['Score'] = df_loan[['Rank_Rate','Rank_Monthly','Rank_Total']].sum(axis=1)
    df_loan = df_loan.sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    Priority = df_loan['Loan ID']
    
    
    
    date_range = pd.date_range(start = '2024-01-01', end = '2037-01-01', freq='MS')
    df_loan_table = pd.DataFrame(index=date_range)
    
    df_loan_table['Total Payment'] = Total_Payment
    df_loan_table = df_loan_table.reset_index(drop=False).rename(columns={'index':'Date'})
    Payment_Cols = set()
    
    #%%
        
    for loan in Priority:
        df_loan_table[loan+' Payment'] = df_loan.loc[df_loan['Loan ID']==loan, 'Monthly'].values[0]
        df_loan_table[loan+' Intrest'] = None
        df_loan_table[loan+' Remaining'] = None
        Payment_Cols.add(loan+ ' Payment')
        
    for loan in Priority:
        df_loan_table.loc[0, loan+' Remaining'] = df_loan.loc[df_loan['Loan ID']==loan, 'Current'].values[0]
        df_loan_table.loc[0, loan+' Payment'] = 0
    
    
    ###Make initial loan table with no payment shifting (table_RAW)
    for loan in Priority:
        #print(loan)    
    
        for index, row in df_loan_table.iterrows():
            if index > 0:
                #print(f'index {index}')
                
                    
                current_payment = df_loan_table.loc[index , loan + ' Payment']
                total_payment = df_loan_table.loc[index, 'Total Payment']
    
                
                prev_remaining = df_loan_table.loc[index - 1, loan + ' Remaining']
                loan_rate = ((df_loan.loc[df_loan['Loan ID']==loan, 'Rate'].values[0])/12)
                
                
                df_loan_table.loc[index, loan+' Intrest'] = prev_remaining * loan_rate
                current_intrest = df_loan_table.loc[index , loan + ' Intrest']
                
                df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - current_payment
                current_remaining = df_loan_table.loc[index, loan+' Remaining']
            
                if current_remaining < 0:
                    df_loan_table.loc[index , loan + ' Payment'] = prev_remaining + current_intrest
                    new_current_payment = df_loan_table.loc[index , loan + ' Payment']
                    
                    df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - new_current_payment
    #%%
    
    df_loan_table_RAW = df_loan_table.copy()           
    
    ### Correct raw table with new payment shifting
    for loan in Priority:
        #print(loan)    
    
        for index, row in df_loan_table.iterrows():
            if index > 0:
                #print(f'index {index}')
                
                
                if loan == Priority[0]:
                    #print(f'active loan {loan}')
                    
                    current_payment = df_loan_table.loc[index , loan + ' Payment']
                    total_payment = df_loan_table.loc[index, 'Total Payment']
                    other_payments_total = sum(row[col] for col in Payment_Cols)-current_payment
                    df_loan_table.loc[index, loan + ' Payment'] = total_payment-other_payments_total
                    updated_payment = df_loan_table.loc[index , loan + ' Payment']
                    
                    prev_remaining = df_loan_table.loc[index - 1, loan + ' Remaining']
                    loan_rate = ((df_loan.loc[df_loan['Loan ID']==loan, 'Rate'].values[0])/12)
                    
                    
                    df_loan_table.loc[index, loan+' Intrest'] = prev_remaining * loan_rate
                    current_intrest = df_loan_table.loc[index , loan + ' Intrest']
                    
                    df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - updated_payment
                    current_remaining = df_loan_table.loc[index, loan+' Remaining']
                
                    if current_remaining < 0:
                        df_loan_table.loc[index , loan + ' Payment'] = prev_remaining + current_intrest
                        new_current_payment = df_loan_table.loc[index , loan + ' Payment']
                        
                        df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - new_current_payment
                else:
                    Loan_Index = df_loan.loc[df_loan['Loan ID'] == loan].index.values[0]
                    Prev_Loan = df_loan.loc[Loan_Index-1,'Loan ID']
                    
                    prev_loan_payment = df_loan_table.loc[index, Prev_Loan+' Remaining']
                    
                
                    #Trigger for next loan to start
                    if prev_loan_payment == 0:
                        current_payment = df_loan_table.loc[index , loan + ' Payment']
                        total_payment = df_loan_table.loc[index, 'Total Payment']
                        other_payments_total = sum(row[col] for col in Payment_Cols)-current_payment
                        df_loan_table.loc[index, loan + ' Payment'] = total_payment-other_payments_total
                        updated_payment = df_loan_table.loc[index , loan + ' Payment']
                        
                        prev_remaining = df_loan_table.loc[index - 1, loan + ' Remaining']
                        loan_rate = ((df_loan.loc[df_loan['Loan ID']==loan, 'Rate'].values[0])/12)
                        
                        
                        df_loan_table.loc[index, loan+' Intrest'] = prev_remaining * loan_rate
                        current_intrest = df_loan_table.loc[index , loan + ' Intrest']
                        
                        df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - updated_payment
                        current_remaining = df_loan_table.loc[index, loan+' Remaining']
                    
                        if current_remaining < 0:
                            df_loan_table.loc[index , loan + ' Payment'] = prev_remaining + current_intrest
                            new_current_payment = df_loan_table.loc[index , loan + ' Payment']
                            
                            df_loan_table.loc[index, loan+' Remaining'] = prev_remaining + current_intrest - new_current_payment
    
    
    
    df_loan_table_final = df_loan_table.copy()
    
    df_loan_table_final['Sum Check'] = df_loan_table_final[Payment_Cols].sum(axis=1)
 
 #%%   
 
    df_sum = pd.DataFrame({'Sum':df_loan_table_final.sum()})
    df_sum = df_sum.reset_index(drop=False)
    df_sum = df_sum[df_sum['index']!='Sum Check']
    df_sum = df_sum[df_sum['index']!='Total Payment']
    df_sum['Category'] = df_sum['index'].str.split().str[-1]
    #df_sum['Test'] = df_sum['index'].str.split().str[0]
    
    df_sum['Loan'] = np.nan
    for loan in Priority:
        df_sum['Loan'] = np.where(df_sum['index'].str.contains(loan), loan, df_sum['Loan'])
        
    df_sum_pivot = df_sum.pivot(index='Category', columns = 'Loan', values = 'Sum')
    df_sum_pivot = df_sum_pivot.drop(index='Remaining')
    df_sum_pivot['Sum'] = df_sum_pivot.sum(axis=1)

    months = len(df_loan_table_final[df_loan_table_final['Sum Check'] != 0])
    
#%%
    return df_sum_pivot, df_loan_table_final, Priority, months







