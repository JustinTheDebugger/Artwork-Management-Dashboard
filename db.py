import pandas as pd
import streamlit as st
import psycopg

def get_connection():
    return psycopg.connect(
        st.secrets["DATABASE_URL"]
    )


def get_all_artworks():
    conn = get_connection()

    query = """
    SELECT
        c.product_code,
        p.product_name,
        c.artwork_group
    FROM vw_product_artwork_coverage_clean c
    LEFT JOIN products p
        ON c.product_code = p.product_code
    """

    return pd.read_sql(query, conn)