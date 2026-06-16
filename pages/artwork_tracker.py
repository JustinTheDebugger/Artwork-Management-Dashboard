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
        r.required,
        CASE
            WHEN r.required = FALSE
                THEN 'NOT_REQUIRED'
            WHEN c.product_code IS NOT NULL
                THEN 'YES'
            ELSE 'NO'
        END AS artwork_status
    FROM product_artwork_requirements r

    LEFT JOIN vw_product_artwork_coverage c
        ON c.product_code = r.product_code
        AND c.artwork_group = r.artwork_group

    LEFT JOIN products p
        ON p.product_code = r.product_code

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
            "required",
            "artwork_status"
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
        values="artwork_status",
        aggfunc="first",
        fill_value="NO"
    )

    return matrix


def format_matrix(matrix):

    def convert(value):

        if value == "YES":
            return "✅"

        if value == "NOT_REQUIRED":
            return "➖"

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

st.write(rows[0])

matrix = build_matrix(rows)

display = format_matrix(matrix)

display = display.reset_index()

# -------------------------
# COMPLETE STATUS
# -------------------------

artwork_cols = [
    col
    for col in display.columns
    if col not in [
        "product",
        "Complete"
    ]
]

display["Complete"] = (
    ~display[artwork_cols]
    .eq("❌")
    .any(axis=1)
)

display["Complete"] = display["Complete"].map(
    lambda x: "YES" if x else "NO"
)

filtered = display.copy()



# -------------------------
# METRICS
# -------------------------

total_products = len(display)

total_missing = (
    display[artwork_cols]
    .eq("❌")
    .sum()
    .sum()
)

complete_products = (
    display["Complete"]
    == "YES"
).sum()

incomplete_products = (
    display["Complete"]
    == "NO"
).sum()

total_required = (
    len(display)
    * len(artwork_cols)
)

coverage_rate = (
    (
        total_required
        - total_missing
    )
    / total_required
    * 100
    if total_required
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
    "Artwork Coverage %",
    f"{coverage_rate:.1f}%"
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
        filtered["product"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# Incomplete

if show_missing_only:

    filtered = filtered[
        filtered["Complete"] == "NO"
    ]

# Complete

if show_complete_only:

    filtered = filtered[
        filtered["Complete"] == "YES"
    ]

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
    options=filtered["product"].tolist()
)

if selected_product:

    product_code = selected_product.split(" - ")[0]

    details_df = load_product_details(
        product_code
    )

    # convert status to icons
    details_df["Status"] = details_df["Status"].map(
        lambda x:
            "✅" if x == "YES"
            else "➖" if x == "NOT_REQUIRED"
            else "❌"
    )

    original_df = details_df.copy()

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
            "Status"
        ]
    )

    for _, row in edited_df.iterrows():

        original_required = original_df.loc[
            original_df["Artwork Type"]
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

    