import pandas as pd
from db import get_connection

def get_seasons():
    conn = get_connection()

    sql = """
    SELECT
        season_code,
        season_name
    FROM season_master
    WHERE active = TRUE
    ORDER BY season_code
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df

def get_categories():
    conn = get_connection()

    sql = """
    SELECT
        category_code,
        category_name
    FROM category_master
    WHERE active = TRUE
    ORDER BY category_code
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df

def get_products():
    conn = get_connection()

    sql = """
    SELECT
        p.product_code,
        p.product_name
    FROM products p
    ORDER BY p.product_name
    """

    df = pd.read_sql(sql, conn)

    conn.close()

    return df


def generate_product_code(
    season_code,
    category_code,
    variant_code="001"
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            COALESCE(MAX(sequence), 0)
        FROM product_master
        WHERE season_code = %s
        AND category_code = %s
        """,
        (
            season_code,
            category_code
        )
    )

    max_sequence = cur.fetchone()[0]

    conn.close()

    next_sequence = max_sequence + 1

    product_code = (
        f"{season_code}"
        f"{category_code}"
        f"{next_sequence:02d}"
        f"-{variant_code}"
    )

    return {
        "product_code": product_code,
        "sequence": next_sequence
    }

def create_product(
    season_code,
    category_code,
    product_name,
    variant_code,
    created_by
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        generated = generate_product_code(
            season_code,
            category_code,
            variant_code
        )

        product_code = generated["product_code"]
        sequence = generated["sequence"]

        cur.execute(
            """
            INSERT INTO products (
                product_code,
                product_name
            )
            VALUES (%s, %s)
            """,
            (
                product_code,
                product_name
            )
        )

        cur.execute(
            """
            INSERT INTO product_master (
                product_code,
                season_code,
                category_code,
                sequence,
                variant_code,
                created_by
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                product_code,
                season_code,
                category_code,
                sequence,
                variant_code,
                created_by
            )
        )

        conn.commit()

        return product_code

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()

def get_product(product_code):

    conn = get_connection()

    sql = """
    SELECT
        p.product_code,
        p.product_name,
        pm.season_code,
        pm.category_code,
        pm.sequence,
        pm.variant_code
    FROM products p
    LEFT JOIN product_master pm
        ON pm.product_code = p.product_code
    WHERE p.product_code = %s
    """

    df = pd.read_sql(
        sql,
        conn,
        params=[product_code]
    )

    conn.close()

    return df

def product_exists(product_code):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM products
        WHERE product_code = %s
        """,
        (product_code,)
    )

    result = cur.fetchone()

    conn.close()

    return result is not None