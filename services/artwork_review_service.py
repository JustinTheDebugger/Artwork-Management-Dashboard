from datetime import datetime, date
from services.database import get_connection

from db import get_connection


def get_draft_artwork_queue():

    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT
            af.id,
            COALESCE(
                p.product_name,
                af.product_name,
                af.full_product_code,
                'Unknown Product'
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

        WHERE af.status = 'Draft'

        ORDER BY
            af.uploaded_at ASC
        """
    )


    rows = cur.fetchall()


    cur.close()
    conn.close()


    return rows

# Save review
def save_artwork_review(
    artwork_id,
    reviewed_by,
    review_status,
    review_comments
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO artwork_reviews
        (
            artwork_id,
            reviewed_by,
            review_status,
            review_comments,
            reviewed_at
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            NOW()
        )
        """,
        (
            artwork_id,
            reviewed_by,
            review_status,
            review_comments
        )
    )

    conn.commit()

    cur.close()
    conn.close()

# Update artwork status
def update_artwork_status(
    artwork_id,
    status
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE artwork_files
        SET status = %s
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