import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("sample_data.csv", parse_dates=["date"])
    return df

df = load_data()

st.title("📊 Sample Sales Dashboard")
st.caption("Dummy data loaded from sample_data.csv")

# --- Exploratory Data Analysis ---
with st.expander("🔍 Exploratory Data Analysis", expanded=False):
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    st.write("**Column types**")
    st.dataframe(df.dtypes.astype(str).rename("dtype"), width='stretch')

    st.write("**Missing values**")
    st.dataframe(df.isna().sum().rename("missing_count"), width='stretch')

    st.write("**Summary statistics (numeric columns)**")
    st.dataframe(df.describe(), width='stretch')

    st.write("**Correlation matrix (numeric columns)**")
    st.dataframe(df.select_dtypes("number").corr(), width='stretch')

    st.write("**Distribution of sales**")
    st.bar_chart(df["sales"].value_counts(bins=8).sort_index())

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))

filtered = df[df["region"].isin(regions) & df["category"].isin(categories)]

# KPI row
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered['sales'].sum():,.0f}")
col2.metric("Total Units", f"{filtered['units'].sum():,.0f}")
col3.metric("Total Profit", f"${filtered['profit'].sum():,.0f}")

st.divider()

# Sales over time
st.subheader("Sales Over Time")
sales_by_date = filtered.groupby("date")["sales"].sum()
st.line_chart(sales_by_date)

col4, col5 = st.columns(2)

with col4:
    st.subheader("Sales by Category")
    st.bar_chart(filtered.groupby("category")["sales"].sum())

with col5:
    st.subheader("Sales by Region")
    st.bar_chart(filtered.groupby("region")["sales"].sum())

st.subheader("Profit vs. Units Sold")
st.scatter_chart(filtered, x="units", y="profit", color="category")

st.subheader("Raw Data")
st.dataframe(filtered, width='stretch')
