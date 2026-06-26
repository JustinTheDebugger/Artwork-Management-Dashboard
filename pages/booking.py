import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

from services.booking_service import (
    get_available_samples,
    get_active_bookings,
    create_booking,
    return_booking
)

# page header
st.set_page_config(
    page_title="Sample Booking",
    layout="wide"
)

st.title("📅 Sample Booking Dashboard")

# dashboard counters
active_bookings = get_active_bookings()
available_samples = get_available_samples()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Active Bookings",
        len(active_bookings)
    )

with col2:
    st.metric(
        "Available Samples",
        len(available_samples)
    )

# calendar view
calendar_events = []


for booking in active_bookings:

    (
        booking_id,
        booked_by,
        purpose,
        booking_start_date,
        expected_return_date,
        samples

    ) = booking


    calendar_events.append({

        "title":
            f"{purpose} - {booked_by}",

        "start":
            str(booking_start_date),

        "end":
            str(expected_return_date),

        "allDay":
            True,

        "extendedProps": {

            "samples": samples,
            "booking_id": str(booking_id)

        }

    })

# display calendar
st.subheader("Booking Calendar")

calendar(
    events=calendar_events,
    options={
        "initialView": "dayGridMonth",
        "height": 600
    }
)

# new booking form
st.divider()

st.subheader("Create Booking")

sample_options = {}

for sample in available_samples:

    (
        sample_id,
        sample_name,
        product_code,
        status,
        sample_type

    ) = sample


    label = (
        f"{sample_id} | "
        f"{sample_name}"
    )


    sample_options[label] = sample_id

selected = st.multiselect(
    "Select Samples",
    options=list(sample_options.keys())
)

col1, col2 = st.columns(2)

with col1:

    booked_by = st.text_input(
        "Booked By"
    )

    booking_start_date = st.date_input(
        "Booking Start Date"
    )


with col2:

    department = st.text_input(
        "Department"
    )

    expected_return = st.date_input(
        "Expected Return Date"
    )

purpose = st.text_input(
    "Purpose"
)

notes = st.text_area(
    "Notes"
)

if st.button(
    "Create Booking",
    type="primary"
):

    if not selected:

        st.warning(
            "Please select at least one sample"
        )


    elif not booked_by:

        st.warning(
            "Please enter booked by"
        )


    else:

        sample_ids = [
            sample_options[x]
            for x in selected
        ]


        booking_id = create_booking(
            booked_by,
            department,
            purpose,
            booking_start_date,
            expected_return,
            notes,
            sample_ids
        )

        st.success(
            f"Booking created: {booking_id}"
        )


        st.rerun()

st.divider()

st.subheader("Active Booking List")

for booking in active_bookings:


    (
        booking_id,
        booked_by,
        purpose,
        booking_start_date,
        expected_return_date,
        samples

    ) = booking


    with st.expander(
        f"{purpose} - {booked_by}"
    ):

        st.write(
            f"Samples: {samples}"
        )


        st.write(
            f"Start date: {booking_start_date}"
        )


        st.write(
            f"Return date: {expected_return_date}"
        )


        if st.button(
            "Return Booking",
            key=str(booking_id)
        ):

            return_booking(
                booking_id
            )

            st.success(
                "Returned successfully"
            )

            st.rerun()