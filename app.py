import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.image("Black_Money.png",use_container_width=True)

# Caching the data using st.cache_data
@st.cache_data
def load_data(filepath):
    """Load data from a CSV file."""
    return pd.read_csv(filepath)

# Load the dataset
data = load_data(r"C:\Users\asus\OneDrive\Desktop\Masai School all Notes\Unit 2 PY\Unit2ProjectBlackmoney\Big_Black_Money_Dataset.csv"
)  # Replace with your dataset file path

# Sidebar for Filters
st.sidebar.header("Dashboard Controls")

# User Input Options
selected_column = st.sidebar.selectbox(
    "Select Column for Analysis", data.columns
)

# Ensure the selected column is numeric for the slider
if pd.api.types.is_numeric_dtype(data[selected_column]):
    numeric_filter = st.sidebar.slider(
        "Filter Numeric Range",
        min_value=float(data[selected_column].min()),
        max_value=float(data[selected_column].max()),
        value=(float(data[selected_column].min()), float(data[selected_column].max())),
    )
else:
    numeric_filter = None
    st.sidebar.write("The selected column is not numeric. Numeric filters are disabled.")

# Main Dashboard
st.title("Interactive Black Money Transactions Dashboard")

# Display Filtered Data
st.subheader("Filtered Dataset")

if numeric_filter:
    # Apply numeric filtering if the column is numeric
    filtered_data = data[
        (data[selected_column] >= numeric_filter[0]) & (data[selected_column] <= numeric_filter[1])
    ]
else:
    # Display all data if no numeric filter is applicable
    filtered_data = data

st.write(filtered_data)

# Generate Chart Based on User Input
st.subheader("Dynamic Visualization")
selected_chart = st.sidebar.radio(
    "Select Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"]
)

if selected_chart == "Bar Chart":
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_data, x=selected_column, ax=ax)
    st.pyplot(fig)

elif selected_chart == "Line Chart":
    if pd.api.types.is_numeric_dtype(data[selected_column]):
        fig, ax = plt.subplots()
        filtered_data.groupby(selected_column).size().plot(kind='line', ax=ax)
        st.pyplot(fig)
    else:
        st.error("Line chart requires a numeric column.")

elif selected_chart == "Scatter Plot":
    st.sidebar.write("Scatter plots require two numeric columns.")
    numeric_columns = data.select_dtypes(include='number').columns
    col_x = st.sidebar.selectbox("Select X-Axis", numeric_columns)
    col_y = st.sidebar.selectbox("Select Y-Axis", numeric_columns)
    fig, ax = plt.subplots()
    ax.scatter(filtered_data[col_x], filtered_data[col_y])
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    st.pyplot(fig)

elif selected_chart == "Pie Chart":
    fig, ax = plt.subplots()
    filtered_data[selected_column].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

# Additional Sidebar Features
st.sidebar.subheader("Additional Options")
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(filtered_data.describe())

if st.sidebar.checkbox("Show Original Dataset"):
    st.subheader("Original Dataset")
    st.write(data)

# Footer Section
st.sidebar.markdown("---")
st.sidebar.write("Developed by Your Name")
