# Transaction Analysis Dashboard

This repository contains a Streamlit application designed for interactive analysis of transaction data. The dashboard provides key insights through statistical summaries and visualizations, making it easier to interpret large datasets and explore transaction trends across different countries.

## Overview

The **Transaction Analysis Dashboard** is a powerful tool that offers:
- A user-friendly interface to visualize and explore transaction data.
- Detailed summary statistics for an immediate understanding of data characteristics.
- Top contributors displayed by transaction amounts, helping to identify important regions.

Built in Python, this application leverages:
- **Streamlit** for creating a web-based interactive dashboard.
- **Pandas** for data handling and manipulation.
- **Seaborn** and **Matplotlib** for data visualization.
- **Plotly** for creating interactive charts.

## Features

- **Display Raw Data**: Provides a toggle in the sidebar to view the complete dataset, allowing users to verify and explore raw data entries.
- **Summary Statistics**: Calculates and displays descriptive statistics like mean, median, standard deviation, etc., offering an immediate snapshot of the dataset’s structure.
- **Top 5 Countries by Transaction Amount**: Visualizes the countries with the highest transaction amounts, displayed in an easy-to-read bar chart to highlight key contributors.

## Getting Started

### Prerequisites

To run this application, you’ll need Python installed on your system, along with the following libraries:
- `streamlit`: For building the interactive app interface.
- `pandas`: For efficient data loading and manipulation.
- `seaborn` and `matplotlib`: For creating static visualizations.
- `plotly`: For adding interactive charting capabilities.

You can install all required libraries with the following command:
```bash
pip install streamlit pandas seaborn matplotlib plotly
