import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Personal Finance",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Personal Finance Dashboard")
st.write("Track your income, expenses, and monthly budget.")

# Set Monthly Income
st.subheader("💰 Set Monthly Income")

total_income = st.number_input(
    "Enter Monthly Income (₹)",
    min_value=0,
    value=30000,
    step=1000
)

# Sample data
data = {
    "Category": ["Food", "Transport", "Shopping", "Rent", "Bills"],
    "Amount": [4000, 2000, 3000, 8000, 1500]
}

import os

if os.path.exists("expenses.csv"):
    df = pd.read_csv("expenses.csv")
else:
    df = pd.DataFrame(data)

# Sample financial values

total_expenses = df["Amount"].sum()
remaining_balance = total_income - total_expenses

# Dashboard cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"₹{total_income:,}")
col2.metric("Total Expenses", f"₹{total_expenses:,}")
col3.metric("Remaining Balance", f"₹{remaining_balance:,}")

st.divider()
# Filter expenses by category
st.subheader("🔎 Filter Expenses")

categories = ["All"] + df["Category"].tolist()

selected_category = st.selectbox(
    "Select Expense Category",
    categories
)

if selected_category == "All":
    filtered_df = df
else:
    filtered_df = df[df["Category"] == selected_category]

# Expense chart
st.subheader("📊 Category-wise Expenses")

fig, ax = plt.subplots(figsize=(5, 2.5))
ax.bar(filtered_df["Category"], filtered_df["Amount"], width=0.5)

ax.set_title("Expenses by Category", fontsize=12)
ax.set_xlabel("Category", fontsize=9)
ax.set_ylabel("Amount (₹)", fontsize=9)

ax.tick_params(axis="both", labelsize=8)

st.pyplot(fig, use_container_width=False)
plt.close(fig)

# Expense Prediction
st.divider()
st.subheader("🔮 Next Month Expense Prediction")

predicted_expense = total_expenses * 1.10

st.metric(
    "Estimated Next Month Expenses",
    f"₹{predicted_expense:,.0f}"
)

st.caption(
    "Demo estimate: assumes expenses increase by 10%. "
    "This is not an ML model prediction."
)
# Add New Expense
st.divider()
st.subheader("➕ Add New Expense")

with st.form("expense_form"):

    new_date = st.date_input("Expense Date")

    new_category = st.selectbox(
        "Select Category",
        ["Food", "Transport", "Shopping", "Rent", "Bills", "Other"]
    )

    new_amount = st.number_input(
        "Enter Amount (₹)",
        min_value=1.0,
        step=100.0
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_row = pd.DataFrame({
            "Date": [new_date],
            "Category": [new_category],
            "Amount": [new_amount]
        })

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("expenses.csv", index=False)

        st.success("Expense added and saved successfully!")
        st.dataframe(df, use_container_width=True)

# Download Expense Report
st.divider()
st.subheader("📥 Download Expense Report")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Expenses CSV",
    data=csv_data,
    file_name="expenses_report.csv",
    mime="text/csv"
)
# Monthly Budget Alert
st.divider()
st.subheader("🎯 Monthly Budget Alert")

monthly_budget = st.number_input(
    "Set Monthly Expense Budget (₹)",
    min_value=0,
    value=20000,
    step=1000,
    key="monthly_budget"
)

if total_expenses > monthly_budget:
    st.warning("⚠️ Your expenses have exceeded your monthly budget!")
else:
    st.success("✅ Your expenses are within your monthly budget.")
# Search Transactions
st.divider()
st.subheader("🔍 Search Transactions")

search_category = st.text_input("Enter category to search")

if search_category:
    search_results = df[
        df["Category"].str.contains(
            search_category,
            case=False,
            na=False
        )
    ]
else:
    search_results = df

st.dataframe(search_results, use_container_width=True)    
# Expense table
st.subheader("📋 Expense Details")
st.dataframe(df, use_container_width=True)

st.success("Dashboard loaded successfully!")

# Monthly Expense Trend
st.divider()
st.subheader("📈 Monthly Expense Trend")

monthly_data = pd.DataFrame({
    "Month": ["January", "February", "March", "April", "May", "June"],
    "Expenses": [12000, 14000, 11000, 16000, 13500, 17000]
})

fig, ax = plt.subplots(figsize=(5, 2.5))

ax.plot(
    monthly_data["Month"],
    monthly_data["Expenses"],
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Expenses (₹)")
ax.tick_params(axis="x", rotation=45, labelsize=8)

plt.tight_layout()
st.pyplot(fig, use_container_width=False)
plt.close(fig)
# Income vs Expenses Chart
st.divider()
st.subheader("💵 Income vs Expenses")

comparison_data = pd.DataFrame({
    "Type": ["Income", "Expenses"],
    "Amount": [total_income, total_expenses]
})

fig, ax = plt.subplots(figsize=(5, 2.5))

ax.bar(comparison_data["Type"], comparison_data["Amount"], width=0.5)

ax.set_ylabel("Amount (₹)")
ax.set_title("Income vs Expenses")

plt.tight_layout()
st.pyplot(fig, use_container_width=False)
plt.close(fig)
# Income and Expense Distribution
st.divider()
st.subheader("🥧 Income Distribution")

fig, ax = plt.subplots(figsize=(5, 3))

ax.pie(
    [total_expenses, max(total_income - total_expenses, 0)],
    labels=["Expenses", "Remaining Balance"],
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title("Income Usage")

plt.tight_layout()
st.pyplot(fig, use_container_width=False)
plt.close(fig)
# Expense Summary
st.divider()
st.subheader("📊 Expense Summary")

st.write("Total Transactions:", len(df))
st.write("Average Expense: ₹", round(df["Amount"].mean(), 2))

if not df.empty:
    highest_expense = df.loc[df["Amount"].idxmax()]

    st.write("Highest Expense Category:", highest_expense["Category"])
    st.write("Highest Expense Amount: ₹", highest_expense["Amount"])
else:
    st.info("No expenses available.")