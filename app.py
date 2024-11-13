# Import required libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
@st.cache_data
def load_data():
    # Replace 'your_data.csv' with the actual file path
    data = pd.read_csv("C:/Users/priya/Downloads/archive (4)/Big_Black_Money_Dataset.csv")
    return data

df = load_data()

# Streamlit app layout
st.title("Transaction Analysis Dashboard")
st.sidebar.title("Filters")

# Display the dataset
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(df)

# Summary statistics
st.subheader("Summary Statistics")
st.write(df.describe())

# Top 5 Countries by Transaction Amount
st.subheader("Top 5 Countries by Transaction Amount")
top_countries = df.groupby('Country')['Amount (USD)'].sum().nlargest(5)
st.bar_chart(top_countries)

# Distribution of Transaction Types
st.subheader("Distribution of Transaction Types")
transaction_type_counts = df['Transaction Type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=transaction_type_counts.index, y=transaction_type_counts.values, ax=ax)
ax.set_title("Distribution of Transaction Types")
ax.set_ylabel("Count")
st.pyplot(fig)

# Risk Score Analysis
risk_threshold = st.sidebar.slider("Select Risk Score Threshold", 0, 100, 80)
high_risk_transactions = df[df['Money Laundering Risk Score'] > risk_threshold]
st.subheader(f"High-Risk Transactions (Score > {risk_threshold})")
st.write(high_risk_transactions)

# Shell Companies Involvement by Industry
st.subheader("Average Shell Companies Involved by Industry")
shell_by_industry = df.groupby('Industry')['Shell Companies Involved'].mean()
st.bar_chart(shell_by_industry)

# Monthly Transaction Trend
st.subheader("Monthly Transaction Trend")
df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'])
monthly_trend = df.groupby(df['Date of Transaction'].dt.to_period('M'))['Amount (USD)'].sum()
st.line_chart(monthly_trend)

# Transactions Involving Tax Haven Countries
st.subheader("Transactions Involving Tax Haven Countries")
tax_haven_transactions = df[df['Tax Haven Country'] != 'None']
avg_tax_haven_amount = tax_haven_transactions['Amount (USD)'].mean()
st.write(f"Average Transaction Amount in Tax Haven Countries: ${avg_tax_haven_amount:.2f}")

# Percentage of Transactions Reported by Authority
st.subheader("Percentage of Transactions Reported by Authority")
reported_percentage = df['Reported by Authority'].mean() * 100
st.write(f"{reported_percentage:.2f}% of transactions are reported by authority.")

# Top Financial Institutions by Transaction Volume
st.subheader("Top Financial Institutions by Transaction Volume")
top_institutions = df.groupby('Financial Institution')['Amount (USD)'].sum().nlargest(5)
st.bar_chart(top_institutions)

