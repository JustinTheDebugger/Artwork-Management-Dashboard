from db import get_connection
from datetime import datetime
import pandas as pd

# GET PRODUCTS - DROPDOWN
def get_products():
    conn = get_connection()

    sql = """
    SELECT
        product_code,
        product_name
    FROM products
    ORDER BY product_name
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df

# GET SAMPLE TYPES  
def get_sample_types():
    conn = get_connection()

    sql = """
    SELECT
        sample_type_code,
        sample_type_name,
        allow_booking
    FROM sample_types
    WHERE active = TRUE
    ORDER BY sample_type_name
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df

# GET BIN LOCATIONS
def get_bin_locations():
    conn = get_connection()

    sql = """
    SELECT
        bin_code,
        bin_name
    FROM bin_locations
    WHERE active = TRUE
    ORDER BY bin_code
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return df

# CREATE NEW NIN LOCATION
def create_bin_location(
    bin_code,
    bin_name
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO bin_locations (
            bin_code,
            bin_name
        )
        VALUES (%s, %s)
        """,
        (
            bin_code,
            bin_name
        )
    )

    conn.commit()
    conn.close()

# GET NEXT SAMPLE SEQUENCE
def get_next_sequence(
    product_code,
    sample_type_code
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            COALESCE(
                MAX(
                    CAST(
                        RIGHT(sample_id, 2)
                        AS INTEGER
                    )
                ),
                0
            )
        FROM samples
        WHERE product_code = %s
        AND sample_type_code = %s
        """,
        (
            product_code,
            sample_type_code
        )
    )

    next_seq = cur.fetchone()[0] + 1

    conn.close()

    return next_seq

# GENERATE SAMPLE IDS
def generate_sample_ids(
    product_code,
    sample_type_code,
    quantity
):
    start_seq = get_next_sequence(
        product_code,
        sample_type_code
    )

    sample_ids = []

    for i in range(quantity):

        seq = start_seq + i

        sample_id = (
            f"{product_code}S-"
            f"{sample_type_code}-"
            f"{seq:02d}"
        )

        sample_ids.append(sample_id)

    return sample_ids

# GENERATE SAMPLE NAME
def generate_sample_name(
    product_name,
    sample_type_code,
    received_date
):
    sample_type_name = SAMPLE_TYPE_MAP.get(
        sample_type_code,
        sample_type_code
    )

    batch_date = received_date.strftime(
        "%Y-%m"
    )

    return (
        f"{product_name} "
        f"{sample_type_name} "
        f"{batch_date}"
    )

# CREATE SAMPLES
def create_samples(
    product_code,
    product_name,
    sample_type_code,
    quantity,
    bin_location,
    received_date,
    remarks,
    created_by
):