import streamlit as st
import pandas as pd

from services.artwork_history_service import (
    get_artwork_library,
    get_artwork_history
)

st.set_page_config(
    page_title="Artwork Library",
    layout="wide"
)

st.title("📜 Artwork Library")

if "selected_history" not in st.session_state:
    st.session_state.selected_history = None

library = get_artwork_library()

df = pd.DataFrame(
    library,
    columns=[
        "ID",
        "Product",
        "Product Code",
        "Artwork Group",
        "Filename",
        "Storage URL",
        "Status",
        "Uploaded",
        "Review Status",
        "Reviewed By",
        "Review Comments",
        "Reviewed At",
        "Released By",
        "Released At"
    ]
)


# Product filter
selected_product = st.selectbox(
    "Product",
    ["All"] + sorted(df["Product"].dropna().unique())
)

if selected_product != "All":

    df = df[
        df["Product"] == selected_product
    ]

# Display main table
display = df[
    [
        "Artwork Group",
        "Status",
        "Filename",
        "Uploaded"
    ]
].copy()

# -----------------------------
# Main Layout
# -----------------------------

main_col, history_col = st.columns(
    [3,1]
)


with main_col:


    st.subheader(
        "Artwork Files"
    )

    st.divider()


    for index, row in df.iterrows():


        col1, col2, col3, col4 = st.columns(
            [2,2,4,1]
        )


        with col1:
            st.write(
                row["Artwork Group"]
            )


        with col2:

            status_icon = {
                "Released":"🟢",
                "Approved":"🟡",
                "Rejected":"🔴",
                "Draft":"⚪",
                "Superseded":"⚫"
            }.get(
                row["Status"],
                ""
            )

            st.write(
                f"{status_icon} {row['Status']}"
            )


        with col3:

            if row["Storage URL"]:

                st.markdown(
                    f"[📄 {row['Filename']}]({row['Storage URL']})"
                )

            else:

                st.write(
                    row["Filename"]
                )


        with col4:

            if st.button(
                "View",
                key=f"history_{row['ID']}"
            ):

                st.session_state.selected_history = {

                    "product_code":
                        row["Product Code"],

                    "product":
                        row["Product"],

                    "group":
                        row["Artwork Group"]

                }

                st.rerun()

        st.divider()

# -----------------------------
# History Panel
# -----------------------------
with history_col:


    st.subheader(
        "📜 History"
    )


    if st.session_state.selected_history:


        selected = st.session_state.selected_history


        st.write(
            f"**{selected['product']}**"
        )


        st.write(
            selected["group"]
        )


        st.divider()


        history = get_artwork_history(

            selected["product_code"],

            selected["group"]

        )


        for item in history:


            (
                artwork_id,
                filename,
                status,
                uploaded_at,
                review_status,
                reviewed_by,
                comments,
                reviewed_at,
                released_by,
                released_at,
                storage_url

            ) = item


            icon = {

                "Released":"🟢",

                "Approved":"🟡",

                "Rejected":"🔴",

                "Draft":"⚪",

                "Superseded":"⚫"

            }.get(
                status,
                ""
            )


            st.write(
                f"{icon} **{status}**"
            )


            if storage_url:

                st.markdown(
                    f"[📄 {filename}]({storage_url})"
                )

            else:

                st.write(
                    filename
                )


            st.caption(
                f"Uploaded: {uploaded_at}"
            )


            if reviewed_by:

                st.write(
                    f"Reviewed by: {reviewed_by}"
                )


            if comments:

                st.write(
                    f"Comment: {comments}"
                )


            if released_by:

                st.write(
                    f"Released by: {released_by}"
                )


            st.divider()


    else:

        st.info(
            "Select an artwork to view history."
        )
