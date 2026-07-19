import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finance Companion", layout="wide")

st.title("💰 Ultimate Finance Companion")
st.write("Track income, expenses, and view automated profit breakdowns.")

# Initialize storage arrays in the app memory
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# --- SECTION 1: LOG NEW TRANSACTION ---
st.subheader("📝 Log Cash Flow")
col1, col2, col3 = st.columns(3)

with col1:
    t_type = st.selectbox("Type", ["Expense", "Income"])
with col2:
    category = st.selectbox("Category", [
        "Salary/Earnings", "Business", "Transport", "Food", 
        "Shopping", "Bills", "Entertainment", "Other"
    ])
with col3:
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")

# Let users choose the date manually so they can log past/future entries accurately
selected_date = st.date_input("Transaction Date", datetime.today())

if st.button("🚀 Save Transaction", type="primary"):
    if amount > 0:
        new_entry = {
            "Date": selected_date.strftime("%Y-%m-%d"),
if st.button("🚀 Save Transaction", type="primary"):
    if amount > 0:
        new_entry = {
            "Date": selected_date.strftime("%Y-%m-%d"),
            "Type": t_type,
            "Category": category,
            "Amount": amount if t_type == "Income" else -amount
        }
        st.session_state.transactions.append(new_entry)
        st.success(f"Successfully recorded {t_type}: ${amount:.2f} under {category}!")
        st.rerun()
    else:
        st.warning("Please enter an amount greater than $0.00.")

st.markdown("---")

# Convert tracking list to DataFrame if it has entries
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Display Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}" if x >= 0 else f"-${abs(x):,.2f}")
    
    # --- SECTION 2: VIEW & DELETE ENTRIES ---
    st.subheader("📊 Live Ledger & Deletions")
    
    # Show clean overview table
    st.dataframe(df[["Date", "Type", "Category", "Display Amount"]], use_container_width=True)
    
    # Dropdown system to remove wrong entries safely
    delete_options = [f"Row {i}: {row['Date'].strftime('%Y-%m-%d')} | {row['Type']} | {row['Category']} ({row['Display Amount']})" for i, row in df.iterrows()]
    row_to_delete = st.selectbox("Select an entry to delete if entered incorrectly:", options=delete_options)
    
    if st.button("❌ Delete Selected Entry"):
        idx = delete_options.index(row_to_delete)
        removed = st.session_state.transactions.pop(idx)
        st.error("Entry deleted successfully!")
        st.rerun()
        
    st.markdown("---")
    
    # --- SECTION 3: BREAKDOWNS (DAILY, WEEKLY, MONTHLY) ---
    st.subheader("📈 Financial Breakdowns & Performance")
    
    # Setup calculation helper columns
    df['Income'] = df['Amount'].apply(lambda x: x if x > 0 else 0)
    df['Expense'] = df['Amount'].apply(lambda x: abs(x) if x < 0 else 0)
    df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time.strftime('%Y-%m-%d'))
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    
    tab1, tab2, tab3 = st.tabs(["🗓️ Daily Breakdown", "📅 Weekly Breakdown", "📆 Monthly Breakdown"])
    
    with tab1:
        st.write("### Day-by-Day Summary")
        daily_df = df.groupby('Date').agg({'Income': 'sum', 'Expense': 'sum', 'Amount': 'sum'}).reset_index()
        daily_df.columns = ['Date', 'Total Earned', 'Total Spent', 'Net Profit']
        
        # Format for clean viewing
        for col in ['Total Earned', 'Total Spent', 'Net Profit']:
            daily_df[col] = daily_df[col].apply(lambda x: f"${x:,.2f}")
        st.dataframe(daily_df, use_container_width=True)
        
    with tab2:
        st.write("### Week-by-Week Summary")
        weekly_df = df.groupby('Week').agg({'Income': 'sum', 'Expense': 'sum', 'Amount': 'sum'}).reset_index()
        weekly_df.columns = ['Week Commencing', 'Total Earned', 'Total Spent', 'Net Profit']
        
        for col in ['Total Earned', 'Total Spent', 'Net Profit']:
            weekly_df[col] = weekly_df[col].apply(lambda x: f"${x:,.2f}")
        st.dataframe(weekly_df, use_container_width=True)
        
    with tab3:
        st.write("### Month-by-Month Summary")
        monthly_df = df.groupby('Month').agg({'Income': 'sum', 'Expense': 'sum', 'Amount': 'sum'}).reset_index()
        monthly_df.columns = ['Month (YYYY-MM)', 'Total Earned', 'Total Spent', 'Net Profit']
        
        for col in ['Total Earned', 'Total Spent', 'Net Profit']:
            monthly_df[col] = monthly_df[col].apply(lambda x: f"${x:,.2f}")
        st.dataframe(monthly_df, use_container_width=True)

else:
    st.info("No logs captured yet. Start typing income or expenses above to build your dashboard!")
