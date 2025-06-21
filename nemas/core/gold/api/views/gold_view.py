from core.gold.api.serializers import (
    GoldSerializer as objectSerializer,
    GoldUploadSerializer as uploadSerializer,
    GoldServiceFilter as objectFilter,
    GoldProductShowSerializer,
)
from rest_framework import status, viewsets, filters, pagination, response
from core.domain import gold as modelInfo, gold_price
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from shared.services.s3_services import S3Service
import os
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Value, IntegerField, Prefetch, Count, Q, Sum
from core.domain import gold_cert_detail_price as CoreGoldCertDetailPrice
from order.models import order_gold_detail as OrderOrderGoldDetail
from django.db.models.functions import Floor
from django.db import connection
from django.db.models import Subquery, OuterRef


@extend_schema(
    tags=["gold"],
)
class GoldServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = objectSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = objectFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    ordering_fields = [
        "gold_id",
        "create_time",
        "upd_time",
        "brand",
        "gold_weight",
        "gold_price_summary_roundup",
        "gold_price_summary",
    ]
    ordering = ["-create_time"]

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "list_product_show", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        responses=GoldProductShowSerializer(many=True),
        tags=["gold"],
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Fields to order by, e.g. '-create_time', 'gold_id', etc.",
                required=False,
            ),
        ],
    )
    def list_product_show(self, request):
        gold_price_buy = cache.get("gold_price_buy")
        if gold_price_buy is None:
            gold_price_buy = gold_price().get_active_price().gold_price_buy or 0
            cache.set("gold_price_buy", gold_price_buy, timeout=60)

        # Subquery for gold_cert_detail_price count
        cert_detail_count_subquery = (
            CoreGoldCertDetailPrice.objects.filter(
                gold_id=OuterRef("pk"), include_stock=True
            )
            .values("gold_id")
            .annotate(count=Count("id"))
            .values("count")[:1]
        )

        # Subquery for open order_gold_detail count
        open_order_count_subquery = (
            OrderOrderGoldDetail.objects.filter(
                gold_id=OuterRef("pk"), order_detail_stock_status="open"
            )
            .values("gold_id")
            .annotate(count=Sum("qty"))
            .values("count")[:1]
        )

        queryset = (
            modelInfo.objects.all()
            .select_related("certificate")
            .annotate(
                gold_price_summary=F("gold_weight")
                * Value(gold_price_buy, output_field=IntegerField()),
                gold_price_summary_roundup=Floor(
                    (F("gold_weight") * Value(gold_price_buy)) / 100
                )
                * 100
                + 100
                + F("product_cost")
                + F("certificate__cert_price"),
                cert_detail_count=Subquery(
                    cert_detail_count_subquery, output_field=IntegerField()
                ),
                open_order_count=Subquery(
                    open_order_count_subquery, output_field=IntegerField()
                ),
            )
        )

        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldProductShowSerializer(paginated_queryset, many=True)
        paginated_result = self.get_paginated_response(serializer.data)

        # print(f"Queries executed in my_view:")
        # for query in connection.queries:
        #     print(f"  SQL: {query['sql']}")
        #     print(f"  Time: {query['time']} ms")
        #     print("-" * 20)

        return paginated_result

    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)

        ordering_filter = filters.OrderingFilter()
        queryset = ordering_filter.filter_queryset(request, queryset, self)

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
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, id=None):
        info = get_object_or_404(modelInfo, pk=id)
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
