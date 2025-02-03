from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_saving_sell
from gold_transaction.api.serializers import (
    GoldTransactionSellSerializer,
    GoldTransactionSellFilter,
)


@extend_schema(
    tags=["gold transaction - Gold Sale "],
)
class GoldSaleListCreateAPIView(viewsets.ModelViewSet):
    queryset = gold_saving_sell.objects.all()  # Use the model class directly
    serializer_class = GoldTransactionSellSerializer
    authentication_classes = [JWTAuthentication]
    filterset_class = GoldTransactionSellFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="List Gold Sales",
        description="Retrieve a list of gold Sales for the authenticated user.",
        responses={200: GoldTransactionSellSerializer},
    )
    def list(self, request):
        queryset = gold_saving_sell.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldTransactionSellSerializer(paginated_queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create Gold Sale",
        description="Create a gold Sale for the authenticated user.",
        request=GoldTransactionSellSerializer,
        responses={201: GoldTransactionSellSerializer},
    )
    def perform_create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
