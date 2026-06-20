import streamlit as st

from services.storage_service import supabase


st.title(
    "Supabase Storage Test"
)


try:

    buckets = supabase.storage.list_buckets()

    st.success(
        "Connected to Supabase"
    )


    st.write(
        "Buckets:"
    )


    for bucket in buckets:

        st.write(
            bucket.name
        )


except Exception as e:

    st.error(
        "Supabase connection failed"
    )

    st.exception(e)