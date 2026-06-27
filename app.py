import streamlit as st

test_supabase = st.Page(
    "pages/test_supabase.py",
    title="Test Supabase Connection",
    icon="🧪"
)

test_create_samples = st.Page(
    "pages/test_create_samples.py",
    title="Test Create Samples",
    icon="🧪"
)

test_sample_service = st.Page(
    "pages/test_sample_generation.py",
    title="Test Sample Service",
    icon="🧪"
)

test_qr_service = st.Page(
    "pages/test_qr.py",
    title="Test QR Service",
    icon="🧪"
)

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠"
)

product_dashboard = st.Page(
    "pages/product_dashboard.py",
    title="Dashboard",
    icon="📊"
)

artwork_dashboard = st.Page(
    "pages/artwork_dashboard.py",
    title="Dashboard",
    icon="📊"
) 

artwork_review = st.Page(
    "pages/artwork_review.py",
    title="Artwork Review",
    icon="📥"
)

artwork_release = st.Page(
    "pages/artwork_release.py",
    title="Artwork Release",
    icon="📥"
) 

artwork_tracker = st.Page(
    "pages/artwork_tracker.py",
    title="Artwork Tracker",
    icon="📋"
)

artwork_library = st.Page(
    "pages/artwork_library.py",
    title="Artwork Timeline",
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
    "pages/booking.py",
    title="Booking",
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
        "Product Management": [
            product_dashboard
        ],
        "Artwork Management": [
            artwork_dashboard,
            artwork_tracker,
            artwork_review,
            artwork_release,
            artwork_library
        ],
        "Sample Management": [
            sample_dashboard,
            sample_listing,
            sample_intake,
            bookings,
            fulfilment
        ],
        "Tests": [
            test_sample_service,
            test_qr_service,
            test_create_samples,
            test_supabase
        ]
    }
)

pg.run()