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
    AddToCartSerializer,
    OrderShippingSerializer,
)


@extend_schema(
    tags=["Order Cart - Add to Cart"],
)
class OrderShippingAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = AddToCartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="List Cart",
        description="Retrieve a list of gold purchases for the authenticated user.",
        responses={200: AddToCartSerializer},
    )
    def list(self, request):
        queryset = order_cart_detail.objects.filter(user_id=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = AddToCartSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

        # return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="getPrice",
        description="Get Shipping Price",
        request=OrderShippingSerializer,
        responses={200: OrderShippingSerializer},
    )
    def get_price(self, request):
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

    @extend_schema(
        summary="Create Cart",
        description="Create a gold purchase for the authenticated user.",
        request=AddToCartSerializer,
        responses={201: AddToCartSerializer},
    )
    def perform_create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
