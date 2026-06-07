import os
from supabase import create_client
from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException

load_dotenv()

SUPRABASE_BUCKET = os.getenv("SUPRABASE_BUCKET")
SUPRABASE_KEY = os.getenv("SUPABASE_KEY")
SUPRABASE_URL = os.getenv("SUPABASE_URL")

print(SUPRABASE_KEY)

def suprabase_client():
    if not SUPRABASE_KEY or not SUPRABASE_URL:
        return None

    else:
        client = create_client(SUPRABASE_URL, SUPRABASE_KEY)
        return client

def save_img(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="not image")
    content = file.file.read()
    path = file.filename
    content_type = file.content_type
    print(content_type)
    supaclient = suprabase_client()
    response = supaclient.storage.from_(SUPRABASE_BUCKET).upload(
        path = path,
        file = content,
        file_options= {"content-type":file.content_type},
    )
    url = (supaclient.storage.from_(SUPRABASE_BUCKET).get_public_url(path))
    return url

def delete_img(url: str):
    supaclient = suprabase_client()
    path = url.split("/")[-1]
    supaclient.storage.from_(SUPRABASE_BUCKET).remove([path])