import os
from db import get_connection
from datetime import datetime
import pandas as pd

from services.qr_service import (
    generate_sample_qr
)
from services.product_service import (
    product_exists
)

from services.storage_service import (
    upload_sample_qr
)

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


# GET SAMPLE DETAILS
def get_sample_detail(sample_id):

    conn = get_connection()

    query = """
    SELECT
        s.*,
        st.sample_type_name,
        b.bin_name

    FROM samples s

    LEFT JOIN sample_types st
        ON s.sample_type_code = st.sample_type_code

    LEFT JOIN bin_locations b
        ON s.bin_location = b.bin_code

    WHERE s.sample_id = %s
    """

    df = pd.read_sql(
        query,
        conn,
        params=[sample_id]
    )

    conn.close()

    if df.empty:
        return None

    return df.iloc[0]

# GET SMAPLE MOVEMENTS
def get_sample_movements(sample_id):

    conn = get_connection()

    query = """
    SELECT
        movement_type,
        from_location,
        to_location,
        remarks,
        performed_by,
        created_at

    FROM sample_movements

    WHERE sample_id = %s

    ORDER BY created_at DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=[sample_id]
    )

    conn.close()

    return df

# CREATE NEW BIN LOCATION
def create_bin_location(
    bin_code,
    bin_name
):

    conn = get_connection()
    cur = conn.cursor()

    try:

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

    except:

        conn.rollback()
        raise

    finally:

        conn.close()

# CREATE SAMPLE PHOTOS
def create_sample_photo(
    sample_id,
    file_url,
    uploaded_by
):
    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO sample_photos
            (
                sample_id,
                file_url,
                uploaded_by
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                sample_id,
                file_url,
                uploaded_by
            )
        )

        conn.commit()

    except:

        conn.rollback()
        raise

    finally:

        conn.close()  

# DISPALY PHOTOS
def get_sample_photos(
    sample_id
):

    conn = get_connection()

    query = """
    SELECT
        file_url
    FROM sample_photos
    WHERE sample_id = %s
    ORDER BY uploaded_at
    """

    df = pd.read_sql(
        query,
        conn,
        params=[sample_id]
    )

    conn.close()

    return df


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

SAMPLE_TYPE_NAMES = {
    "MAS": "Master Sample",
    "SMS": "Salesman Sample",
    "DEV": "Development Sample",
    "PP": "Preproduction Sample"
}

# GENERATE SAMPLE NAME
def generate_sample_name(
    product_name,
    sample_type_code,
    received_date
):
    sample_type_name = SAMPLE_TYPE_NAMES.get(
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

def create_samples(
    product_code,
    product_name,
    sample_type_code,
    quantity,
    received_date,
    bin_location,
    remarks,
    created_by='Justin'
):
    if not product_exists(product_code):

        raise ValueError(
            f"Product {product_code} not found."
        )

    conn = get_connection()
    cur = conn.cursor()

    try:

        sample_ids = generate_sample_ids(
            product_code,
            sample_type_code,
            quantity
        )

        sample_name = generate_sample_name(
            product_name,
            sample_type_code,
            received_date
        )

        batch = received_date.strftime(
            "%Y-%m"
        )

        created_samples = []

        for sample_id in sample_ids:

            qr_path = generate_sample_qr(
                sample_id,
                sample_name
            )

            qr_url = upload_sample_qr(
                sample_id,
                qr_path
            )

            os.remove(qr_path)

            cur.execute(
                """
                INSERT INTO samples (
                    sample_id,
                    product_code,
                    sample_name,
                    sample_type_code,
                    sample_status,
                    bin_location,
                    remarks,
                    qr_code_url,
                    received_date,
                    created_batch,
                    created_by
                )
                VALUES (
                    %s,%s,%s,%s,
                    'AVAILABLE',
                    %s,%s,%s,%s,%s,%s
                )
                """,
                (
                    sample_id,
                    product_code,
                    sample_name,
                    sample_type_code,
                    bin_location,
                    remarks,
                    qr_url,
                    received_date,
                    batch,
                    created_by
                )
            )

            cur.execute(
                """
                INSERT INTO sample_movements (
                    sample_id,
                    movement_type,
                    to_location,
                    remarks,
                    performed_by
                )
                VALUES (
                    %s,
                    'CREATE',
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    sample_id,
                    bin_location,
                    remarks,
                    created_by
                )
            )

            created_samples.append(
                sample_id
            )

        conn.commit()

        return created_samples

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()
    
# BUILD A PREVIEW
def preview_sample_creation(
    product_code,
    product_name,
    sample_type_code,
    quantity,
    received_date
):

    sample_name = generate_sample_name(
        product_name,
        sample_type_code,
        received_date
    )

    sample_ids = generate_sample_ids(
        product_code,
        sample_type_code,
        quantity
    )

    return {
        "sample_name": sample_name,
        "sample_ids": sample_ids
    }

def get_samples(
    search=None,
    sample_type=None,
    status=None,
    bin_code=None
):
    conn = get_connection()

    query = """
        SELECT
            s.sample_id,
            s.sample_name,
            s.product_code,
            s.sample_type_code,
            st.sample_type_name,
            s.sample_status,
            s.bin_location,
            b.bin_name,
            s.current_holder,
            s.created_at,
            s.qr_code_url
        FROM samples as s
        LEFT JOIN sample_types as st
        ON s.sample_type_code =  st.sample_type_code
        LEFT JOIN bin_locations as b
        ON s.bin_location = b.bin_code
        WHERE 1=1
    """

    params = []

    if search:

        query += """
            AND (
                s.sample_id ILIKE %s
                OR
                s.sample_name ILIKE %s
                OR
                s.product_code ILIKE %s
            )
        """

        keyword = f"%{search}%"

        params.extend(
            [
                keyword,
                keyword,
                keyword
            ]
        )

    if sample_type:

        query += """
            AND s.sample_type_code = %s
        """

        params.append(
            sample_type
        )


    if status:

        query += """
            AND s.sample_status = %s
        """

        params.append(
            status
        )


    if bin_code:

        query += """
            AND s.bin_location = %s
        """

        params.append(
            bin_code
        )

    query += """
        ORDER BY s.created_at DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=params
    )


    conn.close()

    return df