import decimal
from common.responses import NemasReponses
from core import address
from core.domain.delivery import delivery_partner
from shared.services.external.delivery.sapx.sapx_service import SapxService
from order_fix.api.serializers.OrderCartSerializer import User
from order_fix.type.shipping_details import ShippingDetails
from user.models.users import user_address
from order.models import order_payment, order_gold
from user.models import user_virtual_account as UserVa
from core.domain import bank as core_bank
from datetime import datetime, timedelta
from shared.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from uuid import uuid4
from decimal import Decimal
from rest_framework import serializers
from order.models import order_shipping
import json


class TrackingProcess:
    def __init__(self, order):
        self.order = order

    def submit_tracking(
        self,
        order_gold_instance: order_gold,
        user: user_address,
        shipping_data: ShippingDetails,
        delivery_partner: delivery_partner,
    ):

        if shipping_data is None:
            raise serializers.ValidationError("Shipping data is required")

        # if delivery_partner.delivery_partner_external == True:

        # if delivery_partner.delivery_partner_code == "sapx":
        #     partner_response = self.process_sapx(
        #         order_gold_instance=order_gold_instance,
        #         user=user,
        #         shipping_data=shipping_data,
        #         delivery_partner=delivery_partner,
        #     )
        #     elif delivery_partner.delivery_partner_code == "paxcel":
        #         partner_response = self.process_paxcel(
        #             order_gold_instance=order_gold_instance,
        #             user=user,
        #             shipping_data=shipping_data,
        #             delivery_partner=delivery_partner,
        #         )
        # elif delivery_partner.delivery_partner_external == False:
        #     sapx_request = {
        #         "delivery_partner_id": delivery_partner.delivery_partner_id,
        #         "delivery_partner_name": delivery_partner.delivery_partner_name,
        #         "delivery_partner_external": delivery_partner.delivery_partner_external,
        #         "delivery_partner_code": delivery_partner.delivery_partner_code,
        #         "delivery_partner_service": delivery_partner.delivery_partner_service,
        #     }

        order_shipping.objects.create(
            order_gold_id=order_gold_instance,
            delivery_partner_id=order_gold.tracking_courier,
            delivery_price=shipping_data["cost"],
            delivery_insurance_price=shipping_data["insurance"],
            delivery_total_price=shipping_data["shipping_total"],
            delivery_pickup_order_date=datetime.now(),
            delivery_pickup_date=None,
            delivery_est_date=datetime.now() + timedelta(days=1),
            delivery_actual_date=None,
            delivery_status="ISSUED",
            delivery_tracking_number="",
            delivery_tracking_url="",
            delivery_notes="",
            delivery_address=user.address,
            delivery_postal_code=user.postal_code,
            delivery_city=user.city,
            delivery_phone_number=user.phone_number,
            user=user.user,
        )

    # # process sapx
    def process_sapx(self, order_gold_instance: order_gold):
        sapx_service = SapxService()
        sapx_service.submit_order(
            order_gold_instance=order_gold_instance,
            user=self.order.user,
            shipping_data=self.order.shipping_data,
            delivery_partner=self.order.delivery_partner,
        )

        pass

    # # process paxcel
    # def process_paxcel(
    #     self, validated_data, order_amount, user, order_gold_instance: order_gold
    # ):
    #     # process paxcel
    #     pass
