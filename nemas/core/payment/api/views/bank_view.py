from core.payment.api.serializers import (
    BankSerializer as objectSerializer,
    BankUploadSerializer as uploadSerializer,
    BankFilter as objectFilter,
)
from rest_framework import status, viewsets, filters, pagination, response
from core.domain import bank as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from shared.services.s3_services import S3Service
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["payment - bank"],
)
class BankServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = objectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = objectFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed
    ordering_fields = "__all__"
    ordering = ["id"]

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description='Comma-separated list of fields to order by. Use "-" for descending. Example: id,-name',
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request):
        queryset = modelInfo.objects.filter(is_deleted=False)
        filter_queryset = self.filter_queryset(queryset)
        ordering = request.query_params.get("ordering")
        if ordering:
            filter_queryset = filter_queryset.order_by(*ordering.split(","))
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = objectSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = objectSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = objectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(create_user=request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        print(info, "info")
        serializer = objectSerializer(
            info, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        info.delete()
        return response.Response(
            {
                "message": "Gold object deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        request=uploadSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "url": {"type": "string"},
                },
            }
        },
        tags=["payment - bank"],
    )
    def upload(self, request, id, *args, **kwargs):
        serializer = uploadSerializer(data=request.data)
        if serializer.is_valid():
            if (
                isinstance(serializer.validated_data, dict)
                and "file" in serializer.validated_data
            ):
                file = serializer.validated_data["file"]
            else:
                return response.Response(
                    {"error": "File not provided"}, status=status.HTTP_400_BAD_REQUEST
                )
            s3_service = S3Service()
            try:
                file_name = f"bank/{id}.jpg"
                file_url = s3_service.upload_file(
                    file_obj=file, file_name=file_name, content_type=file.content_type
                )
                # update information_promo model where modelid

                try:
                    models = modelInfo.objects.get(pk=id)
                    models.bank_logo_url = file_url
                    models.save()
                except modelInfo.DoesNotExist:
                    return response.Response(
                        {"error": "Bank Id not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                return response.Response(
                    {"message": "File uploaded successfully", "file_url": file_url},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
