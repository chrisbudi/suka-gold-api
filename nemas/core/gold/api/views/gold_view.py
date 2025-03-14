from core.gold.api.serializers import (
    GoldSerializer as objectSerializer,
    GoldUploadSerializer as uploadSerializer,
    GoldServiceFilter as objectFilter,
)
from rest_framework import status, viewsets, filters, pagination, response
from core.domain import gold as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from shared_kernel.services.s3_services import S3Service
import os
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["gold"],
)
class GoldServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = objectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = objectFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = objectSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = objectSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = objectSerializer(data=request.data)
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
        serializer = objectSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save(create_user=request.user)
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
        tags=["gold"],
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
                file_extension = os.path.splitext(file.name)[1]
                file_name = f"gold/{str(id)}/{serializer.validated_data['gold_image_code']}{file_extension}"
                file_url = s3_service.upload_file(
                    file_obj=file, file_name=file_name, content_type=file.content_type
                )
                # update information_promo model where modelid

                try:
                    information_promo = modelInfo.objects.get(pk=id)
                    if serializer.validated_data["gold_image_code"] == "image1":
                        information_promo.gold_image_1 = file_url
                    if serializer.validated_data["gold_image_code"] == "image2":
                        information_promo.gold_image_2 = file_url
                    if serializer.validated_data["gold_image_code"] == "image3":
                        information_promo.gold_image_3 = file_url
                    if serializer.validated_data["gold_image_code"] == "image4":
                        information_promo.gold_image_4 = file_url
                    if serializer.validated_data["gold_image_code"] == "image5":
                        information_promo.gold_image_5 = file_url
                    information_promo.save()
                except modelInfo.DoesNotExist:
                    return response.Response(
                        {"error": "Information Promo not found"},
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
