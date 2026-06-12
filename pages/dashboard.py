import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_all_artworks

st.set_page_config(
    page_title="Artwork Dashboard",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Artwork Management Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_all_artworks()

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------

total_products = df["product_code"].nunique()

total_artworks = len(df)

product_summary = (
    df.groupby(
        ["product_code", "product_name"]
    )
    .size()
    .reset_index(name="artwork_count")
)

complete_products = len(
    product_summary[
        product_summary["artwork_count"] >= 5
    ]
)

missing_products = (
    total_products - complete_products
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Products",
        f"{total_products:,}"
    )

with col2:
    st.metric(
        "Artwork Files",
        f"{total_artworks:,}"
    )

with col3:
    st.metric(
        "Complete Products",
        f"{complete_products:,}"
    )

with col4:
    st.metric(
        "Missing Products",
        f"{missing_products:,}"
    )

st.divider()

# --------------------------------------------------
# Charts
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Artwork Coverage")

    coverage_df = (
        df.groupby("artwork_group")
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        coverage_df,
        x="artwork_group",
        y="count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top Products")

    top_products = (
        product_summary
        .sort_values(
            "artwork_count",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="artwork_count",
        y="product_name",
        orientation="h"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# Search
# --------------------------------------------------

st.subheader("Search Products")

search = st.text_input(
    "",
    placeholder="Search by product code or product name..."
)

filtered_df = product_summary.copy()

if search:

    filtered_df = filtered_df[
        filtered_df["product_code"]
        .astype(str)
        .str.contains(search, case=False)
        |
        filtered_df["product_name"]
        .astype(str)
        .str.contains(search, case=False)
    ]

# --------------------------------------------------
# Product Summary
# --------------------------------------------------

st.subheader("Product Summary")

st.dataframe(
    filtered_df.sort_values(
        "product_name"
    ),
    use_container_width=True,
    hide_index=True
)