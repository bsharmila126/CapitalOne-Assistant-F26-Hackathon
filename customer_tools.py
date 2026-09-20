import pandas as pd

# Import pandas so we can work with the CSV file as a DataFrame


# Load the cleaned customer dataset
clean = pd.read_csv("data/customers_clean.csv")

# Read the cleaned CSV file and store it in a DataFrame called clean


# Create a surplus status column
clean["surplus_status"] = "Positive surplus"

# Start by labeling every customer as having a positive surplus


clean.loc[
    clean["monthly_surplus_inr"] < 0,
    "surplus_status"
] = "Negative surplus"

# Find customers whose monthly surplus is below 0
# and change their surplus status to "Negative surplus"



# -------------------------
# SUMMARIZE THE DATASET
# -------------------------

def summarize(df):

    # Create a function that summarizes the whole dataset


    if df is None or df.empty:
        return {
            "error": "Dataset is empty."
        }

    # Check that the dataset exists and is not empty
    # If it is empty, return an error instead of crashing


    total_customers = len(df)

    # Count the total number of customers


    average_household_income = df["household_monthly_income_inr"].mean()

    # Calculate the average household monthly income


    average_total_expenses = df["total_monthly_expenses_inr"].mean()

    # Calculate the average monthly expenses


    average_monthly_surplus = df["monthly_surplus_inr"].mean()

    # Calculate the average amount of money left after expenses


    negative_surplus_count = (
        df["monthly_surplus_inr"] < 0
    ).sum()

    # Count how many customers spend more than their household income


    negative_surplus_percent = (
        negative_surplus_count / total_customers
    ) * 100

    # Calculate what percent of customers have a negative surplus


    average_total_debt = df["total_debt_inr"].mean()

    # Calculate the average total debt


    average_credit_score = df["credit_score"].mean()

    # Calculate the average credit score


    average_emergency_fund_months = (
        df["emergency_fund_months"].mean()
    )

    # Calculate the average number of emergency-fund months


    high_dti_count = (
        df["debt_to_income_ratio_pct"] >= 40
    ).sum()

    # Count customers whose debt-to-income ratio is 40% or higher


    high_dti_percent = (
        high_dti_count / total_customers
    ) * 100

    # Calculate what percent of customers have high debt-to-income


    return {
        "total_customers": total_customers,

        "average_household_income": round(
            average_household_income, 2
        ),

        "average_total_expenses": round(
            average_total_expenses, 2
        ),

        "average_monthly_surplus": round(
            average_monthly_surplus, 2
        ),

        "negative_surplus_count": int(
            negative_surplus_count
        ),

        "negative_surplus_percent": round(
            negative_surplus_percent, 2
        ),

        "average_total_debt": round(
            average_total_debt, 2
        ),

        "average_credit_score": round(
            average_credit_score, 2
        ),

        "average_emergency_fund_months": round(
            average_emergency_fund_months, 2
        ),

        "high_dti_count": int(
            high_dti_count
        ),

        "high_dti_percent": round(
            high_dti_percent, 2
        )
    }

    # Return all the calculated values in one dictionary
    # round(..., 2) keeps numbers to 2 decimal places
    # int(...) makes counts regular whole numbers



# -------------------------
# GET ONE CUSTOMER PROFILE
# -------------------------

def get_customer_profile(customer_id):

    # Create a function that looks up one customer using their ID


    if customer_id is None or customer_id == "":
        return {
            "error": "Customer ID is required."
        }

    # Make sure the user actually entered a customer ID


    customer = clean[
        clean["customer_id"] == customer_id
    ]

    # Search the dataset for the row with that customer ID


    if customer.empty:
        return {
            "error": "Customer ID not found."
        }

    # If no matching customer exists, return an error


    customer = customer.iloc[0]

    # Take the first matching customer row
    # iloc[0] changes it from a one-row DataFrame into a single row


    return {
        "customer_id": customer["customer_id"],

        "age": int(customer["age"]),

        "household_income": customer[
            "household_monthly_income_inr"
        ],

        "total_expenses": customer[
            "total_monthly_expenses_inr"
        ],

        "monthly_surplus": customer[
            "monthly_surplus_inr"
        ],

        "surplus_rate": customer[
            "surplus_rate_pct"
        ],

        "total_debt": customer[
            "total_debt_inr"
        ],

        "debt_payment": customer[
            "monthly_debt_payment_inr"
        ],

        "credit_score": customer[
            "credit_score"
        ],

        "emergency_fund_months": customer[
            "emergency_fund_months"
        ],

        "card_utilization": customer[
            "credit_card_utilization_pct"
        ],

        "insurance": customer[
            "insurance_coverage"
        ],

        "budgeting_behavior": customer[
            "budgeting_frequency"
        ]
    }

    # Return the most important financial information
    # about the selected customer



