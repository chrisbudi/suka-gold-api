from core.information.api.serializers import (
    InformationPromoSerializer as infoSerializer,
    InformationPromoFilter as promoFilter,
    PromoUploadSerializer as uploadSerializer,
)

from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.domain import information_promo as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from shared_kernel.services.s3_services import S3Service


@extend_schema(
    tags=["Information - Promo"],
)
class InformationPromoViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = promoFilter

    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = infoSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = infoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = infoSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        info.delete()
        return response.Response(
            {
                "message": "Information Promo deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class PromoUploadAPIView(viewsets.ModelViewSet):

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
        tags=["Information - Promo"],
    )
    def upload(self, request, *args, **kwargs):
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
                file_name = f"promo/{file.name}"
                file_url = s3_service.upload_file(
                    file_obj=file, file_name=file_name, content_type=file.content_type
                )
                # update information_promo model where modelid
                id = request.data.get("id")
                information_promo = modelInfo.objects.get(id=id)
                if information_promo:
                    information_promo.promo_url_background = file_url
                    information_promo.save()

                return response.Response(
                    {"message": "File uploaded successfully", "file_url": file_url},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
