from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from order.models import order_cart_detail, order_cart
from order_fix.api.serializers import OrderCartSerializer
from order_fix.api.serializers.OrderCartSerializer import (
    AddCartDetailSerializer,
    CartDetailSerializer,
    CartSerializer,
    ProcessCartSerializer,
)


@extend_schema(
    tags=["Order Cart Fix - Add to Cart"],
)
class CartItemListAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartDetailSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination

    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    def get_queryset(self):
        return order_cart_detail.objects.filter(
            user_id=self.request.user, completed_cart=False
        ).select_related("gold")

    @extend_schema(
        summary="List Cart Detail",
        description="Retreive all detail data that completed_cart false.",
        request={200: CartDetailSerializer},
    )
    def list_cart_detail(self, request):
        queryset = order_cart_detail.objects.filter(
            user_id=request.user, completed_cart=False, selected=True
        ).select_related("gold")

        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        if paginated_queryset is not None:
            serializer = CartDetailSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CartDetailSerializer(filter_queryset, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Show Cart",
        description="Show data cart detail",
        request={200: OrderCartSerializer.CartSerializer},
    )
    def show_cart(self, request):
        queryset = order_cart.objects.filter(
            user_id=request.user, completed_cart=False
        ).first()

        serializer = OrderCartSerializer.CartSerializer(queryset)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Add To Cart",
        description="Add a gold to cart for the authenticated user.",
        request=AddCartDetailSerializer,
        responses={201: CartDetailSerializer, 400: "Bad Request"},
    )
    def add_cart(self, request):
        serializer = AddCartDetailSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            updated_serializer = CartDetailSerializer(instance)
            return response.Response(
                updated_serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Submit Cart",
        description="Submit Cart.",
        request=ProcessCartSerializer,
        responses={201: CartSerializer, 400: "Bad Request"},
    )
    def process_cart(self, request):
        serializer = ProcessCartSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            return response.Response(instance.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete Cart Item",
        description="Delete a gold purchase for the authenticated user.",
        request={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        queryset = order_cart_detail.objects.filter(
            user_id=request.user, order_cart_detail_id=kwargs.get("pk")
        )
        queryset.delete()
        return response.Response(
            {"message": "data is removed"}, status=status.HTTP_204_NO_CONTENT
        )
