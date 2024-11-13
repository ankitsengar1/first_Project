# Import required libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load your dataset
@st.cache_data
def load_data():
    # Replace 'your_data.csv' with the actual file path
    data = pd.read_csv(r"C:\Users\asus\OneDrive\Desktop\Masai School all Notes\Unit 2 PY\Unit2ProjectBlackmoney\Big_Black_Money_Dataset.csv")
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








st.subheader("Top 5 Countries by Transaction Amount")
# Get top 5 countries by transaction amount
top_countries = df.groupby('Country')['Amount (USD)'].sum().nlargest(5)
# Set up the color palette and style
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
colors = sns.color_palette("viridis", len(top_countries))  # Choose a vibrant color palette

# Create the bar plot
ax = sns.barplot(
    x=top_countries.index, 
    y=top_countries.values, 
    palette=colors
)
ax.set_title("Top 5 Countries by Transaction Amount", fontsize=16)
ax.set_xlabel("Country", fontsize=14)
ax.set_ylabel("Total Transaction Amount (USD)", fontsize=14)

# Add values on top of each bar for clarity
for index, value in enumerate(top_countries.values):
    ax.text(index, value + 0.05 * value, f"${value:,.2f}", ha="center", fontsize=12, color="black")

# Display the chart in Streamlit
st.pyplot(plt)







# Distribution of Transaction Types - Enhanced Visualization
st.subheader("Distribution of Transaction Types")

# Count the transaction types
transaction_type_counts = df['Transaction Type'].value_counts()

# Set up color palette and style
sns.set(style="whitegrid")  # Clean grid background
plt.figure(figsize=(10, 6))
colors = sns.color_palette("Set2")  # A colorful, pastel palette

# Create the bar plot
fig, ax = plt.subplots()
sns.barplot(
    x=transaction_type_counts.index, 
    y=transaction_type_counts.values, 
    palette=colors, 
    ax=ax
)

# Add titles and labels
ax.set_title("Distribution of Transaction Types", fontsize=18, color="darkblue", weight="bold")
ax.set_xlabel("Transaction Type", fontsize=14, color="gray")
ax.set_ylabel("Count", fontsize=14, color="gray")

# Customize ticks and grids
ax.tick_params(axis='x', rotation=45, colors="darkgray", labelsize=12)
ax.tick_params(axis='y', colors="darkgray", labelsize=12)
ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

# Display values on top of bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 10), 
                textcoords='offset points', 
                color="black", fontsize=12, weight="bold")

# Display the chart in Streamlit
st.pyplot(fig)







# Risk Score Analysis
risk_threshold = st.sidebar.slider("Select Risk Score Threshold", 0, 100, 80)
high_risk_transactions = df[df['Money Laundering Risk Score'] > risk_threshold]
st.subheader(f"High-Risk Transactions (Score > {risk_threshold})")
st.write(high_risk_transactions)

st.subheader("Average Shell Companies Involved by Industry")

# Calculate the average shell companies involved by industry
shell_by_industry = df.groupby('Industry')['Shell Companies Involved'].mean().sort_values()

# Set up color palette and style
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
colors = sns.color_palette("Spectral", len(shell_by_industry))  # Colorful, contrasting palette

# Create the bar plot
fig, ax = plt.subplots()
sns.barplot(
    x=shell_by_industry.values, 
    y=shell_by_industry.index, 
    palette=colors, 
    ax=ax
)

# Add titles and labels
ax.set_title("Average Shell Companies Involved by Industry", fontsize=18, color="darkblue", weight="bold")
ax.set_xlabel("Average Shell Companies Involved", fontsize=14, color="gray")
ax.set_ylabel("Industry", fontsize=14, color="gray")

# Customize ticks and grid
ax.tick_params(axis='x', colors="darkgray", labelsize=12)
ax.tick_params(axis='y', colors="darkgray", labelsize=12)
ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

# Display values next to each bar for clarity
for p in ax.patches:
    ax.annotate(f'{p.get_width():.2f}', 
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha='left', va='center', 
                xytext=(5, 0), 
                textcoords='offset points', 
                color="black", fontsize=12, weight="bold")

# Display the chart in Streamlit
st.pyplot(fig)








# Monthly Transaction Trend - Enhanced Visualization
st.subheader("Monthly Transaction Trend")

# Convert the date to datetime and extract monthly data
df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'])
monthly_trend = df.groupby(df['Date of Transaction'].dt.to_period('M'))['Amount (USD)'].sum()
monthly_trend.index = monthly_trend.index.to_timestamp()  # Convert PeriodIndex to Timestamp for plotting

# Set up color palette and style
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
fig, ax = plt.subplots()

# Create the line plot
sns.lineplot(
    x=monthly_trend.index, 
    y=monthly_trend.values, 
    color="dodgerblue", 
    marker="o", 
    markersize=8, 
    linewidth=2, 
    ax=ax
)

# Add titles and labels
ax.set_title("Monthly Transaction Trend", fontsize=18, color="darkblue", weight="bold")
ax.set_xlabel("Month", fontsize=14, color="gray")
ax.set_ylabel("Total Transaction Amount (USD)", fontsize=14, color="gray")

