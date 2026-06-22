from datetime import datetime, date
from services.database import get_connection

# get available samples
def get_available_samples():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.sample_id,
            s.sample_name,
            s.product_code,
            s.sample_status,
            s.sample_type_code

        FROM samples s

        JOIN sample_types st
        ON s.sample_type_code = st.sample_type_code

        WHERE
            s.sample_status = 'AVAILABLE'
        AND
            st.allow_booking = TRUE

        ORDER BY
            s.product_code
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# create booking
def create_booking(
    booked_by,
    department,
    purpose,
    booking_start_date,
    expected_return_date,
    notes,
    sample_ids
):

    conn = get_connection()

    try:

        cur = conn.cursor()


        # booking header

        cur.execute("""
            INSERT INTO bookings
            (
                booked_by,
                department,
                purpose,
                booking_start_date,
                expected_return_date,
                notes
            )

            VALUES
            (%s,%s,%s,%s,%s,%s)

            RETURNING booking_id
        """,
        (
            booked_by,
            department,
            purpose,
            booking_start_date,
            expected_return_date,
            notes
        ))

        booking_id = cur.fetchone()[0]


        # booking items

        for sample_id in sample_ids:

            cur.execute("""
                INSERT INTO booking_items
                (
                    booking_id,
                    sample_id
                )

                VALUES
                (%s,%s)
            """,
            (
                booking_id,
                sample_id
            ))


            # reserve sample

            cur.execute("""
                UPDATE samples

                SET sample_status='RESERVED'

                WHERE sample_id=%s
            """,
            (sample_id,))


        conn.commit()

        return booking_id


    except Exception:

        conn.rollback()
        raise


    finally:

        cur.close()
        conn.close()

# active bookings
def get_active_bookings():

    conn=get_connection()
    cur=conn.cursor()


    cur.execute("""
        SELECT

            b.booking_id,
            b.booked_by,
            b.purpose,
            b.expected_return_date,

            s.sample_id,
            s.sample_name,
            s.product_code


        FROM bookings b


        JOIN booking_items bi

        ON b.booking_id=bi.booking_id


        JOIN samples s

        ON bi.sample_id=s.sample_id


        WHERE
        b.booking_status='ACTIVE'


        ORDER BY
        b.expected_return_date

    """)


    rows=cur.fetchall()


    cur.close()
    conn.close()


    return rows

# return booking
def return_booking(booking_id):

    conn=get_connection()
    cur=conn.cursor()


    try:

        # release samples

        cur.execute("""
            UPDATE samples

            SET sample_status='AVAILABLE'

            WHERE sample_id IN

            (
                SELECT sample_id

                FROM booking_items

                WHERE booking_id=%s
            )

        """,
        (booking_id,))


        # update booking

        cur.execute("""
            UPDATE bookings

            SET
            booking_status='RETURNED',
            returned_date=%s

            WHERE booking_id=%s

        """,
        (
            datetime.utcnow(),
            booking_id
        ))


        conn.commit()


    except Exception:

        conn.rollback()
        raise


    finally:

        cur.close()
        conn.close()

# overdue check
def mark_overdue_bookings():

    today = date.today()

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE bookings

            SET booking_status = 'OVERDUE'

            WHERE expected_return_date < %s

            AND booking_status = 'ACTIVE'

        """,
        (today,))


        updated_count = cur.rowcount

        conn.commit()

        return updated_count


    except Exception:

        conn.rollback()
        raise


    finally:

        cur.close()
        conn.close()