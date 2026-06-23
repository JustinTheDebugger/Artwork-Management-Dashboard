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
                "content-type": "image/png",
                "upsert": "true"
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

# INSERT SAMPLE PHOTOS
def upload_sample_photo(
    sample_id,
    uploaded_file
):
    storage_path = (
        f"photos/{sample_id}/"
        f"{uploaded_file.name}"
    )

    supabase.storage.from_(
        "sample-assets"
    ).upload(
        path=storage_path,
        file=uploaded_file.getvalue(),
        file_options={
            "content-type":
            uploaded_file.type,
            "upsert": "true"
        }
    )

    return (
        supabase.storage
        .from_("sample-assets")
        .get_public_url(storage_path)
    )