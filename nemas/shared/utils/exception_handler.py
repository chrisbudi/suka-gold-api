# In your project, e.g., utils.py
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is None:
        # Handle non-DRF exceptions here
        import traceback

        response = Response(
            {
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc(),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
