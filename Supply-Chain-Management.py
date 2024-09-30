
import streamlit as st
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load your data
# Adjust the file path as necessary
df = pickle.load(open("C:\\Users\\SUBHANKAR\\jupyter Notebook (Anaconda3) for Python\\df.pkl", 'rb'))

# Define mock data for visualization (replace with actual data from df)
product_sales = df.groupby('Product type')['Number of products sold'].sum()
revenue_analysis = df.groupby('Product type')['Revenue generated'].sum()
price_distribution = df['Price']
stock_levels = df.pivot_table(index='SKU', columns='Product type', values='Stock levels', fill_value=0)
lead_times_order_quantities = df[['Lead times', 'Order quantities']]
shipping_costs_carrier = df.groupby('Shipping carriers')['Shipping costs'].sum()
manufacturing_efficiency = df[['Manufacturing lead time', 'Production volumes']]
defect_rates = df.groupby('Supplier name')['Defect rates'].mean()
demographic_breakdown = df['Customer demographics'].value_counts()
revenue_demographics = df.groupby('Customer demographics')['Revenue generated'].sum()

# KPIs
total_revenue = revenue_analysis.sum()
total_order_quantity = df['Order quantities'].sum()
total_availability = df['Availability'].sum()

# Streamlit App
st.title("Supply Chain Management Dashboard")

# Add 3 KPIs at the top of the dashboard
st.header("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue Generated", f"${total_revenue:,.2f}")
col2.metric("Total Order Quantity", f"{total_order_quantity:,}")
col3.metric("Total Availability", f"{total_availability:,}")

st.header("Product Performance")

st.subheader("Product Sales")
st.bar_chart(product_sales)

st.subheader("Revenue Analysis")
st.line_chart(revenue_analysis)

st.subheader("Price Distribution")
fig, ax = plt.subplots()
ax.hist(price_distribution, bins=20)
ax.set_title('Price Distribution')
ax.set_xlabel('Price')
ax.set_ylabel('Frequency')
st.pyplot(fig)

st.subheader("Stock Levels")
fig, ax = plt.subplots()
im = ax.imshow(stock_levels, cmap='hot', interpolation='nearest')
ax.set_title('Stock Levels')
ax.set_xlabel('Product')
ax.set_ylabel('SKU')
fig.colorbar(im, ax=ax)
st.pyplot(fig)

# Supply Chain Efficiency
st.header("Supply Chain Efficiency")

st.subheader("Lead Times vs. Order Quantities")
fig, ax = plt.subplots()
ax.scatter(lead_times_order_quantities['Lead times'], lead_times_order_quantities['Order quantities'])
ax.set_title('Lead Times vs. Order Quantities')
ax.set_xlabel('Lead Times')
ax.set_ylabel('Order Quantities')
st.pyplot(fig)

st.subheader("Shipping Costs by Carrier")
st.bar_chart(shipping_costs_carrier)

st.subheader("Manufacturing Efficiency")
fig, ax = plt.subplots()
ax.scatter(manufacturing_efficiency['Manufacturing lead time'], manufacturing_efficiency['Production volumes'])
ax.set_title('Manufacturing Efficiency')
ax.set_xlabel('Manufacturing Lead Time')
ax.set_ylabel('Production Volumes')
st.pyplot(fig)

st.subheader("Defect Rates")
st.bar_chart(defect_rates)

# Customer Demographics
st.header("Customer Demographics")

st.subheader("Demographic Breakdown")
fig, ax = plt.subplots()
ax.pie(demographic_breakdown.values, labels=demographic_breakdown.index, autopct='%1.1f%%')
ax.set_title('Demographic Breakdown')
st.pyplot(fig)

st.subheader("Revenue by Demographics")
st.bar_chart(revenue_demographics)

# Analysis Questions
st.header("Analysis Questions")

st.subheader("Which Product Type generates the highest revenue?")
highest_revenue_product = revenue_analysis.idxmax()
st.write(highest_revenue_product)

st.subheader("Are there any significant correlations between Lead times and Order quantities?")
lead_times_order_quantities_corr = lead_times_order_quantities.corr()
st.write(lead_times_order_quantities_corr)

st.subheader("How do Shipping costs vary by Shipping carrier and Location?")
shipping_costs_carrier_location = df.groupby(['Shipping carriers', 'Location'])['Shipping costs'].sum()
st.write(shipping_costs_carrier_location)

st.subheader("Which supplier has the most efficient manufacturing process based on Manufacturing lead time and Production volumes?")
manufacturing_efficiency_supplier = manufacturing_efficiency.groupby(df['Supplier name']).mean()
st.write(manufacturing_efficiency_supplier)

st.subheader("What demographic group contributes the most to sales?")
demographic_sales = df.groupby('Customer demographics')['Revenue generated'].sum()
st.write(demographic_sales.idxmax())
