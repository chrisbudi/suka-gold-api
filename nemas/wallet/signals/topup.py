from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from wallet.models import topup_transaction
from user.models import user_wallet_history, user_props
from django.db import transaction
from sendgrid.helpers.mail import Mail

from django.template.loader import render_to_string

from user.models.users import user as User

from shared_kernel.services.email_service import EmailService
from django.conf import settings


@receiver(post_save, sender=topup_transaction)
def handle_disburst(
    sender: type[topup_transaction],
    instance: topup_transaction,
    created,
    **kwargs,
):
    if instance.topup_status == "PAID" or created:
        # send email
        mailService = EmailService()
        mail = generate_email(instance, instance.user)
        if mail:
            mailService.sendMail(mail)
        else:
            print("Failed to generate email. Mail object is None.")


def generate_email(topup: topup_transaction, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = ""
    # for detail in disburst:
    table_product_data += f"""
    <tr>
    <td>{detail_number}</td>
    <td>Top Up</td>
    <td>{topup.topup_amount}</td>
    </tr>"""
    detail_number += 1

    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/topup.html",
            {
                "NAMA_USER": user.name,
                "NO_TRANSAKSI": topup.topup_transaction_id,
                "Total": topup.topup_amount,
                "table_product": table_product_data,
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
