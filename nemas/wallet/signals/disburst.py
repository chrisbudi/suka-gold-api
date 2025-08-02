from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from shared.utils.notification import create_user_notification
from user.models.user_history import WalletHistory
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from wallet.models import disburst_transaction
from user.models import user_props
from django.db import transaction
from sendgrid.helpers.mail import Mail

from django.template.loader import render_to_string

from user.models.users import user as User

from shared.services.email_service import EmailService
from django.conf import settings


@receiver(post_save, sender=disburst_transaction)
def handle_disburst(
    sender: type[disburst_transaction],
    instance: disburst_transaction,
    created,
    **kwargs,
):
    if created:
        with transaction.atomic():
            # update user props
            user_props_instance: user_props = user_props.objects.get(user=instance.user)
            user_props_instance.wallet_amt -= instance.disburst_total_amount
            user_props_instance.save()

            WalletHistory.objects.create(
                user=instance.user,
                wallet_history_date=datetime.now(),
                wallet_history_amount=instance.disburst_total_amount,
                wallet_history_type="D",
                wallet_history_notes="disb-" + str(instance.disburst_transaction_id),
            )
        # send email
        mailService = EmailService()
        mail = generate_email(instance, instance.user)
        if mail:
            mailService.sendMail(mail)
            create_user_notification(
                instance.user,
                title="Penarikan Uang Berhasil",
                message=f"Penarikan uang Anda untuk transaksi {instance.disburst_number} telah berhasil diproses.",
                icon_type=NotificationIconType.INFO,
                transaction_type=NotificationTransactionType.WITHDRAW,
            )
        else:
            print("Failed to generate email. Mail object is None.")


def generate_email(disburst: disburst_transaction, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = ""
    # for detail in disburst:
    table_product_data += f"""
    <tr>
    <td style="text-align: center;">{detail_number}</td>
    <td style="text-align: center;">Penarikan Uang</td>
    <td style="text-align: right;">{disburst.disburst_amount:,.2f}</td>
    <td style="text-align: right;">{disburst.disburst_admin:,.2f}</td>
    <td style="text-align: right;">{disburst.disburst_total_amount:,.2f}</td>
    </tr>"""
    detail_number += 1

    # email_body = email_body.replace(f"{{table_product}}", table_product_data)
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/withdraw.html",
            {
                "ID_PELANGGAN": user.member_number,
                "NAMA_USER": user.name,
                "NO_TRANSAKSI": disburst.disburst_number,
                "TANGGAL_WAKTU": (
                    disburst.disburst_timestamp.strftime("%d/%m/%Y")
                    if disburst.disburst_timestamp
                    else "N/A"
                ),
                "TOTAL_AMOUNT": f"{disburst.disburst_total_amount:,.2f}",
                "table_product": table_product_data,
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject="Penarikan Uang",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
