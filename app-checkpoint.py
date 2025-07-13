import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load or create CSV
def load_data():
    try:
        df = pd.read_csv("expenses.csv")
    except:
        columns = ["ID", "User", "Title", "Description", "Amount", "Category", "Date"]
        df = pd.DataFrame(columns=columns)
        df.to_csv("expenses.csv", index=False)
    return df

# Save Data
def save_data(df):
    df.to_csv("expenses.csv", index=False)

# App Title
st.title("💸 Expense Management System")

# Load Data
df = load_data()

# Menu
menu = ["Add Expense", "View Expenses", "Delete Expense", "Show Graphs"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Add Expense":
    st.header("➕ Add New Expense")
    user = st.text_input("User Name")
    title = st.text_input("Title")
    description = st.text_area("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    date = st.date_input("Date", datetime.now())

    if st.button("Add Expense"):
        new_id = len(df) + 1
        new_expense = {
            "ID": new_id,
            "User": user,
            "Title": title,
            "Description": description,
            "Amount": amount,
            "Category": category,
            "Date": date
        }
        df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
        save_data(df)
        st.success(f"Expense '{title}' added successfully!")

elif choice == "View Expenses":
    st.header("📄 All Expenses")
    st.dataframe(df)

elif choice == "Delete Expense":
    st.header("🗑️ Delete Expense")
    if not df.empty:
        del_id = st.number_input("Enter Expense ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            if del_id in df["ID"].values:
                df = df[df["ID"] != del_id]
                df.reset_index(drop=True, inplace=True)
                df["ID"] = range(1, len(df) + 1)
                save_data(df)
                st.success(f"Expense ID {del_id} deleted successfully!")
            else:
                st.error("Expense ID not found.")
    else:
        st.info("No expenses to delete.")

elif choice == "Show Graphs":
    st.header("📊 Expense Graphs")
    if not df.empty:
        st.subheader("Category-wise Expense Distribution")
        category_data = df.groupby("Category")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        category_data.plot.pie(autopct='%1.1f%%', ax=ax1)
        ax1.set_ylabel("")
        st.pyplot(fig1)

        st.subheader("Monthly Expense Trend")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")
        month_data = df.groupby("Month")["Amount"].sum()
        fig2, ax2 = plt.subplots()
        month_data.plot(kind="bar", ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("No expenses to show graphs.")
