import streamlit as st

from services.sample_service import (
    get_samples,
    get_sample_types,
    get_bin_locations
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