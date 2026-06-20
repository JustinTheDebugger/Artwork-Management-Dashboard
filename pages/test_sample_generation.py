import streamlit as st
from datetime import date

from services.sample_service import (
    generate_sample_ids,
    generate_sample_name
)

from services.qr_service import (
    generate_qr_code
)


st.set_page_config(
    page_title="Test Sample Service",
    layout="wide"
)


st.title("🧪 Test Sample Service")


product_code = st.text_input(
    "Product Code",
    value="0266661-001"
)


product_name = st.text_input(
    "Product Name",
    value="Shapeshifter 4"
)


sample_type = st.selectbox(
    "Sample Type",
    [
        "MAS",
        "SMS",
        "DEV",
        "PP"
    ]
)


quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=3
)


received_date = st.date_input(
    "Received Date",
    value=date.today()
)


if st.button("Generate Preview"):

    sample_ids = generate_sample_ids(
        product_code,
        sample_type,
        quantity
    )


    sample_name = generate_sample_name(
        product_name,
        sample_type,
        received_date
    )

    

    


    st.subheader("Generated Sample Name")

    st.success(sample_name)


    st.subheader("Generated Sample IDs")

    for sid in sample_ids:
        st.write(
            sid
        )