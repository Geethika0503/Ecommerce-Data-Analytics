
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

# Dataset directory
P = Path(__file__).resolve().parents[1] / "data/processed"

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 E-Commerce Sales & Customer Behaviour")
st.markdown("Interactive Retail Business Intelligence Dashboard")

# Check dataset availability
if not (P / "sales.csv").exists():
    st.error("Run python pipeline.py first.")
    st.stop()

# Load datasets
@st.cache_data
def load(name):
    return pd.read_csv(
        P / f"{name}.csv",
        dtype={
            "CustomerID": "string",
            "InvoiceNo": "string",
            "StockCode": "string"
        }
    )

s = load("sales")
r = load("returns")
rfm = load("rfm")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

markets = sorted(set(s.Country) | set(r.Country))

selected = st.sidebar.multiselect(
    "Select Countries",
    markets,
    default=markets
)

months = sorted(set(s.Month) | set(r.Month))

period = (
    st.sidebar.select_slider(
        "Select Month Range",
        options=months,
        value=(months[0], months[-1])
    )
    if len(months) > 1
    else (months[0], months[0])
)

# Filter data
def filt(d):
    return d[
        d.Country.isin(selected)
        & d.Month.between(*period)
    ]

s = filt(s)
r = filt(r)

# Calculate KPIs
gross = s.Revenue.sum()
orders = s.InvoiceNo.nunique()
customers = s.CustomerID.nunique()
net = gross + r.Revenue.sum()
average_order = gross / orders if orders else 0

# KPI section
st.subheader("Business Performance Overview")

a, b, c, d, e = st.columns(5)

a.metric("Gross Sales", f"£{gross:,.0f}")
b.metric("Net Recorded Value", f"£{net:,.0f}")
c.metric("Purchase Invoices", f"{orders:,}")
d.metric("Known Customers", f"{customers:,}")
e.metric("Average Invoice", f"£{average_order:,.2f}")

st.divider()

# Monthly sales analysis
st.subheader("Monthly Sales Analysis")

monthly = (
    s.groupby("Month", as_index=False)
    .Revenue.sum()
    .sort_values("Month")
)

fig_sales = px.line(
    monthly,
    x="Month",
    y="Revenue",
    title="Monthly Gross Sales Trend",
    markers=True,
    color_discrete_sequence=["#38BDF8"]
)

fig_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (£)",
    height=380
)

fig_sales.update_yaxes(tickprefix="£")

st.plotly_chart(fig_sales, width="stretch")

st.divider()

# Product and country analysis
a, b = st.columns(2)

# Top products
products = (
    s.groupby("StockCode", as_index=False)
    .Revenue.sum()
    .nlargest(10, "Revenue")
    .sort_values("Revenue")
)

# Treat stock codes as categories
products["StockCode"] = products["StockCode"].astype(str)

fig_products = px.bar(
    products,
    x="Revenue",
    y="StockCode",
    orientation="h",
    title="Top 10 Stock Codes by Revenue",
    color="Revenue",
    color_continuous_scale="Blues",
    text_auto=".3s"
)

fig_products.update_yaxes(
    type="category",
    categoryorder="total ascending"
)

fig_products.update_xaxes(tickprefix="£")

fig_products.update_layout(
    xaxis_title="Revenue (£)",
    yaxis_title="Stock Code",
    coloraxis_showscale=False,
    height=450
)

a.plotly_chart(fig_products, width="stretch")

# Top countries
countries = (
    s.groupby("Country", as_index=False)
    .Revenue.sum()
    .nlargest(10, "Revenue")
    .sort_values("Revenue")
)

fig_countries = px.bar(
    countries,
    x="Revenue",
    y="Country",
    orientation="h",
    title="Top 10 Markets by Revenue",
    color="Revenue",
    color_continuous_scale="Teal",
    text_auto=".3s"
)

fig_countries.update_xaxes(tickprefix="£")

fig_countries.update_yaxes(
    categoryorder="total ascending"
)

fig_countries.update_layout(
    xaxis_title="Revenue (£)",
    yaxis_title="Country",
    coloraxis_showscale=False,
    height=450
)

b.plotly_chart(fig_countries, width="stretch")

st.divider()

# Customer segmentation
st.subheader("RFM Customer Segmentation")

st.caption(
    "Customer segments are calculated using the full dataset "
    "and are not affected by the sidebar filters."
)

segments = (
    rfm.Segment.value_counts()
    .rename_axis("Segment")
    .reset_index(name="Customers")
)

a, b = st.columns(2)

# Customer segmentation bar chart
fig_segments = px.bar(
    segments,
    x="Segment",
    y="Customers",
    color="Segment",
    text="Customers",
    title="Customers by Segment"
)

fig_segments.update_traces(
    textposition="outside"
)

fig_segments.update_layout(
    showlegend=False,
    xaxis_title="Customer Segment",
    yaxis_title="Number of Customers",
    height=450
)

a.plotly_chart(fig_segments, width="stretch")

# Customer segmentation donut chart
fig_pie = px.pie(
    segments,
    names="Segment",
    values="Customers",
    hole=0.45,
    title="Customer Segment Distribution",
    color="Segment"
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent"
)

fig_pie.update_layout(height=450)

b.plotly_chart(fig_pie, width="stretch")

st.divider()

# Customer segmentation table
st.subheader("Customer Segment Summary")

st.dataframe(
    segments,
    width="stretch",
    hide_index=True
)

# Dataset limitations
st.subheader("Data Notes")

st.caption(
    "Gross sales excludes cancellations and nonpositive prices. "
    "Recorded returns are negative quantity lines without "
    "invoice matching. December 2011 contains partial-month "
    "data. Product rankings may include postage or miscellaneous "
    "stock codes. The dataset does not contain profit information."
)

st.markdown("---")

st.caption(
    "E-Commerce Data Analytics Project | "
    "Python, SQL, Pandas, Plotly & Streamlit | "
    "Source: UCI Online Retail Dataset"
)
