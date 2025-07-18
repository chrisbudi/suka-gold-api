from rest_framework.decorators import api_view
from core.information.api.serializers import (
    InformationArticleSerializer as infoSerializer,
    InformationArticleFilter as ratingFilter,
    InformationArticleUploadSerializer as uploadSerializer,
)
from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.domain import information_article as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from shared.services.s3_services import S3Service
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["Information - Article"],
)
class InformationArticleViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ratingFilter

    ordering_fields = ["information_article_id", "create_time", "upd_time"]
    ordering = ["-create_time"]

    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    def get_permissions(self):
        request_method = self.request.method
        path = self.request.path
        if request_method == "GET" and (path.endswith("/") or "/article/" in path):
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = modelInfo.objects.all()
        queryset = self.filter_queryset(queryset)

        # implement ordering
        ordering_filter = filters.OrderingFilter()
        queryset = ordering_filter.filter_queryset(request, queryset, self)

        paginated_queryset = self.paginate_queryset(queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = infoSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = infoSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = infoSerializer(
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
                "message": "Information article deleted successfully",
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
    )
    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request, id=None):
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
                file_name = f"article/{file.name}"
                file_url = s3_service.upload_file(
                    file_obj=file, file_name=file_name, content_type=file.content_type
                )
                # update information_promo model where modelid
                information = modelInfo.objects.get(information_article_id=id)
                if information:
                    information.article_background = file_url
                    information.save()

                return response.Response(
                    {"message": "File uploaded successfully", "file_url": file_url},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
