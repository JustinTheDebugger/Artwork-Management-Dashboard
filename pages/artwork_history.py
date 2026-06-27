import streamlit as st
import pandas as pd

from services.artwork_history_service import (
    get_artwork_history
)

st.set_page_config(
    page_title="Artwork History",
    layout="wide"
)

st.title("📜 Artwork History")

history = get_artwork_history()

if not history:
    st.info("No released artwork yet.")
    st.stop()

df = pd.DataFrame(
    history,
    columns=[
        "ID",
        "Product",
        "Product Code",
        "Artwork Group",
        "Filename",
        "Storage URL",
        "Status",
        "Artwork Date",
        "Released By",
        "Released At"
    ]
)

# Product filter
selected_product = st.selectbox(
    "Product",
    sorted(df["Product"].unique())
)

filtered = df[
    df["Product"] == selected_product
]

# Artwork group filter
selected_group = st.selectbox(
    "Artwork Group",
    sorted(filtered["Artwork Group"].unique())
)

filtered = filtered[
    filtered["Artwork Group"] == selected_group
]

# Timeline
for _, row in filtered.iterrows():

    if row["Status"] == "Released":
        icon = "🟢"
    else:
        icon = "⚪"

    with st.container(border=True):

        st.subheader(
            f"{icon} {row['Status']}"
        )

        st.write(
            f"**Released By:** {row['Released By']}"
        )

        st.write(
            f"**Released At:** {row['Released At']}"
        )

        if pd.notna(row["Storage URL"]) and row["Storage URL"]:

            st.markdown(
                f"📄 [{row['Filename']}]({row['Storage URL']})"
            )

        else:

            st.write(
                f"📄 {row['Filename']}"
            )