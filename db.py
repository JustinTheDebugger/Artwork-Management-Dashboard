import pandas as pd
import streamlit as st
import psycopg

def get_connection():
    return psycopg.connect(
        st.secrets["DATABASE_URL"]
    )

# def get_products():

# def get_artwork_by_product(product_code):

# def get_latest_artwork():

def get_all_artworks():

    with get_connection() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM artwork_files
            ORDER BY release_date DESC
            """,
            conn
        )