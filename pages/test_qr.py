import streamlit as st
import os

from services.qr_service import (
    generate_sample_qr
)


st.title("QR Code Generator")


sample_id = st.text_input(
    "Sample ID",
    value="0266661-001S-MS-01"
)


sample_name = st.text_input(
    "Sample Name",
    value="Shapeshifter 4 Master Sample 2026-06"
)


if st.button("Generate QR"):

    path = generate_sample_qr(
        sample_id,
        sample_name
    )

    st.success(
        "QR Generated"
    )

    st.write(
        "Saved to:",
        path
    )

    st.write(
        "Exists:",
        os.path.exists(path)
    )

    if os.path.exists(path):
        st.image(
            path,
            caption=sample_id
        )