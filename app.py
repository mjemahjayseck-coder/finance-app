import streamlit as st
import pandas as pd
from datetime import datetime

st.title("💰 Finance Companion")
st.subheader("Quick Expense Logger")
st.write("Log your expenses on the go as they happen.")

# Initialize the storage area inside the app if it doesn't exist yet
if "expenses_list" not in st.session_state:
    st.session_state.expenses_list = []

# --- SECTION 1: ADD NEW EXPENSE ---
with st.form("expense_form", clear_on_submit=True):
    category = st.selectbox("Select Category", ["Transport", "Food", "Shopping", "Bills", "Entertainment", "Other"])
    amount = st.number_input("Amount Spent ($)", min_value=0.0, step=0.01, format="%.2f")
    submitted = st.form_submit_button("🚀 Save Expense")
    
    if submitted:
        if amount > 0:
            new_expense = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Category": category,
                "Amount": f"${amount:.2f}"
            }
            st.session_state.expenses_list.append(new_expense)
            st.success(f"Added: {category} - ${amount:.2f}!")
        else:
            st.error("Please enter an amount greater than 0.")

st.markdown("---")

# --- SECTION 2: VIEW & DELETE ENTRIES ---
st.subheader("📊 Current Entries & Management")

if st.session_state.expenses_list:
    # Convert the running list into a structured table format to view
    df = pd.DataFrame(st.session_state.expenses_list)
    
    # Show the table interface
    st.dataframe(df, use_container_width=True)
    
    # ❌ The Delete Feature
    # Create a dropdown that lets you pick which row index number you want to wipe out
    options = [f"Row {i}: {item['Category']} ({item['Amount']})" for i, item in enumerate(st.session_state.expenses_list)]
    row_to_delete = st.selectbox("Select an entry to remove:", options=options)
    
    if st.button("❌ Delete Selected Entry", type="primary"):
        # Find the chosen index number and remove it from the list
        idx = options.index(row_to_delete)
        removed = st.session_state.expenses_list.pop(idx)
        st.warning(f"Removed: {removed['Category']} entry.")
        st.rerun()
else:
    st.info("No expenses logged yet. Add one above to get started!")
    
