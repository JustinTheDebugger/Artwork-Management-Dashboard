import streamlit as st

pg = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard"),
    st.Page("pages/artwork_tracker.py", title="Artwork Tracker"),
])

pg.run()