# -------------------------
# GET SEGMENT STATISTICS
# -------------------------

def get_segment_stats(field, value):

    # Create a function that summarizes a group of customers


    allowed_fields = [
        "age_band",
        "income_band",
        "debt_band",
        "emergency_fund_band",
        "surplus_status"
    ]

    # These are the only columns the chatbot is allowed
    # to use for segment comparisons


    if field not in allowed_fields:
        return {
            "error": "Invalid segment field."
        }

    # Stop the function if someone enters a field
    # that is not in the allowed list


    if value is None or value == "":
        return {
            "error": "Segment value is required."
        }

    # Make sure a segment value was provided


    group = clean[
        clean[field] == value
    ]

    # Filter the dataset to only customers in the requested group
    # Example: income_band = High


    if group.empty:
        return {
            "error": "No customers found for this segment."
        }

    # Return an error if the requested group does not exist


    return {
        "field": field,

        "segment": value,

        "total_customers": len(group),

        "average_income": round(
            group[
                "household_monthly_income_inr"
            ].mean(),
            2
        ),

        "average_expenses": round(
            group[
                "total_monthly_expenses_inr"
            ].mean(),
            2
        ),

        "average_surplus": round(
            group[
                "monthly_surplus_inr"
            ].mean(),
            2
        ),

        "average_debt": round(
            group[
                "total_debt_inr"
            ].mean(),
            2
        ),

        "average_credit_score": round(
            group[
                "credit_score"
            ].mean(),
            2
        ),

        "average_emergency_fund_months": round(
            group[
                "emergency_fund_months"
            ].mean(),
            2
        )
    }

    # Return summary statistics for that customer group



# -------------------------
# CHECK FINANCIAL RISK
# -------------------------

def get_financial_risk(customer_id):

    # Create a function that checks one customer
    # for different financial warning signs


    if customer_id is None or customer_id == "":
        return {
            "error": "Customer ID is required."
        }

    # Make sure a customer ID was entered


    customer = clean[
        clean["customer_id"] == customer_id
    ]

    # Search for the customer


    if customer.empty:
        return {
            "error": "Customer ID not found."
        }

    # Return an error if the customer does not exist


    customer = customer.iloc[0]

    # Get the customer's row


    risk_factors = []

    # Create an empty list where we will store
    # any financial risk factors we find


    if customer["monthly_surplus_inr"] < 0:
        risk_factors.append(
            "Negative monthly surplus"
        )

    # If expenses are higher than household income,
    # add negative monthly surplus as a risk factor


    if customer["debt_to_income_ratio_pct"] >= 40:
        risk_factors.append(
            "High debt-to-income"
        )

    # Add a warning if debt-to-income is 40% or higher


    if customer["emergency_fund_months"] < 3:
        risk_factors.append(
            "Low emergency fund"
        )

    # Add a warning if the customer has less than
    # 3 months of emergency funds


    if customer[
        "credit_card_utilization_pct"
    ] >= 50:
        risk_factors.append(
            "High card utilization"
        )

    # Add a warning if credit card utilization
    # is 50% or higher


    if customer["credit_score"] < 650:
        risk_factors.append(
            "Lower credit score"
        )

    # Add a warning if the credit score is below 650


    if str(
        customer["recent_income_shock"]
    ).lower() == "yes":
        risk_factors.append(
            "Recent income shock"
        )

    # Convert the value to text and lowercase it
    # Then check whether the customer recently had an income shock


    debt_payment_percent = (
        customer["monthly_debt_payment_inr"]
        / customer["household_monthly_income_inr"]
    ) * 100

    # Calculate what percentage of household income
    # goes toward monthly debt payments


    if debt_payment_percent >= 30:
        risk_factors.append(
            "High debt payment compared with income"
        )

    # Add a warning if debt payments use
    # 30% or more of household income


    return {
        "customer_id": customer_id,
        "risk_count": len(risk_factors),
        "risk_factors": risk_factors
    }

    # Return the customer ID,
    # the number of risk factors found,
    # and the actual list of risk factors