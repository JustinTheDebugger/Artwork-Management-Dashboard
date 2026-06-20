import streamlit as st
from datetime import date

from services.sample_service import (
    create_samples
)

from services.product_service import (
    product_exists
)


st.title(
    "Create Samples Test"
)

product_code = st.text_input(
    "Product Code",
    "0266661-001"
)

product_name = st.text_input(
    "Product Name",
    "Shapeshifter 4"
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
    value=2
)

bin_location = st.text_input(
    "Bin",
    "A01"
)

remarks = st.text_area(
    "Remarks"
)

received_date = st.date_input(
    "Received Date",
    value=date.today()
)

if st.button(
    "Create Samples",
    type="primary"
):
    try:
        if not product_exists(product_code):

            raise ValueError(
                f"Product {product_code} not found"
            )

        samples = create_samples(
            product_code,
            product_name,
            sample_type,
            quantity,
            received_date,
            bin_location,
            remarks,
            "Justin"
        )

        st.success(
            f"{len(samples)} samples created"
        )

        st.write(samples)

    except ValueError as e:

        st.error(str(e))

    except Exception as e:

        st.error(
            "Unable to create samples. Please contact administrator."
        )

        st.exception(e)  # Remove later in production

    