import pandas as pd
import streamlit as st
import psycopg

def get_connection():

    return psycopg.connect(
        host=st.secrets["host"],
        dbname=st.secrets["dbname"],
        user=st.secrets["user"],
        password=st.secrets["password"],
        sslmode="require",
        options=st.secrets["options"]
    )

# def get_connection():
#     return psycopg.connect(
#         host="ep-late-rain-a7epxzsy-pooler.ap-southeast-2.aws.neon.tech",
#         dbname="neondb",
#         user="neondb_owner",
#         password="npg_VsvbSpul5Ch0",
#         sslmode="require",
#         options="endpoint=ep-late-rain-a7epxzsy"
#     )

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