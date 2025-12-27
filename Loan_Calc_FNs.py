# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:23:16 2023

@author: u102720
"""

# import Loan_Calc_FNs as FNs
import pandas as pd
import os
import numpy as np
import numpy_financial as np_fin # pip install numpy-financial

#%%

def nper_calc(row):
    """Calculate the number of periods (nper) based on the loan details."""
    return np_fin.nper(row['Rate']/12, -row['Monthly'], row['Current'])


def Loan_Table(weight_rate, weight_monthly, weight_total, Total_Payment, Loan_Info, Start_Date, End_Date):
    """
    Generate a loan amortization table with prioritized payment shifting strategy.
    
    Parameters:
        weight_rate (float): Weight for loan interest rate in prioritization.
        weight_monthly (float): Weight for monthly payment amount.
        weight_total (float): Weight for total loan amount.
        Total_Payment (float): Total payment available each month.
        
    Returns:
        df_sum_pivot (pd.DataFrame): Summary of total interest and payment per loan.
        df_loan_table_final (pd.DataFrame): Final amortization table.
        Priority (list): Ordered list of loan IDs by priority.
        months (int): Number of months where total payments were made.
    """
    
    #path = os.path.dirname(__file__)
    #Loan_Info = pd.read_csv(path+'\\Loan Info.csv')
    
    ### Determine Loan Repay Order
    df_loan = Loan_Info.copy()
    df_loan['nper'] = df_loan.apply(nper_calc, axis=1)
    df_loan['Total_Max'] = df_loan['nper']*df_loan['Monthly']
    df_loan['Rank_Rate'] = (df_loan['Rate'].rank())*weight_rate
    df_loan['Rank_Monthly'] = (df_loan['Monthly'].rank())*weight_monthly
    df_loan['Rank_Total'] = (df_loan['Current'].rank(ascending=False))*weight_total
    df_loan['Score'] = df_loan[['Rank_Rate','Rank_Monthly','Rank_Total']].sum(axis=1)
    df_loan = df_loan.sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    Priority = df_loan['Loan ID']
    
    ### Build amortization table structure
    date_range = pd.date_range(start = Start_Date, end = End_Date, freq='MS')
    df_loan_table = pd.DataFrame(index=date_range)
    
    df_loan_table['Total Payment'] = Total_Payment
    df_loan_table = df_loan_table.reset_index(drop=False).rename(columns={'index':'Date'})
    Payment_Cols = set()
    
    ### Initialize loan-specific columns
    for loan in Priority:
        df_loan_table[loan+' Payment'] = df_loan.loc[df_loan['Loan ID']==loan, 'Monthly'].values[0]
        df_loan_table[loan+' Intrest'] = None
        df_loan_table[loan+' Remaining'] = None
        Payment_Cols.add(loan+ ' Payment')
        
    for loan in Priority:
        df_loan_table.loc[0, loan+' Remaining'] = df_loan.loc[df_loan['Loan ID']==loan, 'Current'].values[0]
        df_loan_table.loc[0, loan+' Payment'] = 0
    

    ### Make initial loan table with no payment shifting (table_RAW)
    for loan in Priority:
        for index, row in df_loan_table.iterrows():
            if index > 0:
                
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
    
    ### Correct raw table with new payment shifting
    for loan in Priority:  
        for index, row in df_loan_table.iterrows():
            if index > 0:
                if loan == Priority[0]:
                    #Active (first-priority) loan payment logic
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
                    #Subordinate loan logic - trigger when previous loan paid off
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
    df_loan_table_final['Sum Check'] = df_loan_table_final[list(Payment_Cols)].sum(axis=1)  
 
    #Summarize total payments and interest
    # Fill None/NaN with 0 before summing to ensure all numeric columns are included
    df_sum = pd.DataFrame({'Sum':df_loan_table_final.infer_objects(copy=False).fillna(0).sum(numeric_only=True)})
    df_sum = df_sum.reset_index(drop=False)
    df_sum = df_sum[df_sum['index']!='Sum Check']
    df_sum = df_sum[df_sum['index']!='Total Payment']
    df_sum['Category'] = df_sum['index'].str.split().str[-1]
    #df_sum['Test'] = df_sum['index'].str.split().str[0]
    
    df_sum['Loan'] = np.nan
    for loan in Priority:
        df_sum['Loan'] = np.where(df_sum['index'].str.contains(loan), loan, df_sum['Loan'])
        
    df_sum_pivot = df_sum.pivot(index='Category', columns = 'Loan', values = 'Sum')
    if 'Remaining' in df_sum_pivot.index:
        df_sum_pivot = df_sum_pivot.drop(index='Remaining')
    df_sum_pivot['Sum'] = df_sum_pivot.sum(axis=1)

    months = len(df_loan_table_final[df_loan_table_final['Sum Check'] != 0])
    
    return df_sum_pivot, df_loan_table_final, Priority, months



