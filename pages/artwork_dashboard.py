import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_all_artworks

from services.dashboard_service import (
    get_artwork_kpis
)

from services.notification_service import (
    get_notifications
)

st.set_page_config(
    page_title="NexaFlow360 Dashboard",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<h1 style="margin-bottom:0;">
    NexaFlow360 
    <span style="font-size:20px; font-weight:400; color:#666;">
        — Complete Product Lifecycle Visibility
    </span>
</h1>
""", unsafe_allow_html=True)

kpis = get_artwork_kpis()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Draft",
        kpis["Draft"]
    )


with col2:
    st.metric(
        "Approved",
        kpis["Approved"]
    )


with col3:
    st.metric(
        "Released",
        kpis["Released"]
    )


with col4:
    st.metric(
        "Rejected",
        kpis["Rejected"]
    )

st.divider()

st.subheader("🔔 Action Center")


notifications = get_notifications()


if not notifications:

    st.success(
        "Everything is up to date."
    )


else:

    for item in notifications:

        if item["type"] == "warning":

            st.warning(
                f'{item["title"]}: {item["count"]}'
            )


        elif item["type"] == "success":

            st.success(
                f'{item["title"]}: {item["count"]}'
            )


        elif item["type"] == "error":

            st.error(
                f'{item["title"]}: {item["count"]}'
            )