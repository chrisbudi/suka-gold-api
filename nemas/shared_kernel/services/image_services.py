import base64
import os
import tempfile


def image_to_base64(file):
    """
    Converts an image file to a Base64 string.

    Returns:
        str: Base64-encoded string of the image.
    """

    return base64.b64encode(file.read()).decode("utf-8")


def upload_file_to_temp(file, user_id):
    """
    Uploads a file to the temporary directory.

    Returns:
        str: Path to the uploaded file.
    """

    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, user_id + os.path.splitext(file.name)[1])
    print(temp_file_path, "temp_file_path")
    with open(temp_file_path, "wb") as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)

    return temp_file_path


def get_file_from_temp(file_id):
    """
    Retrieves a file from the temporary directory.

    Returns:
        file: File object.
    """

    with open(file_id, "rb") as temp_file:
        return temp_file
