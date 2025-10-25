import os
import uuid
from pathlib import Path
from fastapi import UploadFile


UPLOAD_DIR = Path("uploads/products")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def generate_unique_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()
    unique_id = uuid.uuid4().hex
    return f"{unique_id}{extension}"


def validate_image_file(file: UploadFile) -> None:
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")


async def save_upload_file(file: UploadFile) -> str:
    validate_image_file(file)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_DIR / filename

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File size exceeds 5MB limit")

    with open(file_path, "wb") as f:
        f.write(content)

    return filename

