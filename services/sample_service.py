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

# GENERATE UNIQUE SAMPLE ID
def generate_sample_ids(
    product_code=None,
    sample_type_code=None,
    quantity=1
):

    conn = get_connection()
    cur = conn.cursor()

    sample_ids = []

    try:

        if product_code:

            prefix = (
                f"{product_code}S-{sample_type_code}-"
            )

            cur.execute(
                """
                SELECT sample_id
                FROM samples
                WHERE sample_id LIKE %s
                ORDER BY sample_id DESC
                """,
                (
                    f"{prefix}%",
                )
            )

            existing_ids = [
                row[0]
                for row in cur.fetchall()
            ]


            max_number = 0

            for sample_id in existing_ids:

                try:

                    number = int(
                        sample_id.split("-")[-1]
                    )

                    max_number = max(
                        max_number,
                        number
                    )

                except:
                    pass


            for i in range(quantity):

                sample_ids.append(
                    f"{prefix}{max_number+i+1:02d}"
                )


        else:

            cur.execute(
                """
                SELECT COALESCE(
                    MAX(
                        CAST(
                            REPLACE(sample_id, 'DEV-', '')
                            AS INTEGER
                        )
                    ),
                    0
                )
                FROM samples
                WHERE sample_id LIKE 'DEV-%'
                """
            )

            max_number = cur.fetchone()[0]


            for i in range(quantity):

                sample_ids.append(
                    f"DEV-{max_number+i+1:06d}"
                )


        return sample_ids


    finally:

        conn.close()


# GET SAMPLE TYPE
def get_sample_type_names():
    conn = get_connection()

    sql = """
    SELECT
        sample_type_code,
        sample_type_name
    FROM sample_types
    WHERE active = TRUE
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    return dict(
        zip(
            df["sample_type_code"],
            df["sample_type_name"]
        )
    )

# GENERATE SAMPLE NAME
def generate_sample_name(
    product_name,
    sample_type_code,
    received_date
):
    SAMPLE_TYPE_NAMES = get_sample_type_names()

    sample_type_name = SAMPLE_TYPE_NAMES.get(
        sample_type_code,
        sample_type_code
    )

    return (
        f"{product_name} "
        f"{sample_type_name} "
        f"{received_date}"
    )

def create_samples(
    product_code=None,
    product_name=None,
    prototype_name=None,
    sample_type_code=None,
    quantity=1,
    received_date=None,
    bin_location=None,
    remarks=None,
    photos=None,
    created_by=None
):
    # Commercial sample ->  product_code = 0266661-001
    if product_code:

        if not product_exists(product_code):

            raise ValueError(
                f"Product {product_code} not found."
            )
    # Prototype -> product_code = NULL, prototype_name = New Sample Name
    else:

        if not prototype_name:

            raise ValueError(
                "Prototype name required when product is not selected."
            )

    conn = get_connection()
    cur = conn.cursor()

    try:

        sample_ids = generate_sample_ids(
            product_code,
            sample_type_code,
            quantity
        )

        sample_base_name = (
            product_name

            if product_name
            else prototype_name
        )

        batch_date = received_date.strftime(
            "%Y-%m"
        )

        sample_name = generate_sample_name(
            sample_base_name,
            sample_type_code,
            batch_date
        )

        created_samples = []

        for sample_id in sample_ids:

            # temp qr storage
            qr_path = generate_sample_qr(
                sample_id,
                sample_name
            )

            # store in supabase storage
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
                    product_name,
                    prototype_name,
                    sample_name,
                    sample_type_code,
                    received_date,
                    bin_location,
                    remarks,
                    qr_code_url,
                    created_by
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    sample_id,
                    product_code,
                    product_name,
                    prototype_name,
                    sample_name,
                    sample_type_code,
                    received_date,
                    bin_location,
                    remarks,
                    qr_url,
                    created_by
                ) 
            )

            created_samples.append(
                sample_id
            )

        conn.commit()

        for sample_id in created_samples:

            create_sample_movement(
                sample_id=sample_id,
                movement_type="RECEIVED",
                to_location=bin_location,
                remarks=remarks or "Sample received into inventory",
                performed_by=created_by
            )

        return created_samples

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()
    
# BUILD A PREVIEW
def preview_sample_creation(
    product_code=None,
    product_name=None,
    prototype_name=None,
    sample_type_code=None,
    quantity=1,
    received_date=None
):

    sample_base_name = (
        product_name

        if product_name
        else prototype_name
    )

    batch_date = received_date.strftime(
        "%Y-%m"
    )

    sample_name = generate_sample_name(
        sample_base_name,
        sample_type_code,
        batch_date
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

# CREATE SAMPLE MOVEMENT
def create_sample_movement(
    sample_id,
    movement_type,
    from_location=None,
    to_location=None,
    booking_id=None,
    remarks=None,
    performed_by=None
):
    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO sample_movements
            (
                sample_id,
                movement_type,
                from_location,
                to_location,
                booking_id,
                remarks,
                performed_by
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                sample_id,
                movement_type,
                from_location,
                to_location,
                booking_id,
                remarks,
                performed_by
            )
        )

        conn.commit()

    except:

        conn.rollback()
        raise

    finally:

        conn.close()

# UPDATE SAMPLE
def update_sample(
    sample_id,
    bin_location,
    sample_status,
    current_holder,
    remarks,
    updated_by
):
    sample = get_sample_detail(
        sample_id
    )

    old_bin = sample.bin_location
    old_status = sample.sample_status

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE samples
            SET
                bin_location = %s,
                sample_status = %s,
                current_holder = %s,
                remarks = %s,
                updated_by = %s,
                updated_at = NOW()
            WHERE sample_id = %s
            """,
            (
                bin_location,
                sample_status,
                current_holder,
                remarks,
                updated_by,
                sample_id
            )
        )

        conn.commit()

    except:

        conn.rollback()
        raise

    finally:

        conn.close()

    if old_bin != bin_location:

        create_sample_movement(
            sample_id=sample_id,
            movement_type="LOCATION_CHANGE",
            from_location=old_bin,
            to_location=bin_location,
            performed_by=updated_by
        )

    if old_status != sample_status:

        create_sample_movement(
            sample_id=sample_id,
            movement_type="STATUS_CHANGE",
            remarks=f"{old_status} -> {sample_status}",
            performed_by=updated_by
        )