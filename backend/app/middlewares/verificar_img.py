from fastapi import UploadFile, HTTPException


def is_image(file : UploadFile):
    if not file.content_type.startswith("image/"):
        return False

    return True