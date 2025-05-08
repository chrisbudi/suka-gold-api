from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from core.domain import gold_price

from order.models import order_gold, order_gold_detail
from order.models import order_payment
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string

from user.models.users import user as User

from shared_kernel.services.email_service import EmailService


@receiver(post_save, sender=order_payment)
def handle_order_gold_payment(
    sender: type[order_payment], instance: order_payment, created, **kwargs
):
    print("send email")
    order_gold_model = instance.order_gold
    user = instance.order_gold.user
    if order_gold_model.order_gold_payment_status == "PAID" or created:
        mailService = EmailService()
        mail = generate_email(order_gold_model, instance, user)
        if mail:
            mailService.sendMail(mail)
        else:
            print("Failed to generate email. Mail object is None.")


def generate_email(order: order_gold, order_payment: order_payment, user: User):
    # Format the email body with the reset key
    order_detail = order_gold_detail.objects.select_related("gold").filter(
        order_gold=order
    )
    detail_number = 1
    table_product_data = ""
    for detail in order_detail:
        table_product_data += f"""
        <tr>
        <td>{detail_number}</td>
        <td>{detail.gold.brand} {detail.gold.type} {detail.gold.gold_weight}</td>
        <td>{detail.qty:,}</td>
        <td>gr</td>
        <td>{detail.order_price_round:,.2f}</td>
        <td>{detail.order_detail_total_price_round:,.2f}</td>
        </tr>"""
        detail_number += 1

    # email_body = email_body.replace(f"{{table_product}}", table_product_data)
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/invoice.html",
            {
                "NAMA_USER": user.name,
                "ID_PELANGGAN": user.member_number,
                "TANGGAL_WAKTU": (
                    order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    if order.order_timestamp
                    else "N/A"
                ),
                "NO_TRANSAKSI": order.order_number,
                "table_product": table_product_data,
                "Expedisi": order.tracking_courier_name,
                "Expedisi_Cost": f"{((order.order_tracking_amount or 0) + (order.order_tracking_packing or 0)):,.2f}",
                "Insurance_Cost": f"{(order.order_tracking_insurance_total or 0.0):,.2f}",
                "SubTotal": f"{order.order_total_price_round:,.2f}",
                "GrandTotal": f"{order.order_grand_total_price:,.2f}",
                "Pembayaran": (order_payment.order_payment_method_name or "")
                + " - "
                + (order_payment.order_payment_number or ""),
                **mail_props,
            },
        )
        print(email_html, "email_html")
        sendGridEmail = settings.SENDGRID_EMAIL
        print(sendGridEmail, "email setting")

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
