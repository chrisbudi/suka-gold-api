import json
from requests import Response
from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from shared_kernel.services.external.sapx_service import SapxService
from shared_kernel.utils import round_value

# Correct model import
from order_fix.api.serializers import OrderShippingSerializer


@extend_schema(
    tags=["Order Shipping Fix - Get Shipping Service Price"],
)
class OrderShippingServiceAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="getPrice",
        description="Get Shipping Serivce",
        request=OrderShippingSerializer,
        responses={200: OrderShippingSerializer},
    )
    def list_shipping_service(self, request):
        """get price from sapx"""
        try:
            serializer = OrderShippingSerializer(data=request.data)

            if serializer.is_valid():
                sapx_service = SapxService()
                payload = {
                    "origin": "JK07",
                    "destination": "JI28",
                    "weight": serializer.data.get("weight"),
                    "customer_code": "DEV000",
                    "packing_type_code": "ACH06",
                    "volumetric": "1x1x1",
                    "insurance_type_code": "INS02",
                    "item_value": serializer.data.get("amount"),
                }
                payload_data = json.dumps(payload)
                data = sapx_service.get_price(payload_data)
                filtered_data = [
                    item for item in data["data"]["services"] if item["weight"] == 1
                ]
                item_show = []
                for item in filtered_data:
                    item_show.append(
                        {
                            "weight": item["weight"],
                            "insurance_cost": item["insurance_cost"],
                            "insurance_cost_round": round_value.round_up_to_100(
                                item["insurance_cost"]
                            ),
                            "total_cost": item["total_cost"],
                            "total_cost_round": round_value.round_up_to_100(
                                item["total_cost"]
                            ),
                            "service_type_code": item["service_type_code"],
                            "service_type_name": item["service_type_name"],
                            "insurance_admin_cost": item["insurance_admin_cost"],
                            "packing_cost": item["packing_cost"],
                            "cost": item["cost"],
                            "sla": item["sla"],
                        }
                    )
                return response.Response({"services": item_show}, status.HTTP_200_OK)
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")
