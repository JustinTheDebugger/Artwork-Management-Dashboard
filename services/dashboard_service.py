from db import get_connection


def get_artwork_kpis():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            status,
            COUNT(*)
        FROM artwork_files
        GROUP BY status
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()


    result = {
        "Draft": 0,
        "Approved": 0,
        "Rejected": 0,
        "Released": 0,
        "Superseded": 0
    }


    for status, count in rows:
        if status in result:
            result[status] = count


    return result