import streamlit as st
import pandas as pd
from db import get_connection
from db import (
    load_product_details,
    update_artwork_requirement
)

# -------------------------
# DB
# -------------------------

conn = get_connection()

# -------------------------
# LOAD DATA
# -------------------------

def load_data():

    sql = """
    SELECT
        r.product_code,
        COALESCE(
            p.product_name,
            '(Unknown Product)'
        ) AS product_name,
        r.artwork_group,
        CASE
            WHEN c.product_code IS NOT NULL
            THEN 'YES'
            ELSE 'NO'
        END AS status
    FROM product_artwork_requirements r

    LEFT JOIN vw_product_artwork_coverage c
        ON c.product_code = r.product_code
        AND c.artwork_group = r.artwork_group

    LEFT JOIN products p
        ON p.product_code = r.product_code

    WHERE r.required = TRUE

    ORDER BY
        r.product_code,
        r.artwork_group
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(sql)

            return cur.fetchall()


# -------------------------
# BUILD MATRIX
# -------------------------

def build_matrix(rows):

    df = pd.DataFrame(
        rows,
        columns=[
            "product_code",
            "product_name",
            "artwork_group",
            "status"
        ]
    )

    df["product"] = (
        df["product_code"]
        + " - "
        + df["product_name"]
    )

    matrix = df.pivot_table(
        index="product",
        columns="artwork_group",
        values="status",
        aggfunc="first",
        fill_value="NO"
    )

    return matrix


# -------------------------
# FORMAT
# -------------------------

def format_matrix(matrix):

    def convert(value):

        if value == "YES":
            return "✅"

        return "❌"

    return matrix.map(convert)


# -------------------------
# PAGE
# -------------------------

st.set_page_config(
    page_title="Artwork Tracker",
    layout="wide"
)

st.title("📦 Artwork Tracker Dashboard")

# -------------------------
# LOAD
# -------------------------

rows = load_data()

matrix = build_matrix(rows)

display = format_matrix(matrix)

# -------------------------
# METRICS
# -------------------------

total_products = len(display)

complete_products = (
    display.eq("✅")
    .all(axis=1)
    .sum()
)

incomplete_products = (
    total_products
    - complete_products
)

completion_rate = (
    complete_products
    / total_products
    * 100
    if total_products
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Products",
    total_products
)

col2.metric(
    "Complete",
    complete_products
)

col3.metric(
    "Incomplete",
    incomplete_products
)

col4.metric(
    "Completion %",
    f"{completion_rate:.1f}%"
)

# -------------------------
# FILTERS
# -------------------------

st.sidebar.header("Filters")

search_text = st.sidebar.text_input(
    "Search Product"
)

show_missing_only = st.sidebar.checkbox(
    "Incomplete Only"
)

show_complete_only = st.sidebar.checkbox(
    "Complete Only"
)

filtered = display.copy()

# Search

if search_text:

    filtered = filtered[
        filtered.index.str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# Incomplete

if show_missing_only:

    filtered = filtered[
        ~(filtered == "✅")
        .all(axis=1)
    ]

# Complete

if show_complete_only:

    filtered = filtered[
        (filtered == "✅")
        .all(axis=1)
    ]

# -------------------------
# MISSING COUNT
# -------------------------

filtered["Missing"] = (
    filtered == "❌"
).sum(axis=1)

# -------------------------
# DISPLAY
# -------------------------

st.dataframe(
    filtered,
    width="stretch",
    height=900
)

selected_product = st.selectbox(
    "View Product Details",
    options=filtered.index.tolist()
)

if selected_product:

    product_code = selected_product.split(" - ")[0]

    details_df = load_product_details(
        product_code
    )

    details_df["Exists"] = details_df[
        "Exists"
    ].map(
        lambda x: "✅" if x else "❌"
    )

    st.subheader(selected_product)

    edited_df = st.data_editor(
        details_df,
        hide_index=True,
        width="stretch",
        column_config={
            "Required": st.column_config.CheckboxColumn(
                "Required"
            )
        },
        disabled=[
            "Artwork Type",
            "Exists"
        ]
    )

    for _, row in edited_df.iterrows():

        original_required = details_df.loc[
            details_df["Artwork Type"]
            == row["Artwork Type"],
            "Required"
        ].iloc[0]

        if original_required != row["Required"]:

            with st.spinner(
                f"Saving {row['Artwork Type']}..."
            ):

                update_artwork_requirement(
                    product_code,
                    row["Artwork Type"],
                    row["Required"]
                )

            st.rerun()
        

    