import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)



def upload_file(
    bucket,
    file_path,
    storage_path
):

    with open(
        file_path,
        "rb"
    ) as f:

        response = supabase.storage.from_(
            bucket
        ).upload(
            path=storage_path,
            file=f,
            file_options={
                "content-type": "image/png"
            }
        )


    public_url = (
        supabase.storage
        .from_(bucket)
        .get_public_url(
            storage_path
        )
    )


    return public_url


def upload_sample_qr(
    sample_id,
    qr_path
):

    storage_path = (
        f"qr/{sample_id}.png"
    )


    return upload_file(
        "sample-assets",
        qr_path,
        storage_path
    )