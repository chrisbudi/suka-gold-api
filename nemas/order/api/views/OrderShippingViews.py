import json
from requests import Response
from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from shared_kernel.services.external.sapx_service import SapxService

# Correct model import
from order.models import order_cart_detail
from order.api.serializers import (
    OrderCartSerializer,
    # AddToCartSerializer,
    OrderShippingSerializer,
)


@extend_schema(
    tags=["Order Shipping - Get Shipping Service Price"],
)
class OrderShippingAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="getPrice",
        description="Get Shipping Price",
        request=OrderShippingSerializer,
        responses={200: OrderShippingSerializer},
    )
    def list_service_price(self, request):
        """get price from sapx"""
        try:
            serializer = OrderShippingSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return response.Response(
                    serializer.context.get("response"), status.HTTP_200_OK
                )
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")
