from django.db.models.signals import post_save
from django.dispatch import receiver
from gold_transaction.models import gold_transfer
from user.models import user_gold_history
from core.domain import gold_price
from datetime import datetime
from decimal import Decimal
from sendgrid.helpers.mail import Mail

from django.template.loader import render_to_string

from user.models.users import user as User

from shared_kernel.services.email_service import EmailService
from django.conf import settings


@receiver(post_save, sender=gold_transfer)
def handle_transfer(sender, instance: gold_transfer, created: bool, **kwargs):
    if created:
        # update user props
        user_props = instance.user_from.user_props
        user_props.gold_wgt -= instance.transfer_member_gold_weight
        user_props.save()

        to_user_props = instance.user_to.user_props
        to_user_props.gold_wgt += instance.transfer_member_gold_weight
        to_user_props.save()

        price_instance = gold_price()
        price = price_instance.get_active_price()
        if price is None:
            raise ValueError("Active gold price not found")

        user_gold_history.objects.bulk_create(
            [
                user_gold_history(
                    user=instance.user_from,
                    gold_purchase_date=datetime.now(),
                    gold_weight=instance.transfer_member_gold_weight,
                    gold_history_price_base=price.gold_price_base,
                    gold_history_price_buy=price.gold_price_buy,
                    gold_history_price_sell=price.gold_price_sell,
                    gold_history_type="C",
                    gold_history_amount=0,
                    gold_history_note="transfer-" + instance.transfer_ref_number,
                ),
                user_gold_history(
                    user=instance.user_to,
                    gold_purchase_date=datetime.now(),
                    gold_weight=instance.transfer_member_gold_weight,
                    gold_history_price_base=price.gold_price_base,
                    gold_history_price_buy=price.gold_price_buy,
                    gold_history_price_sell=price.gold_price_sell,
                    gold_history_type="D",
                    gold_history_amount=0,
                    gold_history_note="transfer-" + instance.transfer_ref_number,
                ),
            ]
        )

        UserFrom = instance.user_from
        UserTo = instance.user_to
        mailFrom = generate_email(instance, UserFrom)
        mailTo = generate_email(instance, UserTo)
        mailService = EmailService()
        if mailService:
            if mailFrom:
                mailService.sendMail(mailFrom)
            else:
                print("Failed to generate email for sender. Mail object is None.")
            if mailTo:
                mailService.sendMail(mailTo)
            else:
                print("Failed to generate email for receiver. Mail object is None.")
        else:
            print("Failed to create EmailService instance. Mail object is None.")


def generate_email(transfer: gold_transfer, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = ""
    table_product_data += f"""
    <tr>
    <td>{detail_number}</td>
    <td>Transfer Gold</td>
    <td>{transfer.transfer_member_gold_weight}</td>
    </tr>"""
    detail_number += 1

    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/invoice.html",
            {
                "table_product": table_product_data,
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject="Nemas Invoice",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)


# def generate_email(order: order_gold, order_payment: order_payment, user: User):
#     # Format the email body with the reset key
#     order_detail = order_gold_detail.objects.select_related("gold").filter(
#         order_gold=order
#     )
#     detail_number = 1
#     table_product_data = ""
#     for detail in order_detail:
#         table_product_data += f"""
#         <tr>
#         <td>{detail_number}</td>
#         <td>{detail.gold.brand} {detail.gold.type} {detail.gold.gold_weight}</td>
#         <td>{detail.qty}</td>
#         <td>grams</td>
#         <td>{detail.order_price}</td>
#         <td>{detail.order_detail_total_price_round}</td>
#         </tr>"""
#         detail_number += 1

#     # email_body = email_body.replace(f"{{table_product}}", table_product_data)
#     mail_props = EmailService().get_email_props()
#     try:
#         email_html = render_to_string(
#             "email/transaction/invoice.html",
#             {
#                 "transaction_date": order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#                 "transaction_number": order.order_number,
#                 "transaction_account": order.user.id,
#                 "first_name": order.user.name,
#                 "table_product": table_product_data,
#                 "SubTotal": order.order_total_price_round,
#                 "Pph22": order.order_pph22,
#                 "GrandTotal": order.order_grand_total_price,
#                 "Pembayaran": order_payment.order_payment_method_name,
#                 **mail_props,
#             },
#         )
#         print(email_html, "email_html")
#         sendGridEmail = settings.SENDGRID_EMAIL
#         print(sendGridEmail, "email setting")

#         message = Mail(
#             from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
#             to_emails=[user.email],
#             subject="Nemas Invoice",
#             html_content=email_html,
#         )
#         return message
#     except FileNotFoundError as e:
#         print("Template file not found:", e)
#     except Exception as e:
#         print("Failed to render email template:", e)
