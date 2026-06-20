import os
from datetime import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont



def generate_qr_code(
    sample_id
):

    folder = "temp_qr"

    os.makedirs(
        folder,
        exist_ok=True
    )

    filename = (
        f"{sample_id}.png"
    )

    path = os.path.join(
        folder,
        filename
    )

    qr_data = (
        f"SAMPLE:{sample_id}"
    )

    img = qrcode.make(
        qr_data
    )

    img.save(path)

    return path

def generate_sample_qr(
    sample_id,
    sample_name,
    logo_path=None
):
    folder = "temp_qr"
    os.makedirs(folder, exist_ok=True)

    # Data encoded in QR
    qr_data = f"{sample_id}|{sample_name}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    # Create canvas
    img = Image.new("RGB", (400, 500), "white")

    # Resize QR and paste
    qr_img = qr_img.resize((250, 250))
    img.paste(qr_img, (75, 20))

    draw = ImageDraw.Draw(img)

    draw.text((50, 300), f"ID: {sample_id}", fill="black")
    draw.text((50, 340), f"Name: {sample_name}", fill="black")

    filename = f"{sample_id}.png"
    qr_path = os.path.join(folder, filename)

    img.save(qr_path)

    return qr_path