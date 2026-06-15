import streamlit as st

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠"
)

artwork_dashboard = st.Page(
    "pages/artwork_dashboard.py",
    title="Dashboard",
    icon="📊"
)

artwork_tracker = st.Page(
    "pages/artwork_tracker.py",
    title="Artwork Tracker",
    icon="📋"
)

sample_dashboard = st.Page(
    "pages/sample_dashboard.py",
    title="Dashboard",
    icon="📊"
)

sample_listing = st.Page(
    "pages/sample_listing.py",
    title="Sample Listing",
    icon="📋"
)

sample_intake = st.Page(
    "pages/sample_intake.py",
    title="Sample Intake",
    icon="📥"
)

bookings = st.Page(
    "pages/bookings.py",
    title="Bookings",
    icon="📅"
)

fulfilment = st.Page(
    "pages/fulfilment.py",
    title="Fulfilment",
    icon="🚚"
)

pg = st.navigation(
    {
        "": [home],
        "Artwork Management": [
            artwork_dashboard,
            artwork_tracker
        ],
        "Sample Management": [
            sample_dashboard,
            sample_listing,
            sample_intake,
            bookings,
            fulfilment
        ]
    }
)

pg.run()