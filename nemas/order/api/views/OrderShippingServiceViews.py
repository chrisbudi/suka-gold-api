import json
from requests import Response
from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from common import round_value

# Correct model import
from shared.services.external.delivery.sapx.sapx_service import SapxService
from order.api.serializers import OrderShippingSerializer
from user.models.users import user_address


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

                item_weight = request.data.get("weight")
                item_amount = request.data.get("amount")
                partner = request.data.get("delivery_partner_code")
                address = user_address.objects.filter(user=request.user).first()
                item_show = []

                if partner == "SAPX":
                    # process sapx service
                    item_show = self.process_sapx(item_weight, item_amount, address)
                elif partner == "PAXEL":
                    item_show = self.process_paxel(item_weight, item_amount, address)
                    # process paxel service
                    pass
                else:
                    return response.Response(
                        {"error": "Invalid delivery partner code"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return response.Response({"services": item_show}, status.HTTP_200_OK)
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")

    def process_sapx(self, item_weight, item_amount, address: user_address):
        """Process sapx service"""

        sapx_service = SapxService()
        payload = {
            "origin": "JK07",
            "destination": "JI28",
            "weight": float(item_weight),
            "customer_code": "DEV000",
            "volumetric": "1x1x1",
            "insurance_type_code": "INS02",
            "item_value": float(item_amount),
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
                    "insurance_cost": item["insurance_cost"]
                    + item["insurance_admin_cost"],
                    "insurance_cost_round": round_value.round_up_to_100(
                        item["insurance_cost"]
                    )
                    + item["insurance_admin_cost"],
                    "total_cost": item["total_cost"],
                    "total_cost_round": round_value.round_up_to_100(item["total_cost"]),
                    "service_type_code": item["service_type_code"],
                    "service_type_name": item["service_type_name"],
                    "sla": item["sla"],
                }
            )

        return item_show

    def process_paxel(self, item_weight, item_amount, address: user_address):
        """Process paxel service"""
        # Implement paxel service processing logic here
        # This is a placeholder for the actual implementation
        pass
