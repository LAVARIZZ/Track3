import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def run_financial_tracker_app():
    st.title("Financial Goal Tracker")
    st.write("Answer a few questions about your spending and saving habits to help us create a budget and expense tracker for you.")

    income = st.number_input("What is your monthly income?")

    st.write("Expenses")
    rent = st.number_input("Rent/Mortgage")
    utilities = st.number_input("Utilities")
    groceries = st.number_input("Groceries")
    transportation = st.number_input("Transportation")
    other_expenses = st.number_input("Other Expenses")

    st.write("Savings")
    emergency_fund = st.number_input("Emergency Fund Savings")
    retirement_savings = st.number_input("Retirement Savings")
    other_savings = st.number_input("Other Savings")

    total_expenses = rent + utilities + groceries + transportation + other_expenses
    total_savings = emergency_fund + retirement_savings + other_savings
    # remaining_income = income - total_expenses - total_savings

    st.write("Your Budget and Savings Summary:")
    st.write(f"Total Expenses: {total_expenses}")
    st.write(f"Total Savings: {total_savings}")
    # st.write(f"Remaining Income: {remaining_income}")

    # Expense Tracker Table
    expense_data = {
        'Category': ['Rent/Mortgage', 'Utilities', 'Groceries', 'Transportation', 'Other Expenses'],
        'Amount': [rent, utilities, groceries, transportation, other_expenses]
    }
    expense_df = pd.DataFrame(expense_data)
    st.write("Expense Tracker:")
    st.dataframe(expense_df)

    # Savings Tracker Table
    savings_data = {
        'Category': ['Emergency Fund', 'Retirement Savings', 'Other Savings'],
        'Amount': [emergency_fund, retirement_savings, other_savings]
    }
    savings_df = pd.DataFrame(savings_data)
    st.write("Savings Tracker:")
    st.dataframe(savings_df)

    # Visualize Expense Distribution with Pie Chart
    expense_labels = expense_df['Category']
    expense_values = expense_df['Amount']
    plt.figure(figsize=(8, 8))
    plt.pie(expense_values, labels=expense_labels, autopct="%1.1f%%", startangle=140)
    plt.axis('equal')
    st.write("Expense Distribution:")
    st.pyplot(plt)

    # Budgeting Plan based on 50/30/20 Rule
    essentials_budget = income * 0.5
    non_essentials_budget = income * 0.3
    savings_budget = income * 0.2

    st.write("Budgeting Recommendation (50/30/20 Rule):")
    st.write(f"Allocate 50% of your income to Essentials: ${essentials_budget:.2f}")
    st.write(f"Allocate 30% of your income to Non-Essentials: ${non_essentials_budget:.2f}")
    st.write(f"Allocate 20% of your income to Savings: ${savings_budget:.2f}")

if __name__ == "__main__":
    # st.sidebar.title("Navigation")
    # app_mode = st.sidebar.selectbox("Choose a mode", ["Introduction", "Financial Tracker"])

    # if app_mode == "Introduction":
    #     st.sidebar.success("To view the financial tracker, select 'Financial Tracker' from the dropdown.")
    # elif app_mode == "Financial Tracker":
    #     st.sidebar.success("You're in Financial Tracker mode.")
    run_financial_tracker_app()
