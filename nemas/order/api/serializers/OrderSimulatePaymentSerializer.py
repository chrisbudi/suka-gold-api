import json
from rest_framework import serializers
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from order.models import order_gold, order_gold_detail
from django.conf import settings
import os
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class OrderSimulatedPaymentQrisSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    def validate(self, data):
        amount = data.get("amount")
        reference_id = data.get("reference_id")
        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        print(reference_id, "reference_id")
        if not reference_id:
            raise serializers.ValidationError("Reference ID is need")

        return data

    def create(self, validated_data):
        print(validated_data, "validated_data")
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]
        try:
            qris_service = QRISPaymentService()
            payload = {
                "amount": float(amount),
            }
            payload_json = json.dumps(payload)
            response = qris_service.qris_payment_simulate(reference_id, payload_json)
            print(response, "response")
            orderTransaction = order_gold.objects.get(
                order_gold_payment_ref=reference_id
            )
            orderTransaction.update_status("SUCCESS")
            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))


class OrderSimulatedPaymentVaSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    def validate(self, data):
        amount = data.get("amount")

        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        return data

    def create(self, validated_data):
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]
        try:
            va_service = VAPaymentService()
            payload = {
                "amount": float(amount),
            }
            payload_json = json.dumps(payload)
            response = va_service.va_payment_simulate(reference_id, payload_json)

            orderTransaction = order_gold.objects.get(topup_payment_ref=reference_id)
            orderTransaction.update_status("SUCCESS")

            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def send_email(self, order: order_gold):

        print("email type")

        template_file = "nemas-invoice.html"
        template_path = os.path.join(
            settings.BASE_DIR, "app", "templates", "invoice", template_file
        )
        with open(template_path, "r") as template_file:
            email_body = template_file.read()

        # Format the email body with the reset key
        order_detail = order_gold_detail.objects.select_related("gold").filter(
            order_gold=order
        )

        # email_body = email_body.replace(
        #     f"{{transaction_date}}", order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        # )
        # email_body = email_body.replace(f"{{transaction_number}}", order.order_number)
        # email_body = email_body.replace(f"{{transaction_account}}", order.user.id)
        # email_body = email_body.replace(f"{{first_name}}", order.user.name)

        table_product_data = ""
        for detail in order_detail:
            table_product_data += f"""
            <tr>
            <td>{detail.order_qty}</td>
            <td>{detail.gold.brand} {detail.gold.type} {detail.gold.gold_weight}</td>
            <td>{detail.order_detail_total_price}</td>
            </tr>"""

        email_body = email_body.replace(f"{{table_product}}", table_product_data)

        table_price_data = f"""
        <tr>
        <td colspan="2">Total</td>
        <td>{order.order_total_price}</td>
        </tr>
        """

        email_html = render_to_string(
            "invoice/nemas-invoice.html",
            {
                "transaction_date": order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "transaction_number": order.order_number,
                "transaction_account": order.user.id,
                "first_name": order.user.name,
                "table_product": table_product_data,
                "table_price": table_price_data,
            },
        )
        sendgrid = settings.sendgrid

        message = Mail(
            from_email=sendgrid.DEFAULT_FROM_EMAIL,
            to_emails=[order.user.email],
            subject="Nemas Invoice",
            html_content=email_html,
        )

        try:
            sg = SendGridAPIClient(sendgrid.SENDGRID_API_KEY)
            response = sg.send(message)
            return response.status_code
        except Exception as e:
            print(e)
