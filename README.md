# Loan Calculator
## Purpose
This repository contains Python scripts for personal finance loan calculators.

## Contents
- Loan Info.csv
- Loan_Calc_FNs.py
- Loan_Calc_Iterate.py

## Instructions:
*Ensure the .venv is activated in your terminal before running the script.*
- Activate Virtual Env via ".\.venv\Scripts\Activate.ps1" in terminal
    
1. Input your loan information in 'Loan Info.csv' in the same directory as this script. 
3. Adjust user inputs below as needed (monthly payment, date range).
4. Run the script to generate amortization tables and summary reports.
    - View Export Tables in the 'Export' folder created in the script directory.
  
## Export Contents
- **Amortization Table.csv** - Month-by-month breakdown of payments, interest, and remaining balance for each loan
- **Loan Order Iterations.csv** - Different prioritization strategies tested
- **Monthly vs Total Cost.csv** - Analysis of different monthly payment amounts
- **Summary.csv** - Total interest and payments per loan
- **Weight Iterations.csv** - Results from testing different weighting strategies

### Example: Monthly vs Total Cost.csv
Compares different monthly payment amounts and their impact on total interest:

| Monthly | Interest Total | Payments Total | Months |
|---------|----------------|----------------|--------|
| $1,400  | $11,857        | $79,482        | 57     |
| $1,600  | $9,497         | $77,122        | 49     |
| $1,800  | $7,915         | $75,539        | 42     |
| $2,000  | $6,819         | $74,443        | 38     |
| $2,200  | $6,011         | $73,636        | 34     |

*Higher monthly payments = less interest paid and faster payoff*

### Example: Summary.csv
Shows total interest paid and total payments for each loan at the user input monthly payment:

| Category | Loan01 | Loan02 | Loan03 | Loan04 | Loan05 | Loan06 | Loan07 | Loan08 | Sum |
|----------|--------|--------|--------|--------|--------|--------|--------|--------|------|
| Interest | $468   | $2,698 | $700   | $430   | $532   | $951   | $543   | $496   | $6,819 |
| Payment  | $4,261 | $26,106| $5,740 | $5,291 | $5,883 | $15,263| $5,866 | $6,032 | $74,443 |

### Example: Amortization Table.csv
First few rows showing monthly payment breakdown:

| Date       | Total Payment | Loan02 Payment | Loan02 Interest | Loan02 Remaining | Loan01 Payment | Loan01 Interest | ... |
|------------|---------------|----------------|-----------------|------------------|----------------|-----------------|-----|
| 2024-01-01 | $2,000        | $0             | -               | $23,408          | $0             | -               | ... |
| 2024-02-01 | $2,000        | $1,145         | $219            | $22,482          | $85            | $24             | ... |
| 2024-03-01 | $2,000        | $1,145         | $211            | $21,547          | $85            | $24             | ... |

### Example: Weight Iterations.csv
Tests different prioritization strategies (rate weight vs. total balance weight):

| Rate Weight | Total Weight | Interest Total | Payments Total | Months |
|-------------|--------------|----------------|----------------|--------|
| 0.0         | 1.0          | $8,845         | $76,469        | 39     |
| 0.25        | 0.75         | $8,463         | $76,088        | 39     |
| 0.5         | 0.5          | $7,487         | $75,112        | 38     |
| 0.75        | 0.25         | $6,965         | $74,589        | 38     |
| 1.0         | 0.0          | $6,819         | $74,443        | 38     |

*Higher rate weight (1.0) = prioritize high-interest loans first = lowest total interest*

### Example: Loan Order Iterations.csv
Shows the payoff order for each weighting strategy tested:

| Strategy | 1st    | 2nd    | 3rd    | 4th    | 5th    | 6th    | 7th    | 8th    |
|----------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0        | Loan01 | Loan04 | Loan03 | Loan07 | Loan05 | Loan08 | Loan06 | Loan02 |
| 8        | Loan01 | Loan03 | Loan04 | Loan05 | Loan02 | Loan07 | Loan06 | Loan08 |

*Different strategies produce different loan payoff orders*
