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
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="getPrice",
        description="Get Shipping Serivce",
        request=OrderShippingSerializer,
        responses={200: OrderShippingSerializer},
    )
    def list_shipping_service(self, request):
        """get price from sapx"""
        try:
            serializer = OrderShippingSerializer(data=request.data)

            if serializer.is_valid():
                sapx_service = SapxService()
                payload = {
                    "origin": "JK07",
                    "destination": "JI28",
                    "weight": serializer.data.get("weight"),
                    "customer_code": "DEV000",
                    "packing_type_code": "ACH06",
                    "volumetric": "1x1x1",
                    "insurance_type_code": "INS02",
                    "item_value": serializer.data.get("amount"),
                }
                payload_data = json.dumps(payload)
                data = sapx_service.get_price(payload_data)
                # serializer.save()
                return response.Response(data, status.HTTP_200_OK)
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")
