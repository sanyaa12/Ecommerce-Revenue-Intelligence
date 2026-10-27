
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Ecommerce Revenue Intelligence",
    page_icon="📊",
    layout="wide"
)

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"

st.title("📊 Ecommerce Revenue Intelligence")
st.markdown("### Sales Performance & Business Insights")
st.divider()

# Load exported SQL results
@st.cache_data
def load_data(filename):
    file_path = DATA_DIR / filename
    if file_path.exists():
        return pd.read_csv(file_path)
    return pd.DataFrame()

country_df = load_data("country_revenue.csv")
monthly_df = load_data("monthly_revenue.csv")
products_df = load_data("top_10_products.csv")
weekday_df = load_data("sales_by_day_of_week.csv")
cleaned_df = load_data("cleaned_retail.csv")

valid_sales = cleaned_df[
    cleaned_df["CustomerID"].notna()
    & (cleaned_df["Revenue"] > 0)
]

if country_df.empty:
    st.error(
        f"Country revenue file not found in: {DATA_DIR}\n\n"
        "Please check the CSV filenames and location."
    )
    st.stop()

# Sidebar
st.sidebar.header("Dashboard Filters")

if "Country" in country_df.columns:
    countries = sorted(country_df["Country"].dropna().unique())
    selected_countries = st.sidebar.multiselect(
        "Select countries",
        countries,
        default=countries
    )
    filtered_country = country_df[
        country_df["Country"].isin(selected_countries)
    ]
else:
    filtered_country = country_df
    
filtered_sales = cleaned_df[
    cleaned_df["CustomerID"].notna()
    & (cleaned_df["Revenue"] > 0)
    & cleaned_df["Country"].isin(selected_countries)
]



# KPI cards

valid_sales = filtered_sales

total_revenue = valid_sales["Revenue"].sum()
total_orders = valid_sales["InvoiceNo"].nunique()
total_customers = valid_sales["CustomerID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"{total_revenue:,.2f}")
col2.metric("🛒 Orders", f"{total_orders:,.0f}")
col3.metric("👥 Customers", f"{total_customers:,.0f}")

st.divider()

# Revenue by country
st.subheader("🌐 Revenue by Country (Top 10)")
if not filtered_country.empty:
    fig_country = px.bar(
        filtered_country.sort_values("total_revenue", ascending=False),
        x="Country",
        y="total_revenue",
        color="total_revenue",
        title="Total Revenue by Country",
        labels={"total_revenue": "Revenue"}
    )
    st.plotly_chart(fig_country, use_container_width=True)

# Monthly revenue trend
st.subheader("📈 Monthly Revenue Trend")
if not filtered_sales.empty:
    monthly_filtered = filtered_sales.copy()
    monthly_filtered["InvoiceDate"] = pd.to_datetime(
        monthly_filtered["InvoiceDate"], errors="coerce"
    )
    monthly_filtered = monthly_filtered.dropna(subset=["InvoiceDate"])
    monthly_filtered["sales_month"] = (
        monthly_filtered["InvoiceDate"].dt.to_period("M").astype(str)
    )

    monthly_filtered = (
        monthly_filtered.groupby("sales_month", as_index=False)["Revenue"]
        .sum()
        .rename(columns={"Revenue": "monthly_revenue"})
    )

    fig_month = px.line(
        monthly_filtered,
        x="sales_month",
        y="monthly_revenue",
        markers=True,
        title="Revenue Over Time",
        labels={
            "sales_month": "Month",
            "monthly_revenue": "Revenue"
        }
    )
    st.plotly_chart(fig_month, use_container_width=True)
else:
    st.info("No sales available for the selected countries.")


# Top products
st.subheader("🏆 Top 10 Products")

if not filtered_sales.empty:
    products_filtered = (
        filtered_sales.groupby("Description", as_index=False)["Revenue"]
        .sum()
        .rename(columns={"Revenue": "product_revenue"})
        .sort_values("product_revenue", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        products_filtered,
        x="product_revenue",
        y="Description",
        orientation="h",
        title="Top Products by Revenue",
        labels={
            "product_revenue": "Revenue",
            "Description": "Product"
        }
    )
    fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_products, use_container_width=True)
else:
    st.info("No product sales available for the selected countries.")

# Sales by weekday
st.subheader("🗓️ Sales by Day of Week")

if not cleaned_df.empty and selected_countries:
    weekday_filtered = valid_sales[
        valid_sales["Country"].isin(selected_countries)
    ].copy()

    if not weekday_filtered.empty:
        weekday_filtered["day_of_week"] = pd.to_datetime(
            weekday_filtered["InvoiceDate"]
        ).dt.day_name()

        weekday_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]

        weekday_summary = (
            weekday_filtered.groupby("day_of_week", as_index=False)["Revenue"]
            .sum()
        )

        weekday_summary["day_of_week"] = pd.Categorical(
            weekday_summary["day_of_week"],
            categories=weekday_order,
            ordered=True
        )
        weekday_summary = weekday_summary.sort_values("day_of_week")

        fig_weekday = px.bar(
            weekday_summary,
            x="day_of_week",
            y="Revenue",
            title="Revenue by Weekday",
            labels={"day_of_week": "Day", "Revenue": "Revenue"}
        )
        st.plotly_chart(fig_weekday, width="stretch")
    else:
        st.info("No weekday sales available for the selected countries.")
else:
    st.info("Select at least one country to view weekday sales.")


# Detailed country table
st.subheader("📋 Country Revenue Details")
st.dataframe(filtered_country, use_container_width=True)

st.caption("Ecommerce Revenue Intelligence | Built with Python, SQL and Streamlit")