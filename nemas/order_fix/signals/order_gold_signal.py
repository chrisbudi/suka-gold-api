from re import U
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from django.db import transaction
from order.models import (
    order_gold,
    order_cart,
    order_cart_detail,
    order_payment,
    order_gold_detail,
)

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import Settings, settings
from django.template.loader import render_to_string

from user.models.users import user as User


@receiver(post_save, sender=order_gold)
def handle_order_gold(
    sender: type[order_gold], instance: order_gold, created, **kwargs
):

    order_gold_model: order_gold = instance

    # update order cart to complete true
    if created:
        with transaction.atomic():
            if instance.order_cart is not None:
                order_cart_model = order_cart.objects.get(
                    order_cart_id=instance.order_cart.order_cart_id
                )
            else:
                raise ValueError(
                    "instance.order_cart is None, cannot access order_cart_id"
                )
            order_cart_model.completed_cart = True
            order_cart_model.save()

            order_cart_detail_model = order_cart_detail.objects.filter(
                cart_id=instance.order_cart.order_cart_id
            )

            for detail in order_cart_detail_model:
                detail.completed_cart = True
                detail.save()

        print(created, "created", "gold saving buy")

    else:
        with transaction.atomic():
            if instance.order_gold_payment_status == "PAID":
                order_payment_instance = order_payment.objects.filter(
                    order_gold=instance.order_gold_id
                ).first()
                if order_payment_instance:
                    order_payment_instance.order_payment_status = "PAID"
                    order_payment_instance.save()


#         if instance.order_gold_payment_status == "PAID":
#             sendGridEmail = settings.SENDGRID_EMAIL
#             # order_gold_model = instance
#             user = instance.user
#             order_payment_instance = order_payment.objects.get(order_gold=instance)

#             mail = generate_email(order_gold_model, order_payment_instance, user)

#             sg = SendGridAPIClient(sendGridEmail["API_KEY"])
#             response = sg.send(message=mail)
#             print(
#                 response.status_code,
#                 response.body,
#                 response.headers,
#                 "response",
#             )
#             if response.status_code == 202:
#                 print("Email sent successfully")
#             else:
#                 print("Failed to send email")
#             return response.status_code

#             # send email send grid service
#             pass


# def generate_email(order: order_gold, order_payment: order_payment, user: User):

#     # with open(template_path, "r") as template_file:
#     #     email_body = template_file.read()

#     # Format the email body with the reset key
#     order_detail = order_gold_detail.objects.select_related("gold").filter(
#         order_gold=order_gold
#     )
#     print(order_detail, "order_detail")
#     table_product_data = ""
#     for detail in order_detail:
#         table_product_data += f"""
#         <tr>
#         <td>{detail.gold.brand} {detail.gold.type} {detail.gold.gold_weight}</td>
#         <td>{detail.qty}</td>
#         <td>{detail.order_price}</td>
#         <td>{detail.order_detail_total_price_round}</td>
#         </tr>"""

#     # email_body = email_body.replace(f"{{table_product}}", table_product_data)

#     print(table_product_data, "product data")
#     print("successfully render to html")

#     # print(email_html, "email_html")
#     try:
#         print("try to send email")
#         email_html = render_to_string(
#             "transaction/invoice.html",
#             {
#                 "transaction_date": order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#                 "transaction_number": order.order_number,
#                 "transaction_account": order.user.id,
#                 "first_name": order.user.name,
#                 "table_product": table_product_data,
#                 "SubTotal": order.order_total_price,
#                 "Pph22": order.order_pph22,
#                 "GrandTotal": order.order_grand_total_price,
#                 "Pembayaran": order_payment.order_payment_method_name,
#             },
#         )
#         print(email_html, "email_html")
#         sendGridEmail = settings.SENDGRID_EMAIL
#         print(sendGridEmail, "email setting")
#         # sendgrid_api_key = settings.SENDGRID_API_KEY
#         # default_from_email = settings.DEFAULT_FROM_EMAIL

#         message = Mail(
#             from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
#             to_emails=[user.email],
#             subject="Nemas Invoice",
#             html_content=email_html,
#         )

#         print(user.email, sendGridEmail["DEFAULT_FROM_EMAIL"], "message")

#         sg = SendGridAPIClient(sendGridEmail["API_KEY"])
#         response = sg.send(message)
#         print(
#             response.status_code,
#             response.body,
#             response.headers,
#             "response",
#         )
#         if response.status_code == 202:
#             print("Email sent successfully")
#         else:
#             print("Failed to send email")
#         return response.status_code
#     except Exception as e:
#         print("Failed to render email template:", e)
#     return message
