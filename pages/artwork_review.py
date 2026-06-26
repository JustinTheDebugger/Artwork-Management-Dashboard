import streamlit as st
import pandas as pd

from services.artwork_review_service import (
    get_draft_artwork_queue,
    save_artwork_review,
    update_artwork_status
)


st.set_page_config(
    page_title="Artwork Review",
    layout="wide"
)

if "clear_review" not in st.session_state:
    st.session_state.clear_review = False


if st.session_state.clear_review:

    st.session_state.reviewed_by = ""
    st.session_state.review_comments = ""

    st.session_state.clear_review = False


if "review_complete" not in st.session_state:
    st.session_state.review_complete = False


if "review_message" not in st.session_state:
    st.session_state.review_message = None


st.title("📝 Artwork Review")

# -----------------------------
# Review Queue
# -----------------------------

artworks = get_draft_artwork_queue()


if not artworks:

    st.success(
        "🎉 No artwork pending review."
    )

    st.stop()


artwork_df = pd.DataFrame(
    artworks,
    columns=[
        "ID",
        "Product",
        "Artwork Group",
        "Filename",
        "File Path",
        "Status",
        "Upload ID",
        "Uploaded",
        "Storage URL"
    ]
)


st.info(
    f"Pending Reviews: {len(artwork_df)}"
)


# -----------------------------
# Select Product
# -----------------------------

product_list = sorted(
    artwork_df["Product"]
    .unique()
)


selected_product = st.selectbox(
    "Product",
    product_list,
    key="review_product"
)

product_df = artwork_df[
    artwork_df["Product"]
    == selected_product
]


# -----------------------------
# Select file
# -----------------------------

selected_filename = st.selectbox(
    "Artwork File",
    product_df["Filename"]
)

artwork = product_df[
    product_df["Filename"]
    == selected_filename
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


    st.write(
        "**Artwork File**"
    )


    if pd.notna(artwork["Storage URL"]) and artwork["Storage URL"]:

        st.markdown(
            f"📄 [{artwork['File Path']}]({artwork['Storage URL']})"
        )

    else:

        st.write(
            f"📄 {artwork['File Path']}"
        )

    st.code(
        artwork["File Path"]
    )


with col2:

    st.write(
        "**Current Status**"
    )

    st.write(
        artwork["Status"]
    )


    st.write(
        "**Upload ID**"
    )

    st.write(
        artwork["Upload ID"]
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
# Review
# -----------------------------

st.divider()

if st.session_state.review_message:

    st.success(
        st.session_state.review_message
    )

    st.session_state.review_message = None

st.subheader("Review")


reviewed_by = st.text_input(
    "Reviewed By",
    key="reviewed_by"
)


review_comments = st.text_area(
    "Comments",
    key="review_comments"
)


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "✅ Approve",
        width="stretch"
    ):

        if not reviewed_by.strip():

            st.error(
                "Reviewer name is required."
            )

        else:

            review_status = "Approved"

            save_artwork_review(
                artwork["ID"],
                reviewed_by,
                review_status,
                review_comments
            )

            update_artwork_status(
                artwork["ID"],
                review_status
            )

            st.session_state.clear_review = True

            st.session_state.review_message = (
                "✅ Artwork approved successfully."
            )

            st.rerun()


with col2:

    if st.button(
        "🚫 Reject",
        width="stretch"
    ):

        if not reviewed_by.strip():

            st.error(
                "Reviewer name is required."
            )

        elif not review_comments.strip():

            st.error(
                "Comments are required when rejecting artwork."
            )

        else:

            review_status = "Rejected"

            save_artwork_review(
                artwork["ID"],
                reviewed_by,
                review_status,
                review_comments
            )

            update_artwork_status(
                artwork["ID"],
                review_status
            )

            st.session_state.clear_review = True

            st.session_state.review_message = (
                "🚫 Artwork rejected successfully."
            )

            st.rerun()

            