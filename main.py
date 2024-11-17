import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('Big_Black_Money_Dataset.csv')

# Title and Introduction
st.title("Big Black Money Insights")
st.write("An interactive dashboard to explore transactions, risk scores, and key insights.")

# Sidebar for Filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Originating Country", ['All'] + df['Country'].dropna().unique().tolist())
selected_transaction_type = st.sidebar.selectbox("Select Transaction Type", ['All'] + df['Transaction Type'].dropna().unique().tolist())
amount_range = st.sidebar.slider("Select Transaction Amount Range (USD)", 
                                  int(df['Amount (USD)'].min()), 
                                  int(df['Amount (USD)'].max()), 
                                  (int(df['Amount (USD)'].min()), int(df['Amount (USD)'].max())))

# Sidebar for Graph Type
st.sidebar.header("Graph Options")
graph_type = st.sidebar.selectbox("Select Graph Type", ["Bar Chart", "Pie Chart", "Scatter Plot", "Line Chart"])

# Filter data based on selections
filtered_df = df.copy()
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
if selected_transaction_type != 'All':
    filtered_df = filtered_df[filtered_df['Transaction Type'] == selected_transaction_type]
filtered_df = filtered_df[filtered_df['Amount (USD)'].between(amount_range[0], amount_range[1])]

# Graphs
st.subheader(f"Displaying: {graph_type}")
if graph_type == "Bar Chart":
    # Bar chart: Transaction Volume by Country
    transaction_volume = filtered_df.groupby('Country')['Amount (USD)'].sum().reset_index()
    st.bar_chart(transaction_volume.set_index('Country')['Amount (USD)'])

elif graph_type == "Pie Chart":
    # Pie chart: Distribution of Transaction Type
    transaction_type_data = filtered_df['Transaction Type'].value_counts()
    st.write("Transaction Type Distribution (Pie Chart)")
    st.write(transaction_type_data)  # Display data for clarity
    st.area_chart(transaction_type_data)  # Pie chart approximation using area_chart

elif graph_type == "Scatter Plot":
    # Scatter plot: Financial Institutions vs. Transaction Amount
    scatter_data = filtered_df.groupby('Financial Institution')['Amount (USD)'].sum().reset_index()
    st.write("Scatter Plot: Financial Institutions vs. Transaction Volume")
    st.write(scatter_data.set_index('Financial Institution'))  # Display raw data
    st.bar_chart(scatter_data.set_index('Financial Institution')['Amount (USD)'])  # Approximate scatter using bar_chart

elif graph_type == "Line Chart":
    # Line chart: Risk Score Over Time
    filtered_df['Date of Transaction'] = pd.to_datetime(filtered_df['Date of Transaction'], errors='coerce')
    risk_score_time = filtered_df.groupby(pd.Grouper(key='Date of Transaction', freq='M'))['Money Laundering Risk Score'].mean().reset_index()
    st.line_chart(risk_score_time.set_index('Date of Transaction')['Money Laundering Risk Score'])

# Display filtered data
st.subheader("Filtered Data Overview")
st.write(f"Showing {len(filtered_df)} rows based on your filters:")
st.dataframe(filtered_df)
