from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_transaction
from gold_transaction.api.serializers import (
    GoldTransactionSerializer,
    GoldTransactionFilter,
)


@extend_schema(
    tags=["gold transaction - Gold Purchase"],
)
class GoldPurchaseListCreateAPIView(viewsets.ModelViewSet):
    queryset = gold_transaction.objects.all()  # Use the model class directly
    serializer_class = GoldTransactionSerializer
    authentication_classes = [JWTAuthentication]
    filterset_class = GoldTransactionFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ["purchase_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="List Gold Purchases",
        description="Retrieve a list of gold purchases for the authenticated user.",
        responses={200: GoldTransactionSerializer},
    )
    def list(self, request):
        queryset = gold_transaction.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        return response.Response(paginated_queryset)

    @extend_schema(
        summary="Create Gold Purchase",
        description="Create a gold purchase for the authenticated user.",
        request=GoldTransactionSerializer,
        responses={201: GoldTransactionSerializer},
    )
    def perform_create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
