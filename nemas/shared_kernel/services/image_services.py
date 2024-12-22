import base64
import os
import tempfile
import uuid


def image_to_base64(file, user_id: uuid.UUID):
    """
    Converts an image file to a Base64 string.

    Returns:
        str: Base64-encoded string of the image.
    """
    # upload to file temp using upload file to temp function
    # then get the file from temp using get file from temp function
    # then convert the file to base64 using this function

    upload_file_to_temp(file, user_id)
    file = get_file_from_temp(user_id)
    return base64.b64encode(file.read()).decode("utf-8")


def upload_file_to_temp(file, user_id: uuid.UUID):
    """
    Uploads a file to the temporary directory.

    Returns:
        str: Path to the uploaded file.
    """

    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(
        temp_dir, str(user_id) + os.path.splitext(file.name)[1]
    )
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

    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, str(file_id) + ".jpg")
    return open(str(temp_file_path), "rb")


def delete_file_from_temp(file):
    """
    Deletes a file from the temporary directory.
    """

    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, str(file) + ".jpg")
    os.remove((temp_file_path))
