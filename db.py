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

def load_product_details(product_code):

    sql = """
    SELECT
        r.artwork_group,
        r.required,
        CASE
            WHEN c.product_code IS NOT NULL
            THEN TRUE
            ELSE FALSE
        END AS exists
    FROM product_artwork_requirements r

    LEFT JOIN vw_product_artwork_coverage c
        ON c.product_code = r.product_code
        AND c.artwork_group = r.artwork_group

    WHERE r.product_code = %s

    ORDER BY r.artwork_group
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(sql, (product_code,))

            return pd.DataFrame(
                cur.fetchall(),
                columns=[
                    "Artwork Type",
                    "Required",
                    "Exists"
                ]
            )

def update_artwork_requirement(
    product_code,
    artwork_group,
    required
):

    sql = """
    UPDATE product_artwork_requirements
    SET required = %s
    WHERE product_code = %s
      AND artwork_group = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                sql,
                (
                    required,
                    product_code,
                    artwork_group
                )
            )

        conn.commit()

def get_requirements(product_code):

    sql = """
    SELECT artwork_group
    FROM product_artwork_requirements
    WHERE product_code = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (product_code,))
            return [r[0] for r in cur.fetchall()]
        
def get_existing(product_code):

    sql = """
    SELECT DISTINCT artwork_group
    FROM artwork_files
    WHERE full_product_code = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (product_code,))
            return {r[0] for r in cur.fetchall()}