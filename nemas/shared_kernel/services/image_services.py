import base64
import os


def image_to_base64(image_path):
    """
    Converts an image file to a Base64 string.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64-encoded string of the image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
