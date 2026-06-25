# import streamlit as st
# import pandas as pd

# from services.artwork_review_service import (
#     get_artwork_review_queue
# )

# from db import (
#     get_upload_batches,
#     get_upload_files
# )


# st.set_page_config(
#     page_title="Artwork Review",
#     layout="wide"
# )


# st.title("📝 Artwork Review")


# # -----------------------------
# # Upload Batch List
# # -----------------------------

# batches = get_upload_batches()


# if not batches:
#     st.info("No upload batches found.")
#     st.stop()

# batch_df = pd.DataFrame(
#     batches,
#     columns=[
#         "Upload ID",
#         "Files",
#         "Products",
#         "Uploaded",
#         "Status"
#     ]
# )


# st.subheader("Upload Batches")


# st.dataframe(
#     batch_df,
#     width="stretch",
#     hide_index=True
# )


# # -----------------------------
# # Select Batch
# # -----------------------------

# batch_options = {
#     f"{row['Upload ID']} - {row['Products']}": row["Upload ID"]
#     for _, row in batch_df.iterrows()
# }


# selected_batch_display = st.selectbox(
#     "Select Upload Batch",
#     batch_options.keys()
# )


# selected_batch = batch_options[
#     selected_batch_display
# ]


# # -----------------------------
# # Artwork Files
# # -----------------------------

# if selected_batch:

#     files = get_upload_files(
#         selected_batch
#     )


#     if not files:
#         st.warning(
#             "No artwork files found in this batch."
#         )
#         st.stop()


#     files_df = pd.DataFrame(
#         files,
#         columns=[
#             "ID",
#             "Product",
#             "Artwork Group",
#             "Filename",
#             "File Path",
#             "Storage URL",
#             "Status",
#             "Uploaded"
#         ]
#     )


#     st.subheader(
#         f"Artwork Files: {selected_batch}"
#     )


#     # Display cleaner table

#     display_df = files_df[
#         [
#             "Product",
#             "Artwork Group",
#             "Filename",
#             "Status",
#             "Uploaded"
#         ]
#     ]

#     st.dataframe(
#         display_df,
#         width="stretch",
#         hide_index=True
#     )


#     # -----------------------------
#     # Select Artwork
#     # -----------------------------

#     selected_file = st.selectbox(
#         "Select Artwork File",
#         files_df["Filename"]
#     )


#     artwork = files_df[
#         files_df["Filename"] == selected_file
#     ].iloc[0]


#     # -----------------------------
#     # Artwork Detail
#     # -----------------------------

#     st.divider()

#     st.subheader("Artwork Detail")


#     col1, col2 = st.columns(2)


#     with col1:

#         st.write(
#             "**Product**"
#         )
#         st.write(
#             artwork["Product"]
#         )


#         st.write(
#             "**Artwork Group**"
#         )
#         st.write(
#             artwork["Artwork Group"]
#         )

#         st.write("**Artwork File**")

#         if pd.notna(artwork["Storage URL"]) and artwork["Storage URL"]:

#             st.markdown(
#                 f"📄 [{artwork['Filename']}]({artwork['Storage URL']})"
#             )

#         else:

#             st.write(
#                 f"📄 {artwork['Filename']}"
#             )


#     with col2:

#         st.write(
#             "**Current Status**"
#         )
#         st.write(
#             artwork["Status"]
#         )


#         st.write(
#             "**Uploaded Date**"
#         )
#         st.write(
#             artwork["Uploaded"]
#         )


#         st.write(
#             "**File ID**"
#         )
#         st.write(
#             artwork["ID"]
#         )


#     # -----------------------------
#     # Review
#     # -----------------------------

#     st.divider()

#     st.subheader("Review")


#     reviewed_by = st.text_input(
#         "Reviewed By"
#     )

#     review_comments = st.text_area(
#         "Comments"
#     )


#     col1, col2 = st.columns(2)

#     with col1:

#         if st.button(
#             "✅ Approve",
#             width="stretch"
#         ):

#             if not reviewed_by.strip():
#                 st.error("Reviewer name is required.")

#             else:

#                 review_status = "Approved"

#                 st.write(
#                     {
#                         "artwork_id": artwork["ID"],
#                         "reviewed_by": reviewed_by,
#                         "review_status": review_status,
#                         "review_comments": review_comments
#                     }
#                 )

#                 st.success(
#                     "Artwork approved."
#                 )


#     with col2:

#         if st.button(
#             "🚫 Reject",
#             width="stretch"
#         ):

#             if not reviewed_by.strip():

#                 st.error(
#                     "Reviewer name is required."
#                 )

#             elif not review_comments.strip():

#                 st.error(
#                     "Comments are required when rejecting artwork."
#                 )

#             else:

#                 review_status = "Rejected"

#                 st.write(
#                     {
#                         "artwork_id": artwork["ID"],
#                         "reviewed_by": reviewed_by,
#                         "review_status": review_status,
#                         "review_comments": review_comments
#                     }
#                 )

#                 st.error(
#                     "Artwork rejected."
#                 )

import streamlit as st
import pandas as pd

from services.artwork_review_service import (
    get_artwork_review_queue
)


st.set_page_config(
    page_title="Artwork Review",
    layout="wide"
)


st.title("📝 Artwork Review")


# -----------------------------
# Review Queue
# -----------------------------

artworks = get_artwork_review_queue()


if not artworks:
    st.info("No artwork found.")
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


# -----------------------------
# Filter
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    status_filter = st.multiselect(
        "Status",
        [
            "Draft",
            "Approved",
            "Rejected",
            "Released"
        ],
        default=[
            "Draft"
        ]
    )


with col2:

    product_options = sorted(
        artwork_df["Product"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "Product",
        ["All Products"] + product_options
    )


filtered_df = artwork_df[
    artwork_df["Status"].isin(status_filter)
]


if selected_product != "All Products":

    filtered_df = filtered_df[
        filtered_df["Product"] == selected_product
    ]


st.subheader("Artwork Queue")


st.dataframe(
    filtered_df[
        [
            "Artwork Group",
            "File Path",
            "Status",
            "Uploaded"
        ]
    ],
    width="stretch",
    hide_index=True
)


if filtered_df.empty:
    st.info(
        "No artwork matches the selected status."
    )
    st.stop()



# -----------------------------
# Select Artwork
# -----------------------------

filtered_df["Display"] = (
    filtered_df["Product"]
    + " | "
    + filtered_df["Artwork Group"]
    + " | "
    + filtered_df["Filename"]
)

selected_display = st.selectbox(
    "Select Artwork File",
    filtered_df["Display"]
)

artwork = filtered_df[
    filtered_df["Display"] == selected_display
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

st.subheader("Review")


reviewed_by = st.text_input(
    "Reviewed By"
)


review_comments = st.text_area(
    "Comments"
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

            st.write(
                {
                    "artwork_id": artwork["ID"],
                    "reviewed_by": reviewed_by,
                    "review_status": review_status,
                    "review_comments": review_comments
                }
            )

            st.success(
                "Artwork approved."
            )


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

            st.write(
                {
                    "artwork_id": artwork["ID"],
                    "reviewed_by": reviewed_by,
                    "review_status": review_status,
                    "review_comments": review_comments
                }
            )

            st.error(
                "Artwork rejected."
            )