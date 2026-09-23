import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the budget dataframe
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Expense Category', 'Amount', 'Details']
    )

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expenses.columns
    )
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_expense],
        ignore_index=True
    )

def load_expenses():
    uploaded_file = st.file_uploader("Upload Expense File", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)

def save_expenses():
    st.session_state.expenses.to_csv('my_expenses.csv', index=False)
    st.success("Expense data saved successfully!")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(
            data=st.session_state.expenses,
            x='Expense Category',
            y='Amount',
            ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expense data available!")

st.title('Personal Expense Manager')

with st.sidebar:
    st.header('Enter New Expense')

    date = st.date_input('Expense Date')

    category = st.selectbox(
        'Select Category',
        ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']
    )

    amount = st.number_input(
        'Expense Amount',
        min_value=0.0,
        format="%.2f"
    )

    description = st.text_input('Expense Details')

    if st.button('Add Expense'):
        add_expense(date, category, amount, description)
        st.success('Expense added successfully!')

    st.header('File Management')

    if st.button('Save Data'):
        save_expenses()

    if st.button('Import Data'):
        load_expenses()

st.header('Expense Records')
st.write(st.session_state.expenses)

st.header('Expense Analysis')

if st.button('Show Expense Chart'):
    visualize_expenses()

st.header('Conclusion')