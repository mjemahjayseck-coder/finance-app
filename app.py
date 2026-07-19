import streamlit as st
import pandas as pd
import datetime
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Pocket Finance Tracker", page_icon="💰", layout="centered")

# --- INITIALIZE LOCAL DATABASE ---
if not os.path.exists("expenses.csv"):
    pd.DataFrame(columns=["Date", "Category", "Amount"]).to_csv("expenses.csv", index=False)

if not os.path.exists("history.csv"):
    pd.DataFrame(columns=["Date", "Cash Out", "Cash In", "Total Expenses", "Total Revenue", "Net Profit"]).to_csv("history.csv", index=False)

# --- NAVIGATION ---
st.title("💰 Finance Companion")
menu = ["📝 Log Expense", "📊 End of Day Calculation", "📜 History Register"]
choice = st.sidebar.selectbox("Navigate Screens", menu)

today_date = datetime.date.today().strftime("%Y-%m-%d")
current_month = datetime.date.today().strftime("%Y-%m") # e.g., "2026-07"

# ==========================================
# SCREEN 1: LOG EXPENSE
# ==========================================
if choice == "📝 Log Expense":
    st.header("Quick Expense Logger")
    st.write("Log your expenses on the go as they happen.")
    
    # Updated to include Miscellaneous Expenses!
    category = st.selectbox("Select Category", ["Transport", "Food & Drinks", "Miscellaneous Expenses"])
    amount = st.number_input("Amount Spent ($)", min_value=0.0, step=1.0, format="%.2f")
    
    if st.button("🚀 Save Expense", use_container_width=True):
        if amount > 0:
            df_exp = pd.read_csv("expenses.csv")
            new_row = {"Date": today_date, "Category": category, "Amount": amount}
            df_exp = pd.concat([df_exp, pd.DataFrame([new_row])], ignore_index=True)
            df_exp.to_csv("expenses.csv", index=False)
            st.success(f"Successfully logged ${amount:.2f} under {category}!")
        else:
            st.warning("Please enter an amount greater than zero.")

# ==========================================
# SCREEN 2: END OF DAY CALCULATION
# ==========================================
elif choice == "📊 End of Day Calculation":
    st.header("End of Day Summary")
    st.write("Run your daily numbers and look at your monthly progress.")
    
    # Calculate today's logged expenses
    df_exp = pd.read_csv("expenses.csv")
    df_exp['Date'] = df_exp['Date'].astype(str)
    today_expenses = df_exp[df_exp['Date'] == today_date]['Amount'].sum()
    
    st.metric(label="Total Automated Expenses Today", value=f"${today_expenses:.2f}")
    st.markdown("---")
    
    # Input physical cash tracking numbers
    cash_out = st.number_input("Cash you LEFT home with ($)", min_value=0.0, step=1.0)
    cash_in = st.number_input("Cash you CAME BACK home with ($)", min_value=0.0, step=1.0)
    
    if st.button("🔒 Run Trigger & Close Day", use_container_width=True):
        net_profit = cash_in - cash_out
        total_revenue = net_profit + today_expenses
        
        # Save to history ledger immediately so it's included in monthly tracking
        df_hist = pd.read_csv("history.csv")
        new_summary = {
            "Date": today_date,
            "Cash Out": cash_out,
            "Cash In": cash_in,
            "Total Expenses": today_expenses,
            "Total Revenue": total_revenue,
            "Net Profit": net_profit
        }
        df_hist = pd.concat([df_hist, pd.DataFrame([new_summary])], ignore_index=True)
        df_hist.to_csv("history.csv", index=False)
        st.balloons()
        
        # --- DISPLAY DAILY REPORT ---
        st.markdown("### 📅 Today's Financial Report")
        c1, c2, c3 = st.columns(3)
        c1.metric("Expenses", f"${today_expenses:.2f}")
        c2.metric("Net Profit", f"${net_profit:.2f}")
        c3.metric("Total Revenue", f"${total_revenue:.2f}")
        
        # --- CALCULATE & DISPLAY MONTHLY REPORT ---
        st.markdown("---")
        st.markdown("### 🗓️ Current Month Cumulative Totals")
        
        # Filter histories that match the current year-month pattern
        df_hist['Date'] = df_hist['Date'].astype(str)
        df_month = df_hist[df_hist['Date'].str.startswith(current_month)]
        
        month_expenses = df_month["Total Expenses"].sum()
        month_revenue = df_month["Total Revenue"].sum()
        month_profit = df_month["Net Profit"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Month's Expenses", f"${month_expenses:.2f}")
        m2.metric("Month's Net Profit", f"${month_profit:.2f}")
        m3.metric("Month's Total Revenue", f"${month_revenue:.2f}")
        
        st.success("Day locked and summaries updated!")

# ==========================================
# SCREEN 3: HISTORY REGISTER
# ==========================================
elif choice == "📜 History Register":
    st.header("Financial History Register")
    st.write("Look back at your financial performance over time.")
    
    df_hist = pd.read_csv("history.csv")
    
    if df_hist.empty:
        st.info("Your history register is currently empty. Complete an 'End of Day' summary to see records here!")
    else:
        st.dataframe(df_hist, use_container_width=True)
        
        total_all_time_profit = df_hist["Net Profit"].sum()
        st.metric(label="🎉 Total Net Profit Overall", value=f"${total_all_time_profit:.2f}")
        import streamlit as str
from streamlit_gsheets import GSheetsConnection

# Establish the connection using the secrets we just saved
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Read existing data
df = conn.read(worksheet="Expenses", ttl=0)

st.subheader("Manage Expenses")

if not df.empty:
    # Show the latest entries so you can see what to delete
    st.dataframe(df.tail(5))
    
    # Add a button to delete the very last row
    if st.button("❌ Delete Last Entry"):
        # Remove the last row from the dataframe
        df = df.iloc[:-1]
        
        # Clear the spreadsheet worksheet and write the updated data back
        conn.update(worksheet="Expenses", data=df)
        st.success("Last entry deleted successfully!")
        st.rerun()
else:
    st.info("No entries found to delete.")
    
