import streamlit as st
from db import get_connection
from db import get_all_artworks

st.set_page_config(
    page_title="Artwork Tracker",
    layout="wide"
)

st.title("Artwork Management Dashboard")
st.write(st.secrets["dbname"])
conn = get_connection()

df = get_all_artworks()

summary_df = (
    df.groupby(
        ["product_code", "product_name"]
    )
    .size()
    .reset_index(name="artwork_count")
)

st.subheader("Products")

st.dataframe(
    summary_df,
    use_container_width=True
)

# Filters

product_name = st.text_input("Product Name")

if product_name:
    df = df[
        df["product_name"]
        .astype(str)
        .str.contains(product_name, case=False)
    ]

st.dataframe(df, use_container_width=True)