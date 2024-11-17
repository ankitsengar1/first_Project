import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('Big_Black_Money_Dataset.csv')

# Ensure the 'Date of Transaction' column is in datetime format
df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'], errors='coerce')  # Convert to datetime

# Sidebar options
st.sidebar.header("Options")
# Adding an image to the sidebar
st.sidebar.image("assets/Black Money.png", use_container_width=True)

# Add graph selection in the sidebar
graph_option = st.sidebar.radio(
    "Select a Graph to Display:",
    (
        "Transaction Volume by Country",
        "Risk Score Distribution",
        "Transaction Amount by Type",
        "Shell Companies by Industry",
        "Top Financial Institutions",
        "Risk Score Over Time",
        "High-Risk Transactions",
        "Transactions by Tax Haven Countries",
    )
)

# Sidebar filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Originating Country", df['Country'].unique())
selected_transaction_type = st.sidebar.selectbox("Select Transaction Type", df['Transaction Type'].unique())
amount_range = st.sidebar.slider(
    "Select Transaction Amount Range (USD)",
    int(df['Amount (USD)'].min()),
    int(df['Amount (USD)'].max()),
    (10000, 1000000)
)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date of Transaction'].min(), df['Date of Transaction'].max())
)

# Ensure the date_range is in datetime format
date_range = [pd.to_datetime(date) for date in date_range]

# Filter data based on selections
filtered_df = df[
    (df['Country'] == selected_country) &
    (df['Transaction Type'] == selected_transaction_type) &
    (df['Amount (USD)'].between(amount_range[0], amount_range[1])) &
    (df['Date of Transaction'].between(date_range[0], date_range[1]))  # Corrected this part
]

# Title and Introduction
st.title("Big Black Money Insights")
st.write("An interactive dashboard to explore transactions, risk scores, and key insights.")

# Display selected graph
if graph_option == "Transaction Volume by Country":
    st.subheader("Transaction Volume by Country")
    transaction_volume = filtered_df.groupby('Country')['Amount (USD)'].sum().reset_index()
    st.bar_chart(transaction_volume.set_index('Country')['Amount (USD)'])

elif graph_option == "Risk Score Distribution":
    st.subheader("Risk Score Distribution")
    risk_score_counts = filtered_df['Money Laundering Risk Score'].value_counts().sort_index()
    st.bar_chart(risk_score_counts)

elif graph_option == "Transaction Amount by Type":
    st.subheader("Transaction Amount by Type")
    transaction_amount_type = filtered_df.groupby('Transaction Type')['Amount (USD)'].sum().reset_index()
    st.bar_chart(transaction_amount_type.set_index('Transaction Type')['Amount (USD)'])

elif graph_option == "Shell Companies by Industry":
    st.subheader("Shell Companies Involved by Industry")
    shell_companies = filtered_df.groupby('Industry')['Shell Companies Involved'].sum().reset_index()
    st.bar_chart(shell_companies.set_index('Industry')['Shell Companies Involved'])

elif graph_option == "Top Financial Institutions":
    st.subheader("Top Financial Institutions by Transaction Volume")
    top_institutions = filtered_df.groupby('Financial Institution')['Amount (USD)'].sum().reset_index()
    top_institutions = top_institutions.sort_values(by='Amount (USD)', ascending=False).head(10)
    st.bar_chart(top_institutions.set_index('Financial Institution')['Amount (USD)'])

elif graph_option == "Risk Score Over Time":
    st.subheader("Risk Score Over Time")
    risk_score_time = filtered_df.groupby(pd.Grouper(key='Date of Transaction', freq='M'))['Money Laundering Risk Score'].mean().reset_index()
    st.line_chart(risk_score_time.set_index('Date of Transaction')['Money Laundering Risk Score'])

elif graph_option == "High-Risk Transactions":
    st.subheader("High-Risk Transactions (Risk Score > 7)")
    high_risk_transactions = filtered_df[filtered_df['Money Laundering Risk Score'] > 7]
    st.write(high_risk_transactions[['Transaction ID', 'Country', 'Amount (USD)', 'Money Laundering Risk Score']])

elif graph_option == "Transactions by Tax Haven Countries":
    st.subheader("Transactions by Tax Haven Countries")
    tax_haven_transactions = filtered_df.groupby('Tax Haven Country')['Amount (USD)'].sum().reset_index()
    st.bar_chart(tax_haven_transactions.set_index('Tax Haven Country')['Amount (USD)'])

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_df)
