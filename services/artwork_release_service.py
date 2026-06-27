from db import get_connection


def get_approved_artworks():

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
            af.status,
            af.uploaded_at

        FROM artwork_files af

        LEFT JOIN products p
            ON af.full_product_code = p.product_code

        WHERE af.status = 'Approved'

        ORDER BY
            af.uploaded_at ASC
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows



def release_artwork(
    artwork_id,
    released_by
):

    conn = get_connection()
    cur = conn.cursor()


    # Get artwork identity

    cur.execute(
        """
        SELECT
            full_product_code,
            artwork_group

        FROM artwork_files

        WHERE id = %s
        """,
        (
            artwork_id,
        )
    )


    artwork = cur.fetchone()


    if not artwork:

        raise Exception(
            "Artwork not found"
        )


    product_code = artwork[0]
    artwork_group = artwork[1]


    # Remove previous release

    cur.execute(
        """
        UPDATE artwork_files

        SET status = 'Superseded'

        WHERE
            full_product_code = %s
            AND artwork_group = %s
            AND status = 'Released'
        """,
        (
            product_code,
            artwork_group
        )
    )


    # Release selected artwork

    cur.execute(
        """
        UPDATE artwork_files

        SET
            status = 'Released',
            released_by = %s,
            released_at = NOW()

        WHERE id = %s
        """,
        (
            released_by,
            artwork_id
        )
    )


    conn.commit()


    cur.close()
    conn.close()