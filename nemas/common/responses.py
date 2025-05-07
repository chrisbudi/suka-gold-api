from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Any, Optional, TypedDict, Generic, TypeVar, Literal, Union


class NemasReponses:
    @staticmethod
    def success(
        data: Optional[Dict[str, Any]] = None, message: str = "Success"
    ) -> Dict[str, Any]:
        """
        Standard format for a successful response.
        """
        return {
            "success": True,
            "status": "success",
            "message": message,
            "data": data or {},
        }

    @staticmethod
    def failure(
        message: str = "An error occurred", errors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Standard format for a failed response.
        """
        return {
            "success": False,
            "status": "failed",
            "message": message,
            "errors": errors or {},
        }


# jk    @staticmethod
#     def failure(errors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
#         """
#         Standard format for a failed response.
#         """
#         return {
#             "errors": errors or {},
#         }


T = TypeVar("T")


class SuccessResponse(Generic[T], TypedDict):
    success: Literal[True]
    data: T


class ErrorResponse(TypedDict):
    success: Literal[False]
    data: Any


ServicesResponse = Union[SuccessResponse[T], ErrorResponse]
