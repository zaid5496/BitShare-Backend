from pathlib import Path

from rest_framework.exceptions import ValidationError

from .constants import (
    MAX_FILE_SIZE,
    ALLOWED_EXTENSIONS,
)


def validate_uploaded_file(uploaded_file):

    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValidationError(
            f"File exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB limit."
        )

    extension = Path(
        uploaded_file.name
    ).suffix.lower().replace(".", "")

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f".{extension} files are not supported."
        )