# Customize ticks and grid
ax.tick_params(axis='x', rotation=45, colors="darkgray", labelsize=10)
ax.tick_params(axis='y', colors="darkgray", labelsize=12)
ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

# Display values on data points
for x, y in zip(monthly_trend.index, monthly_trend.values):
    ax.text(x, y, f'{y:,.0f}', ha='center', va='bottom', fontsize=10, color="black")

# Display the chart in Streamlit
st.pyplot(fig)





# Transactions Involving Tax Haven Countries - Enhanced Design
st.subheader("Transactions Involving Tax Haven Countries")

# Filter transactions involving tax haven countries
tax_haven_transactions = df[df['Tax Haven Country'] != 'None']

# Calculate the average transaction amount in tax haven countries
avg_tax_haven_amount = tax_haven_transactions['Amount (USD)'].mean()

# Display average transaction amount with custom styling
st.markdown(
    f"<h3 style='text-align: center; color: #2ca02c; font-weight: bold;'>"
    f"Average Transaction Amount in Tax Haven Countries: ${avg_tax_haven_amount:,.2f}"
    "</h3>", 
    unsafe_allow_html=True
)

# Create a progress bar for average transaction amount
progress_bar = st.progress(0)  # Initialize progress bar
max_amount = df['Amount (USD)'].max()  # Max possible value for progress bar
progress_bar.progress(min(avg_tax_haven_amount / max_amount, 1.0))  # Update progress based on avg value

# Optional: Create a pie chart showing the proportion of transactions involving tax haven countries
total_transactions = len(df)
tax_haven_count = len(tax_haven_transactions)

# Create a pie chart to visualize the proportion of transactions involving tax haven countries
fig = go.Figure(go.Pie(
    labels=["Involving Tax Haven", "Not Involving Tax Haven"],
    values=[tax_haven_count, total_transactions - tax_haven_count],
    hole=0.4,  # Creates a donut chart
    hoverinfo="label+percent",
    textinfo="percent+label",
    marker=dict(colors=["#2ca02c", "#ff7f0e"])
))

fig.update_layout(
    title="Proportion of Transactions Involving Tax Haven Countries",
    title_x=0.5,
    title_y=0.95,
    showlegend=False
)

# Display the donut chart
st.plotly_chart(fig)




# Percentage of Transactions Reported by Authority - Enhanced Design
st.subheader("Percentage of Transactions Reported by Authority")

# Calculate the percentage of transactions reported by authority
reported_percentage = df['Reported by Authority'].mean() * 100

# Create a Progress Bar for better visualization
progress_bar = st.progress(0)  # Initialize progress bar
progress_bar.progress(reported_percentage / 100)  # Set progress based on percentage

# Display percentage with a custom styled message
st.markdown(
    f"<h3 style='text-align: center; color: #1f77b4; font-weight: bold;'>"
    f"{reported_percentage:.2f}% of transactions are reported by authority."
    "</h3>", 
    unsafe_allow_html=True
)

# Optionally, add a donut chart for a more graphical representation using Plotly
fig = go.Figure(go.Pie(
    labels=["Reported", "Not Reported"],
    values=[reported_percentage, 100 - reported_percentage],
    hole=0.4,  # Creates a donut chart
    hoverinfo="label+percent",
    textinfo="percent+label",
    marker=dict(colors=["#1f77b4", "#d62728"])
))

fig.update_layout(
    title="Transaction Reporting by Authority",
    title_x=0.5,
    title_y=0.95,
    showlegend=False
)

# Display the donut chart
st.plotly_chart(fig)





# Top Financial Institutions by Transaction Volume - Enhanced Visualization
st.subheader("Top Financial Institutions by Transaction Volume")

# Calculate the top financial institutions by transaction volume
top_institutions = df.groupby('Financial Institution')['Amount (USD)'].sum().nlargest(5)

# Set up color palette and style
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
colors = sns.color_palette("coolwarm", len(top_institutions))  # Cool-to-warm color gradient

# Create the bar plot
fig, ax = plt.subplots()
sns.barplot(
    x=top_institutions.values, 
    y=top_institutions.index, 
    palette=colors, 
    ax=ax
)

# Add titles and labels
ax.set_title("Top Financial Institutions by Transaction Volume", fontsize=18, color="darkblue", weight="bold")
ax.set_xlabel("Total Transaction Volume (USD)", fontsize=14, color="gray")
ax.set_ylabel("Financial Institution", fontsize=14, color="gray")

# Customize ticks and grid
ax.tick_params(axis='x', colors="darkgray", labelsize=12)
ax.tick_params(axis='y', colors="darkgray", labelsize=12)
ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

# Display values next to each bar for clarity
for p in ax.patches:
    ax.annotate(f'${p.get_width():,.0f}', 
                (p.get_width(), p.get_y() + p.get_height() / 2), 
                ha='left', va='center', 
                xytext=(5, 0), 
                textcoords='offset points', 
                color="black", fontsize=12, weight="bold")

# Display the chart in Streamlit
st.pyplot(fig)

