import streamlit as st
import pandas as pd
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
import os

# Excel file path
budget_file = 'budgetTracker.xlsx'

# Function to create the Excel file if it doesn't exist
def create_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    ws.append(["Date", "Category", "Description", "Amount"])
    wb.save(budget_file)

# Function to read budget data into a DataFrame
def read_budget():
    if not os.path.exists(budget_file):
        create_excel()
    df = pd.read_excel(budget_file)
    return df

# Function to write a new entry
def add_entry(date, category, description, amount):
    df = read_budget()
    new_row = pd.DataFrame([[date, category, description, amount]], columns=df.columns)
    if df.empty:
        updated_df = new_row
    else:
        updated_df = pd.concat([df, new_row], ignore_index=True)

    updated_df.to_excel(budget_file, index=False)

# Function to show summary
def show_summary():
    df = read_budget()
    income = df[df['Category'].str.lower() == 'income']['Amount'].sum()
    expense = df[df['Category'].str.lower() == 'expense']['Amount'].sum()
    balance = income - expense
    st.metric("💰 Total Income", f"${income:.2f}")
    st.metric("💸 Total Expense", f"${expense:.2f}")
    st.metric("📊 Balance", f"${balance:.2f}")

# Streamlit App Layout
st.title("📒 Budget Tracker")

menu = st.sidebar.radio("Menu", ["Add Entry", "Summary", "View All"])

if menu == "Add Entry":
    st.subheader("➕ Add New Entry")
    with st.form("entry_form"):
        date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", ["Income", "Expense"])
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        submit = st.form_submit_button("Add Entry")
        
        if submit:
            add_entry(date.strftime("%Y-%m-%d"), category, description, amount)
            st.success("Entry added successfully!")

elif menu == "Summary":
    st.subheader("📊 Summary Report")
    show_summary()

elif menu == "View All":
    st.subheader("📄 All Budget Entries")
    df = read_budget()
    st.dataframe(df)