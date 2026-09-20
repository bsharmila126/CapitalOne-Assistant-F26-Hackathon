# CapitalOne-Assistant-F26-Hackathon
Hackathon project

get_transactions()
summarize(df)
get_spending(category, days)
project_savings(goal, months)

## Data Cleaning

The original dataset contained financial values in Indian Rupees (INR). For consistency with the project, these values were converted to U.S. Dollars (USD).

Exchange rate used: **1 INR = 0.010 USD**  
Date used: **September 19, 2026**

The following columns were converted from INR to USD:

- monthly_income_inr
- household_monthly_income_inr
- rent_or_emi_inr
- food_expense_inr
- utilities_expense_inr
- transport_expense_inr
- healthcare_expense_inr
- education_expense_inr
- discretionary_expense_inr
- total_monthly_expenses_inr
- monthly_debt_payment_inr
- total_debt_inr
- unexpected_expense_inr_12m
- liquid_assets_inr
- investment_amount_inr

After conversion, these columns were renamed from `_inr` to `_usd` and rounded to whole dollar values.

Percentages, credit scores, month counts, loan counts, and 1–10 score columns were left unchanged.

The original `monthly_savings_inr` and `savings_rate_pct` columns were not used because they contained inconsistent values. A new `monthly_surplus_usd` column was calculated as household monthly income minus total monthly expenses.

A new `surplus_rate_pct` column was calculated as monthly surplus divided by household monthly income.

column names: 
customer_id
age
marital_status
education_level
department
employment_type
job_level
years_of_experience
years_at_company
city_tier
number_of_dependents
monthly_income_usd
household_monthly_income_usd
housing_status
rent_or_emi_usd
food_expense_usd
utilities_expense_usd
transport_expense_usd
healthcare_expense_usd
education_expense_usd
discretionary_expense_usd
total_monthly_expenses_usd
monthly_savings_usd
savings_rate_pct
loan_count
monthly_debt_payment_usd
total_debt_usd
debt_to_income_ratio_pct
credit_card_utilization_pct
credit_score
missed_payment_count_12m
late_bill_payment_count_12m
unexpected_expense_usd_12m
liquid_assets_usd
emergency_fund_months
investment_amount_usd
retirement_contribution_pct
insurance_coverage
financial_product_count
budgeting_frequency
expense_tracking_frequency
financial_literacy_score
financial_goal_clarity_score
financial_planning_horizon_months
impulse_spending_score
risk_tolerance_level
digital_finance_usage_score
payment_behavior_score
income_stability_score
job_security_perception_score
recent_income_shock
family_financial_support
financial_advisor_access
sleep_disruption_days_per_month
productivity_impact_score
finance_related_absence_days_12m
financial_wellness_program_participation
preferred_financial_support_channel
target_financial_wellbeing_category

Total monthly expenses already include monthly debt payments. Debt payment is also displayed separately when explaining a customer's spending. Emergency fund months are based on essential expenses plus debt payments. Discretionary spending is not included in the emergency fund calculation. Debt-to-income ratio is based on household monthly income.
The dataset caps debt-to-income values at 85%.


##UI, Deployment, and Testing
- Built the Streamlit user interface for the financial advisor chatbot
- Implemented the chat interface and session-based conversation history
- Added quick-action buttons for common financial questions
- Integrated the frontend with the chatbot response flow
- Tested error handling and user interactions
- Tested the application on desktop and mobile devices
- Tested responsive behavior in portrait and landscape modes
- Deployed and tested the application through Streamlit



