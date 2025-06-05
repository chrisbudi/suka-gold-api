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
        order_qty_html = f"<td style='text-align: center;'>{detail.qty:,.0f}</td> "
        table_product_data += f"""
        <tr>
        <td style="text-align: center;">{detail_number}</td>
        <td style="text-align: left;">{detail.gold.brand} - {detail.gold.type}</td>
        <td style="text-align: center;">{detail.weight:,.4f}</td>
        <td style="text-align: center;">gram</td> 
        {order_qty_html}
        <td style="text-align: center;">{(detail.weight * detail.qty):,.0f}</td>
        <td style="text-align: right;">{(detail.order_price_round if detail.order_type == "buy" else 0):,.2f}</td>
        <td style="text-align: right;">{(detail.order_detail_total_price_round if detail.order_type == "buy" else 0):,.2f}</td>
        </tr>"""

        if order.order_type == "redeem":
            detail_number += 1

            table_product_data += f"""
            <tr>
            <td style="text-align: center;">{detail_number}</td>
            <td style="text-align: left;">{detail.cert_brand}</td>
            <td style="text-align: center;">{1}</td>
            <td style="text-align: center;">Pcs</td>
            {order_qty_html}
            <td style="text-align: center;">{1}</td>
            <td style="text-align: right;">{detail.cert_price:,.2f}</td>
            <td style="text-align: right;">{detail.order_detail_total_price_round:,.2f}</td>
            </tr>"""

        detail_number += 1

    # email_body = email_body.replace(f"{{table_product}}", table_product_data)
    mail_props = EmailService().get_email_props()
    email_template = (
        "email/transaction/invoice.html"
        if order.order_type == "buy"
        else "email/transaction/invoice_emas.html"
    )
    try:
        email_html = render_to_string(
            email_template,
            {
                "NAMA_USER": user.name,
                "ID_PELANGGAN": user.member_number,
                "TANGGAL_WAKTU": (
                    order.order_timestamp.strftime("%d/%m/%Y")
                    if order.order_timestamp
                    else "N/A"
                ),
                "DESC_TRANSAKSI": (
                    "Beli Emas" if order.order_type == "buy" else "Tarik Emas"
                ),
                "NO_TRANSAKSI": order.order_number,
                "table_product": table_product_data,
                "Expedisi": order.tracking_courier_name,
                "Expedisi_Cost": f"{((order.order_tracking_amount or 0)):,.2f}",
                "Admin_Cost": f"{((order.order_admin_amount or 0)):,.2f}",
                "Insurance_Cost": f"{(order.order_tracking_insurance_total_round or 0.0):,.2f}",
                "SubTotal": f"{order.order_total_price_round:,.2f}",
                "GrandTotal": f"{order.order_grand_total_price:,.2f}",
                "STATUS": order_payment.order_payment_status,
                "Pembayaran": (order_payment.order_payment_method_name or "")
                + " - "
                + (order_payment.order_payment_number or ""),
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject=(
                "Pembelian Produk Emas"
                if order.order_type == "buy"
                else "Penarikan Emas"
            ),
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
