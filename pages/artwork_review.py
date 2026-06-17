import streamlit as st
import pandas as pd

from db import (
    get_upload_batches,
    get_upload_files
)


st.set_page_config(
    page_title="Artwork Review",
    layout="wide"
)


st.title("📝 Artwork Review")


# -----------------------------
# Upload Batch List
# -----------------------------

batches = get_upload_batches()


if not batches:
    st.info("No upload batches found.")
    st.stop()

batch_df = pd.DataFrame(
    batches,
    columns=[
        "Upload ID",
        "Files",
        "Products",
        "Uploaded",
        "Status"
    ]
)


st.subheader("Upload Batches")


st.dataframe(
    batch_df,
    width="stretch",
    hide_index=True
)


# -----------------------------
# Select Batch
# -----------------------------

batch_options = {
    f"{row['Upload ID']} - {row['Products']}": row["Upload ID"]
    for _, row in batch_df.iterrows()
}


selected_batch_display = st.selectbox(
    "Select Upload Batch",
    batch_options.keys()
)


selected_batch = batch_options[
    selected_batch_display
]


# -----------------------------
# Artwork Files
# -----------------------------

if selected_batch:

    files = get_upload_files(
        selected_batch
    )


    if not files:
        st.warning(
            "No artwork files found in this batch."
        )
        st.stop()


    files_df = pd.DataFrame(
        files,
        columns=[
            "ID",
            "Product",
            "Artwork Group",
            "Filename",
            "File Path",
            "Storage URL",
            "Status",
            "Uploaded"
        ]
    )


    st.subheader(
        f"Artwork Files: {selected_batch}"
    )


    # Display cleaner table

    display_df = files_df[
        [
            "Product",
            "Artwork Group",
            "Filename",
            "Status",
            "Uploaded"
        ]
    ]

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


    # -----------------------------
    # Select Artwork
    # -----------------------------

    selected_file = st.selectbox(
        "Select Artwork File",
        files_df["Filename"]
    )


    artwork = files_df[
        files_df["Filename"] == selected_file
    ].iloc[0]


    # -----------------------------
    # Artwork Detail
    # -----------------------------

    st.divider()

    st.subheader("Artwork Detail")


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

        st.write("**Artwork File**")

        if pd.notna(artwork["Storage URL"]) and artwork["Storage URL"]:

            st.markdown(
                f"📄 [{artwork['Filename']}]({artwork['Storage URL']})"
            )

        else:

            st.write(
                f"📄 {artwork['Filename']}"
            )


    with col2:

        st.write(
            "**Current Status**"
        )
        st.write(
            artwork["Status"]
        )


        st.write(
            "**Uploaded Date**"
        )
        st.write(
            artwork["Uploaded"]
        )


        st.write(
            "**File ID**"
        )
        st.write(
            artwork["ID"]
        )


    # -----------------------------
    # Review Action
    # -----------------------------

    st.divider()

    st.subheader("Review Action")


    col1, col2, col3 = st.columns(3)


    with col1:
        if st.button(
            "✅ Approve",
            width="stretch"
        ):
            st.success(
                "Approved (database update coming next)"
            )


    with col2:
        if st.button(
            "⚠ Request Correction",
            width="stretch"
        ):
            st.warning(
                "Correction requested (database update coming next)"
            )


    with col3:
        if st.button(
            "🚫 Reject",
            width="stretch"
        ):
            st.error(
                "Rejected (database update coming next)"
            )