import streamlit as st

st.set_page_config(
    page_title="PLM V1",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Product Lifecycle Management System")

st.markdown(
    """
    Centralized platform for managing:

    - Artwork Management
    - Sample Management
    """
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎨 Artwork Management")

    st.info(
        """
        Track artwork coverage,
        manage artwork files,
        monitor missing artwork.
        """
    )

with col2:
    st.subheader("📦 Sample Management")

    st.info(
        """
        Manage sample inventory,
        bookings,
        fulfilment,
        and movement tracking.
        """
    )