import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff


@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/amazon_sales_2025_INR.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Quarter"] = df["Date"].dt.quarter
    df["Delivered_Flag"] = (df["Delivery_Status"] == "Delivered").astype(int)
    df["Satisfied"] = (df["Review_Rating"] >= 4).astype(int)
    df["Log_Total_Sales"] = np.log(df["Total_Sales_INR"] + 1)
    return df

df = load_data()

st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Filter by Product Category",
    sorted(df["Product_Category"].unique()),
    default=df["Product_Category"].unique(),)

states = st.sidebar.multiselect(
    "Filter by State",
    sorted(df["State"].unique()),
    default=df["State"].unique(),)

payment_methods = st.sidebar.multiselect(
    "Filter by Payment Method",
    sorted(df["Payment_Method"].unique()),
    default=df["Payment_Method"].unique(),)

filtered = df[
    (df["Product_Category"].isin(categories))
    & (df["State"].isin(states))
    & (df["Payment_Method"].isin(payment_methods))]

st.title("Amazon Diwali Sales 2025 Dashboard")
st.write("A complete analytics dashboard including sales trends, ratings, payments, correlations, forecasting, and anomaly detection.")

def format_large(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f} B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.2f} M"
    elif n >= 1_000:
        return f"{n/1_000:.2f} K"
    else:
        return f"{n:,}"

col1, col2, col3 = st.columns(3)

total_rev = filtered['Total_Sales_INR'].sum()
col1.metric("Total Revenue (INR)", format_large(total_rev))
col2.metric("Avg Rating", f"{filtered['Review_Rating'].mean():.2f}")
col3.metric("Delivery Success Rate", f"{filtered['Delivered_Flag'].mean()*100:.1f}%")

st.markdown("---")

# RQ1: Sales by Product Category
st.header("RQ1: Sales by Product Category")

category_sales = (
    filtered.groupby("Product_Category")["Total_Sales_INR"]
    .sum()
    .reset_index())

fig1 = px.bar(
    category_sales,
    x="Product_Category",
    y="Total_Sales_INR",
    color="Product_Category",
    text_auto=True,
    title="Total Sales by Category",
    color_discrete_sequence=px.colors.qualitative.Set2,)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")


# RQ2: Ratings & Delivery Behavior
st.header("RQ2: Ratings vs Delivery Status")

fig2 = px.box(
    filtered,
    x="Delivery_Status",
    y="Review_Rating",
    color="Delivery_Status",
    title="Ratings by Delivery Status",
    color_discrete_sequence=px.colors.qualitative.Pastel,)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# RQ3: Revenue by Payment Method
st.header("RQ3: Payment Method Impact")

payment_sales = (
    filtered.groupby("Payment_Method")["Total_Sales_INR"]
    .sum()
    .reset_index())

fig3 = px.bar(
    payment_sales,
    x="Payment_Method",
    y="Total_Sales_INR",
    text_auto=True,
    color="Payment_Method",
    title="Revenue by Payment Method",
    color_discrete_sequence=px.colors.qualitative.Bold,)
st.plotly_chart(fig3, use_container_width=True)

# Ratings by payment method
pm_rating = (
    filtered.groupby("Payment_Method")["Review_Rating"]
    .mean()
    .reset_index())

fig3b = px.bar(
    pm_rating,
    x="Payment_Method",
    y="Review_Rating",
    text_auto=".2f",
    title="Average Rating by Payment Method",
    color="Payment_Method",
    color_discrete_sequence=px.colors.qualitative.Vivid,)
st.plotly_chart(fig3b, use_container_width=True)

st.markdown("---")


# RQ4: Monthly Revenue Trend
st.header("RQ4: Monthly Revenue Trend (2025)")

monthly = (
    filtered.groupby("Month_Name")["Total_Sales_INR"]
    .sum()
    .reset_index())

month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly["Month_Name"] = pd.Categorical(monthly["Month_Name"], month_order, ordered=True)
monthly = monthly.sort_values("Month_Name")

fig4 = px.line(
    monthly,
    x="Month_Name",
    y="Total_Sales_INR",
    markers=True,
    title="Monthly Revenue Trend",
    color_discrete_sequence=["#FF5733"],)
fig4.update_traces(marker=dict(size=9), text=monthly["Total_Sales_INR"], textposition="top center")
st.plotly_chart(fig4, use_container_width=True)

# Quarterly
quarter_sales = (
    filtered.groupby("Quarter")["Total_Sales_INR"]
    .sum()
    .reset_index())

fig4b = px.bar(
    quarter_sales,
    x="Quarter",
    y="Total_Sales_INR",
    text_auto=True,
    color="Quarter",
    title="Quarterly Revenue Comparison",
    color_discrete_sequence=px.colors.qualitative.Set3,)
st.plotly_chart(fig4b, use_container_width=True)

st.markdown("---")

# Correlation Heatmap
st.header("Correlation Heatmap")

numeric_cols = ["Total_Sales_INR", "Review_Rating", "Delivered_Flag", "Satisfied", "Log_Total_Sales"]

corr = filtered[numeric_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Heatmap",)
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

# Scatter Matrix
st.header("Scatter Matrix with Trend Lines")

pairs = [
    ("Log_Total_Sales", "Review_Rating"),
    ("Log_Total_Sales", "Satisfied"),
    ("Review_Rating", "Satisfied"),
    ("Delivered_Flag", "Satisfied")]

for x, y in pairs:
    fig = px.scatter(
        filtered,
        x=x,
        y=y,
        color="Product_Category",
        trendline="ols",
        opacity=0.6,
        title=f"{x} vs {y}",)
    fig.update_layout(title_x=0.5, height=450)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# State x Category Sales Matrix
st.header("State x Category Sales Heatmap")

pivot = filtered.pivot_table(
    values="Total_Sales_INR",
    index="State",
    columns="Product_Category",
    aggfunc="sum",
    fill_value=0)

fig_matrix2 = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Sales Matrix: State vs Product Category",
    text_auto=True,)
st.plotly_chart(fig_matrix2, use_container_width=True)

st.markdown("---")

# Simple Forecasting (Moving Average)
st.header("Forecasting Next 3 Months (Moving Average)")

monthly_sorted = monthly.set_index("Month_Name")

forecast_values = monthly_sorted["Total_Sales_INR"].rolling(3).mean().dropna()
last_value = forecast_values.iloc[-1]

forecast_next = {
    "Next_Month": last_value * 1.02,
    "Month+2": last_value * 1.04,
    "Month+3": last_value * 1.06,}

forecast_df = pd.DataFrame.from_dict(forecast_next, orient="index", columns=["Forecasted_Sales"])

fig_fc = px.line(
    forecast_df,
    y="Forecasted_Sales",
    markers=True,
    title="3-Month Ahead Sales Forecast (Simple MA Model)",)
st.plotly_chart(fig_fc, use_container_width=True)

st.markdown("---")

# Anomaly Detection (Z-score)
st.header("Sales Anomaly Detection")

sales_series = filtered["Total_Sales_INR"]
z_scores = (sales_series - sales_series.mean()) / sales_series.std()

anomalies = filtered[z_scores.abs() > 2]

st.subheader("Detected Outliers (Z-score > 2)")
st.write(anomalies if len(anomalies) > 0 else "No anomalies detected")
