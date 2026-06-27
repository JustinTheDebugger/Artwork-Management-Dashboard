from db import get_connection


def get_artwork_library():

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

            af.full_product_code,
            af.artwork_group,
            af.filename,
            af.storage_url,
            af.status,
            af.uploaded_at,

            ar.review_status,
            ar.reviewed_by,
            ar.review_comments,
            ar.reviewed_at,

            af.released_by,
            af.released_at

        FROM artwork_files af

        LEFT JOIN products p
            ON af.full_product_code = p.product_code

        LEFT JOIN artwork_reviews ar
            ON af.id = ar.artwork_id

        ORDER BY
            product_name,
            artwork_group
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def get_artwork_history(
    product_code,
    artwork_group
):

    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT

            af.id,
            af.filename,
            af.status,
            af.uploaded_at,

            ar.review_status,
            ar.reviewed_by,
            ar.review_comments,
            ar.reviewed_at,

            af.released_by,
            af.released_at,

            af.storage_url


        FROM artwork_files af


        LEFT JOIN LATERAL (

            SELECT *

            FROM artwork_reviews r

            WHERE r.artwork_id = af.id

            ORDER BY reviewed_at DESC

            LIMIT 1

        ) ar ON TRUE


        WHERE
            af.full_product_code = %s

        AND
            af.artwork_group = %s


        ORDER BY
            af.uploaded_at DESC

        """,
        (
            product_code,
            artwork_group
        )
    )


    rows = cur.fetchall()

    cur.close()
    conn.close()


    return rows