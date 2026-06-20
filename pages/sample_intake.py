import streamlit as st

from services.product_service import (
    get_seasons,
    get_categories,
    generate_product_code,
    create_product,
    get_products
)

from services.sample_service import (
    get_sample_types,
    get_bin_locations,
    generate_sample_ids,
    generate_sample_name,
    create_samples
)

created_by = 'Justin'

if "sample_created" in st.session_state:

    result = st.session_state.sample_created

    st.success(
        f"✅ {result['count']} samples created successfully"
    )

    st.write("Created Sample IDs:")

    for sample_id in result["samples"]:
        st.write(
            f"- {sample_id}"
        )

    if st.button(
        "Create Another Sample"
    ):
        del st.session_state.sample_created
        st.rerun()

    st.stop()

st.title(
    "📦 Sample Intake"
)

@st.dialog("New Product")
def show_product_modal():
    seasons = get_seasons()

    season = st.selectbox(
        "Season",
        seasons["season_name"]
    )

    categories = get_categories()

    category = st.selectbox(
        "Category",
        categories["category_name"]
    )

    product_name = st.text_input(
        "Product Name"
    )

    preview = generate_product_code(
        season,
        category
    )

    st.info(
        f"Product Code Preview: "
        f"{preview['product_code']}"
    )

    if st.button(
        "Save Product",
        type="primary"
    ):
        if not product_name:
            st.error(
                "Product Name required"
            )
            st.stop()

        product_code = create_product(
            season,
            category,
            product_name,
            "001",      # default variant for now
            created_by
        )

        st.session_state.new_product = {
            "product_code": product_code,
            "product_name": product_name
        }

        st.rerun()

products = get_products()

product_options = {
    f"{row.product_code} - {row.product_name}": row
    for _, row in products.iterrows()
}

# Auto-select newly created product
default_index = 0

if "new_product" in st.session_state:

    target = (
        f"{st.session_state.new_product['product_code']} - "
        f"{st.session_state.new_product['product_name']}"
    )

    keys = list(product_options.keys())

    if target in keys:
        default_index = keys.index(target)

# ==================================================
# FORM MODE
# ==================================================

if "sample_preview" not in st.session_state:

    selected = st.selectbox(
        "Product *",
        product_options.keys(),
        index=default_index
    )

    selected_product = product_options[selected]

    product_code = selected_product.product_code
    product_name = selected_product.product_name

    if st.button("➕ New Product"):
        show_product_modal()

    sample_types = get_sample_types()

    sample_type_options = {
        row.sample_type_name: row.sample_type_code
        for _, row in sample_types.iterrows()
    }

    selected_sample_type = st.selectbox(
        "Sample Type *",
        sample_type_options.keys()
    )

    sample_type_code = sample_type_options[
        selected_sample_type
    ]

    quantity = st.number_input(
        "Quantity *",
        min_value=1,
        value=1
    )

    received_date = st.date_input(
        "Received Date *"
    )

    bins = get_bin_locations()

    bin_options = {
        f"{row.bin_code} - {row.bin_name}": {
            "code": row.bin_code,
            "name": row.bin_name
        }
        for _, row in bins.iterrows()
    }

    selected_bin = st.selectbox(
        "Bin Location *",
        bin_options.keys()
    )

    bin_location = bin_options[selected_bin]

    st.button("➕ Add Bin")

    remarks = st.text_area(
        "Remarks"
    )

    photos = st.file_uploader(
        "Photos",
        accept_multiple_files=True
    )

    if st.button(
        "Preview",
        type="primary"
    ):

        sample_ids = generate_sample_ids(
            product_code,
            sample_type_code,
            quantity
        )

        sample_name = generate_sample_name(
            product_name,
            sample_type_code,
            received_date
        )

        st.session_state.sample_preview = {
            "product_code": product_code,
            "product_name": product_name,
            "sample_type": sample_type_code,
            "quantity": quantity,
            "received_date": received_date,
            "bin_location": bin_location["code"],
            "bin_name": bin_location["name"],
            "remarks": remarks,
            "sample_name": sample_name,
            "sample_ids": sample_ids
        }

        st.rerun()

# ==================================================
# PREVIEW MODE
# ==================================================

else:

    preview = st.session_state.sample_preview

    st.subheader("Preview")

    st.info(
        f"""
        Sample Name:
        {preview['sample_name']}

        Quantity:
        {preview['quantity']}

        Bin:
        {preview['bin_location']} - {preview['bin_name']}
        """
    )

    st.write("### Sample IDs")

    for sample_id in preview["sample_ids"]:
        st.write(sample_id)

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅ Back"):

            del st.session_state.sample_preview
            st.rerun()

    with col2:

        if st.button(
            "✅ Create Samples",
            type="primary"
        ):

            try:

                samples = create_samples(
                    preview["product_code"],
                    preview["product_name"],
                    preview["sample_type"],
                    preview["quantity"],
                    preview["received_date"],
                    preview["bin_location"],
                    preview["remarks"],
                    created_by
                )

                st.session_state.sample_created = {
                    "count": len(samples),
                    "samples": samples
                }

                del st.session_state.sample_preview

                st.rerun()


            except Exception as e:

                st.error(
                    "Unable to create samples. Please try again."
                )

                st.exception(e)   # remove when deploying