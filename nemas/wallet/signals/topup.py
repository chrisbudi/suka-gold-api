from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from shared.utils.notification import create_user_notification
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from wallet.models import topup_transaction
from sendgrid.helpers.mail import Mail

from django.template.loader import render_to_string

from user.models.users import user as User

from shared.services.email_service import EmailService
from django.conf import settings


@receiver(post_save, sender=topup_transaction)
def handle_topup(
    sender: type[topup_transaction],
    instance: topup_transaction,
    created,
    **kwargs,
):
    print("Topup transaction saved:", instance)
    # send email
    print("Sending email for topup transaction")
    mailService = EmailService()
    mail = generate_email(instance, instance.user)
    if mail:
        mailService.sendMail(mail)
        if instance.topup_status == "PAID":
            create_user_notification(
                instance.user,
                title="Top Up Saldo",
                message=f"Top Up Saldo Anda telah berhasil diproses.",
                icon_type=NotificationIconType.INFO,
                transaction_type=NotificationTransactionType.TOPUP,
            )
        elif instance.topup_status == "ISSUED":
            create_user_notification(
                instance.user,
                title="Top Up Saldo",
                message=f"Top Up Saldo Anda telah diterbitkan.",
                icon_type=NotificationIconType.INFO,
                transaction_type=NotificationTransactionType.TOPUP,
            )
    else:
        print("Failed to generate email. Mail object is None.")


def generate_email(topup: topup_transaction, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = ""
    # for detail in disburst:
    table_product_data += f"""
    <tr>
    <td style="text-align: center;">{detail_number}</td>
    <td style="text-align: center;">Top Up</td>
    <td style="text-align: right;">{topup.topup_amount:,.2f}</td>
    <td style="text-align: right;">{topup.topup_admin:,.2f}</td>
    <td style="text-align: right;">{topup.topup_total_amount:,.2f}</td>
    </tr>"""
    detail_number += 1

    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/topup.html",
            {
                "NAMA_USER": user.name,
                "TANGGAL_WAKTU": topup.topup_timestamp.strftime("%d/%m/%Y"),
                "ID_PELANGGAN": user.member_number,
                "NO_TRANSAKSI": topup.topup_number,
                "Total": f"{topup.topup_amount:,.2f}",
                "table_product": table_product_data,
                "TOTAL": f"{topup.topup_total_amount:,.2f}",
                "STATUS": topup.topup_status,
                "METODE_PEMBAYARAN": topup.topup_payment_method,
                **mail_props,
            },
        )
        print(email_html, "email_html")
        sendGridEmail = settings.SENDGRID_EMAIL
        print(sendGridEmail, "email setting")

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject="TopUp Saldo",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
