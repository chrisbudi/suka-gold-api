from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_saving_sell, gold_transfer
from gold_transaction.api.serializers import GoldTransferSerializer, GoldTransferFilter


@extend_schema(
    tags=["gold transaction - Gold Transfer"],
)
class GoldTransferListCreateAPIView(viewsets.ModelViewSet):
    queryset = gold_transfer.objects.all()  # Use the model class directly
    serializer_class = GoldTransferSerializer
    authentication_classes = [JWTAuthentication]
    filterset_class = GoldTransferFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination

    @extend_schema(
        summary="List Gold Transfer",
        description="Retrieve a list of gold Transfer for the authenticated user.",
        responses={200: GoldTransferSerializer},
    )
    def list(self, request):
        queryset = gold_saving_sell.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldTransferSerializer(paginated_queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create Gold Transfer",
        description="Create a gold Transfer for the authenticated user.",
        request=GoldTransferSerializer,
        responses={201: GoldTransferSerializer},
    )
    def perform_create(self, request):
        serializer = GoldTransferSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
