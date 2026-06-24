from datetime import datetime, date
from services.database import get_connection

def get_artwork_review_queue():

    conn = get_connection()

    query = """
    SELECT
        af.id,
        COALESCE(
            p.product_name,
            af.product_name,
            af.full_product_code
        ) AS product_name,
        af.artwork_group,
        af.filename,
        af.file_path,
        af.status,
        af.upload_id,
        af.uploaded_at,
        af.storage_url

    FROM artwork_files af

    LEFT JOIN products p
        ON af.full_product_code = p.product_code

    ORDER BY
        af.uploaded_at DESC
    """

    cur = conn.cursor()

    cur.execute(query)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def update_artwork_status(
    artwork_id,
    status
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE artwork_files
        SET review_status = %s
        WHERE id = %s
        """,
        (
            status,
            artwork_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()