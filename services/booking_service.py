from services.database import get_connection
from datetime import datetime, date


# -----------------------------------
# Available samples for booking
# -----------------------------------

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



# -----------------------------------
# Create booking
# -----------------------------------

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


        # Create booking header

        cur.execute("""
            INSERT INTO bookings
            (
                booked_by,
                department,
                purpose,
                booking_status,
                booking_start_date,
                expected_return_date,
                notes
            )

            VALUES
            (
                %s,
                %s,
                %s,
                'ACTIVE',
                %s,
                %s,
                %s
            )

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


        # Add booking items

        for sample_id in sample_ids:

            cur.execute("""
                INSERT INTO booking_items
                (
                    booking_id,
                    sample_id,
                    item_status
                )

                VALUES
                (
                    %s,
                    %s,
                    'BOOKED'
                )

            """,
            (
                booking_id,
                sample_id
            ))



            # Reserve sample

            cur.execute("""
                UPDATE samples

                SET sample_status='RESERVED'

                WHERE sample_id=%s

            """,
            (
                sample_id,
            ))



        conn.commit()

        return booking_id



    except Exception:

        conn.rollback()
        raise



    finally:

        cur.close()
        conn.close()




# -----------------------------------
# Calendar data
# -----------------------------------

def get_booking_calendar():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            b.booking_id,
            b.booked_by,
            b.purpose,
            b.booking_start_date,
            b.expected_return_date,

            STRING_AGG(
                s.product_code,
                ', '
            ) AS samples

        FROM bookings b

        JOIN booking_items bi
            ON b.booking_id = bi.booking_id

        JOIN samples s
            ON bi.sample_id = s.sample_id

        WHERE b.booking_status = 'ACTIVE'

        GROUP BY
            b.booking_id,
            b.booked_by,
            b.purpose,
            b.booking_start_date,
            b.expected_return_date

        ORDER BY
            b.booking_start_date
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows




# -----------------------------------
# Active bookings
# -----------------------------------

def get_active_bookings():

    return get_booking_calendar()




# -----------------------------------
# Return booking
# -----------------------------------

def return_booking(booking_id):

    conn = get_connection()
    cur = conn.cursor()


    try:


        # Release samples

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
        (
            booking_id,
        ))



        # Update booking items

        cur.execute("""
            UPDATE booking_items

            SET
                item_status='RETURNED',
                returned_date=NOW()

            WHERE booking_id=%s

        """,
        (
            booking_id,
        ))



        # Update booking

        cur.execute("""
            UPDATE bookings

            SET

                booking_status='RETURNED',

                returned_date=NOW()


            WHERE booking_id=%s

        """,
        (
            booking_id,
        ))



        conn.commit()



    except Exception:

        conn.rollback()
        raise



    finally:

        cur.close()
        conn.close()




# -----------------------------------
# Mark overdue
# -----------------------------------

def mark_overdue_bookings():

    conn = get_connection()
    cur = conn.cursor()


    cur.execute("""
        UPDATE bookings

        SET booking_status='OVERDUE'


        WHERE

        expected_return_date < CURRENT_DATE

        AND

        booking_status='ACTIVE'

    """)


    conn.commit()

    cur.close()
    conn.close()