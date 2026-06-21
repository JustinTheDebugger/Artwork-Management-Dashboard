import streamlit as st

from services.sample_service import (
    get_samples,
    get_sample_types,
    get_bin_locations,
    get_sample_detail,
    get_sample_movements,
    get_sample_photos,
    update_sample
)

st.title(
    "📋 Sample Listing"
)


# =========================
# Filters
# =========================

col1, col2, col3 = st.columns(3)


with col1:

    search = st.text_input(
        "🔍 Search Sample"
    )


with col2:

    sample_types = get_sample_types()

    sample_type_options = {
        "All": None
    }

    sample_type_options.update(
        {
            row.sample_type_name: row.sample_type_code
            for _, row in sample_types.iterrows()
        }
    )


    selected_type = st.selectbox(
        "Sample Type",
        sample_type_options.keys()
    )

    sample_type = sample_type_options[
        selected_type
    ]


with col3:

    status_options = {
        "All": None,
        "AVAILABLE": "AVAILABLE",
        "RESERVED": "RESERVED",
        "MISSING": "MISSING",
        "RETIRED": "RETIRED"
    }


    selected_status = st.selectbox(
        "Status",
        status_options.keys()
    )

    status = status_options[
        selected_status
    ]


# =========================
# Bin Filter
# =========================

bins = get_bin_locations()


bin_options = {
    "All": None
}


bin_options.update(
    {
        f"{row.bin_code} - {row.bin_name}":
        row.bin_code

        for _, row in bins.iterrows()
    }
)


selected_bin = st.selectbox(
    "Bin Location",
    bin_options.keys()
)


bin_code = bin_options[
    selected_bin
]

@st.dialog("Edit Sample")
def edit_sample_dialog():

    bins = get_bin_locations()

    bin_codes = bins["bin_code"].tolist()

    current_index = 0

    if detail.bin_location in bin_codes:
        current_index = bin_codes.index(
            detail.bin_location
        )

    new_bin = st.selectbox(
        "Bin Location",
        bin_codes,
        index=current_index
    )

    status_options = [
        "AVAILABLE",
        "RESERVED",
        "MISSING",
        "RETIRED"
    ]

    status_index = 0

    if detail.sample_status in status_options:
        status_index = status_options.index(
            detail.sample_status
        )

    new_status = st.selectbox(
        "Status",
        status_options,
        index=status_index
    )

    current_holder = st.text_input(
        "Current Holder",
        value=detail.current_holder or ""
    )

    remarks = st.text_area(
        "Remarks",
        value=detail.remarks or ""
    )

    if st.button(
        "Save Changes",
        type="primary"
    ):

        update_sample(
            sample_id=detail.sample_id,
            bin_location=new_bin,
            sample_status=new_status,
            current_holder=current_holder,
            remarks=remarks,
            updated_by="Justin"
        )

        st.session_state.success_message = (
            "Sample updated successfully"
        )

        st.rerun()


# =========================
# Query
# =========================

samples = get_samples(
    search=search,
    sample_type=sample_type,
    status=status,
    bin_code=bin_code
)


st.write(
    f"Total Samples: {len(samples)}"
)


# =========================
# Display Columns
# =========================

display_columns = [
    "sample_id",
    "sample_name",
    "sample_type_name",
    "sample_status",
    "bin_location",
    "bin_name",
    "created_at"
]


st.dataframe(
    samples[display_columns],
    width='stretch'
)

if not samples.empty:

    selected_sample = st.selectbox(
        "Select Sample",
        samples["sample_id"]
    )

    detail = get_sample_detail(
        selected_sample
    )

    st.divider()

    st.subheader(
        "Sample Details"
    )

    col1, col2 = st.columns(
        [2,1]
    )

    # LEFT SIDE
    with col1:

        st.write(
            "Sample ID:",
            detail.sample_id
        )

        st.write(
            "Sample Name:",
            detail.sample_name
        )

        st.write(
            "Type:",
            detail.sample_type_name
        )

        st.write(
            "Status:",
            detail.sample_status
        )

        st.write(
            "Bin:",
            f"{detail.bin_location} - {detail.bin_name}"
        )

        st.write(
            "Created By:",
            detail.created_by
        )

        st.write(
            "Created At:",
            detail.created_at
        )

    # RIGHT SIDE - QR CODE
    with col2:

        if detail.qr_code_url:

            st.image(
                detail.qr_code_url,
                caption="QR Code"
            )

    # PHOTOS SECTION
    photos = get_sample_photos(
        selected_sample
    )

    if not photos.empty:

        st.subheader(
            "Photos"
        )

        cols = st.columns(3)

        for idx, photo in enumerate(
            photos["file_url"]
        ):

            cols[idx % 3].image(
                photo,
                use_container_width=True
            )

    # MOVEMENT HISTORY
    st.divider()

    st.subheader(
        "Movement History"
    )

    movements = get_sample_movements(
        selected_sample
    )

    st.dataframe(
        movements,
        width='stretch'
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "✏ Edit Sample"
        ):
            edit_sample_dialog()

    with col2:

        st.button(
            "📦 Book Sample"
        )

    with col3:

        st.button(
            "🗑 Retire Sample"
        )