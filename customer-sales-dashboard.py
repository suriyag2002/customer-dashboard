import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Load and Cache Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# ----------------------------
# Streamlit Layout
# ----------------------------
st.title("📊 Customer Sales Dashboard")

# Date Range Filter
start_date = st.date_input("Start Date", df['Date'].min())
end_date = st.date_input("End Date", df['Date'].max())

# Apply Filter
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                 (df['Date'] <= pd.to_datetime(end_date))]

# ----------------------------
# KPIs
# ----------------------------
st.write("### 🚀 Key Metrics")
total_revenue = filtered_df['Total'].sum()
total_orders = len(filtered_df)
total_customers = filtered_df['Customer'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${total_revenue}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("👥 Unique Customers", total_customers)

# ----------------------------
# Sales Trend Over Time
# ----------------------------
st.write("### 📈 Sales Trend Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Total'], marker='o', linestyle='-', color='royalblue')
ax.set_xlabel("Date")
ax.set_ylabel("Total Sales")
ax.grid(True)
st.pyplot(fig)

# ----------------------------
# Region-wise Pie Chart
# ----------------------------
st.write("### 🌍 Sales by Region")
region_sales = filtered_df.groupby('Region')['Total'].sum()

fig, ax = plt.subplots()
ax.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.pyplot(fig)

# ----------------------------
# Downloadable CSV
# ----------------------------
st.write("### 📥 Download Sales Report")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "sales_report.csv", "text/csv")
