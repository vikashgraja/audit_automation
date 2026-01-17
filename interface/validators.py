"""
File Upload Validator for Django
Validates file uploads for security
"""

import os

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """
    Validate that uploaded file has an allowed extension
    """
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = getattr(
        settings, "ALLOWED_UPLOAD_EXTENSIONS", [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv"]
    )

    if ext not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(allowed_extensions)}")


def validate_file_size(value):
    """
    Validate that uploaded file is not too large
    """
    max_size = getattr(settings, "FILE_UPLOAD_MAX_MEMORY_SIZE", 5242880)  # 5MB default

    if value.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(f"File size exceeds maximum allowed size of {max_size_mb}MB")


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal and other attacks
    """
    # Remove any path components
    filename = os.path.basename(filename)

    # Remove any potentially dangerous characters
    dangerous_chars = ["..", "/", "\\", "<", ">", ":", '"', "|", "?", "*"]
    for char in dangerous_chars:
        filename = filename.replace(char, "_")

    return filename
