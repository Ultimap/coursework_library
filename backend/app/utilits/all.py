from fastapi import UploadFile
import os
from app.settings import upload_img


async def add_img(img: UploadFile):
    os.makedirs(upload_img, exist_ok=True)
    img_path = os.path.join(upload_img, img.filename)
    with open(img_path, 'wb') as file:
        content = await img.read()
        file.write(content)