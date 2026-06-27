import streamlit as st
import pandas as pd


from services.artwork_release_service import (
    get_approved_artworks,
    release_artwork
)


st.set_page_config(
    page_title="Artwork Release",
    layout="wide"
)


st.title(
    "🚀 Artwork Release"
)

if "release_message" not in st.session_state:
    st.session_state.release_message = None


if st.session_state.release_message:

    st.success(
        st.session_state.release_message
    )

    st.session_state.release_message = None

# Load approved queue
artworks = get_approved_artworks()


if not artworks:

    st.success(
        "🎉 No approved artwork waiting for release."
    )

    st.stop()


artwork_df = pd.DataFrame(
    artworks,
    columns=[
        "ID",
        "Product",
        "Product Code",
        "Artwork Group",
        "Filename",
        "Status",
        "Uploaded"
    ]
)


st.info(
    f"Approved Artwork Waiting Release: {len(artwork_df)}"
)


st.dataframe(
    artwork_df[
        [
            "Product",
            "Artwork Group",
            "Filename",
            "Uploaded"
        ]
    ],
    hide_index=True,
    width="stretch"
)

# Select artwork
selected_file = st.selectbox(
    "Select Artwork",
    artwork_df["Filename"]
)


artwork = artwork_df[
    artwork_df["Filename"] == selected_file
].iloc[0]

# RElease section
st.divider()

st.subheader(
    "Release Confirmation"
)


col1, col2 = st.columns(2)


with col1:

    st.write(
        "**Product**"
    )

    st.write(
        artwork["Product"]
    )


    st.write(
        "**Artwork Group**"
    )

    st.write(
        artwork["Artwork Group"]
    )


with col2:

    st.write(
        "**Filename**"
    )

    st.write(
        artwork["Filename"]
    )


released_by = st.text_input(
    "Released By"
)

# Release button
if st.button(
    "🚀 Release Artwork",
    width="stretch"
):

    if not released_by.strip():

        st.error(
            "Released By is required."
        )

    else:

        release_artwork(
            artwork["ID"],
            released_by
        )


        st.session_state.release_message = (
            "🚀 Artwork released successfully."
        )

        st.rerun()