import streamlit as st
import pandas as pd
import io
import duckdb

# Set page title and configuration
st.set_page_config(page_title="Financier Data Explorer", layout="wide")

# Title and logo
st.title("📊 Financier Data Explorer")
#Connect to DuckDB database
@st.cache_resource
def get_duckdb_connection():
    return duckdb.connect("financier_data.duck.db")

# Load the data from DuckDB
@st.cache_data
def load_data():
    conn = get_duckdb_connection()
    df = conn.execute("SELECT * FROM financier_data").fetchdf()
    # Convert period to string to ensure proper matching
    df['period'] = df['period'].astype(str)
    return df

try:
    data = load_data()
    
    # Get unique accounting categories for the dropdown
    accounting_categories = sorted(data['catAccountingView'].unique())
    
    # Rest of your Streamlit app code here
    # Add filters, visualizations, etc.
    
    # Example: Display some basic info
    st.write(f"Data loaded successfully: {len(data)} records")
    st.write("Sample data:")
    st.dataframe(data.head())
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.error("Please make sure to run setup_duckdb.py first to create the database.")
    
    
# Get unique accounting categories for the dropdown
accounting_categories = sorted(data['catAccountingView'].unique())

# Create sidebar filters
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox("Accounting Category", 
                                       options=accounting_categories,
                                       index=0)

# Get available periods for the selected category
available_periods = sorted(data[data['catAccountingView'] == selected_category]['period'].unique())

# Period selection
selected_period = st.sidebar.selectbox("Period", 
                                     options=available_periods,
                                     index=0 if available_periods else None)

# Main content area
st.header(f"Data for {selected_category} - Period {selected_period}")

if selected_period:
    # Filter data based on selections
    filtered_data = data[(data['catAccountingView'] == selected_category) & 
                         (data['period'] == selected_period)]
    
    if not filtered_data.empty:
        # Display the data
        st.subheader("Financial Data")
        st.dataframe(filtered_data)
        
        # Financial metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue", f"€{filtered_data['revenue'].values[0]:,.2f}")
        with col2:
            st.metric("Net Profit", f"€{filtered_data['netProfit'].values[0]:,.2f}")
        with col3:
            st.metric("Profit Margin", f"{(filtered_data['netProfit'].values[0]/filtered_data['revenue'].values[0])*100:.1f}%")
        
        # Visualization section
        st.subheader("Key Financial Metrics")
        
        # Convert the row to a format suitable for charting
        chart_data = pd.DataFrame({
            'Metric': ['Revenue', 'Gross Margin', 'Operating Profit', 'Net Profit'],
            'Value': [
                filtered_data['revenue'].values[0],
                filtered_data['grossMargin'].values[0],
                filtered_data['operatingProfit'].values[0],
                filtered_data['netProfit'].values[0]
            ]
        })
        
        # Create a bar chart
        st.bar_chart(chart_data.set_index('Metric'))
        
        # Additional financial KPIs
        st.subheader("Financial KPIs")
        kpi_cols = st.columns(2)
        with kpi_cols[0]:
            st.info(f"Gross Margin Ratio: {(filtered_data['grossMargin'].values[0]/filtered_data['revenue'].values[0])*100:.1f}%")
            st.info(f"Operating Margin: {(filtered_data['operatingProfit'].values[0]/filtered_data['revenue'].values[0])*100:.1f}%")
        with kpi_cols[1]:
            st.info(f"Operating Expenses: €{filtered_data['operatingExpenses'].values[0]:,.2f}")
            st.info(f"Financial Result: €{filtered_data['FinancialResult'].values[0]:,.2f}")
    else:
        st.warning(f"No data found for category '{selected_category}' and period '{selected_period}'")
else:
    st.info("Please select a category and period to view data")

# About section
with st.expander("About this app"):
    st.markdown("""
    This application allows you to explore financial data across different accounting categories and time periods.
    
    - Use the sidebar to filter data by accounting category and period
    - View key financial metrics and visualizations
    - Analyze financial KPIs and performance indicators
    """)