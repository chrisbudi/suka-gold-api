from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from sendgrid.helpers.mail import Mail

from core.domain import gold_price
from gold_transaction.models import gold_saving_sell
from shared.services.email_service import EmailService
from shared.utils.notification import create_user_notification
from user.models import GoldHistory, WalletHistory, user_props
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from user.models.users import user as User


@receiver(post_save, sender=gold_saving_sell)
def handle_sale(sender: type[gold_saving_sell], instance, created, **kwargs):
    print(created, "created", "gold saving sell")
    if created:
        with transaction.atomic():
            # update user props
            user_props_instance: user_props = user_props.objects.get(user=instance.user)
            user_props_instance.gold_wgt -= instance.weight
            user_props_instance.wallet_amt += instance.price
            user_props_instance.save()

            price_instance = gold_price()
            price = price_instance.get_active_price()
            if price is None:
                raise ValueError("Active gold price not found")

            GoldHistory.objects.create(
                user=instance.user,
                date=datetime.now(),
                weight=instance.weight,
                price_base=price.gold_price_base,
                price_buy=price.gold_price_buy,
                price_sell=price.gold_price_sell,
                transaction_type="C",
                amount=0,
                note="sale-" + str(instance.gold_transaction_id),
            )

            WalletHistory.objects.create(
                user=instance.user,
                date=datetime.now(),
                amount=instance.price,
                type="D",
                notes="sale-" + str(instance.gold_transaction_id),
            )
            # send email
            mailService = EmailService()
            if instance.user is not None:
                mail = generate_email(instance, instance.user)
            else:
                print("User is None, cannot generate email.")
                return

            if mail:
                mailService.sendMail(mail)
                create_user_notification(
                    instance.user,
                    "Pembelian Emas Digital",
                    f"Anda telah melakukan penjualan emas digital dengan nomor transaksi {instance.gold_sell_number}.",
                    NotificationIconType.INFO,
                    NotificationTransactionType.GOLD_SELL,
                )

            else:
                print("Failed to generate email. Mail object is None.")


def generate_email(gold: gold_saving_sell, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = f"""
        <tr>
        <td style="text-align: center;">{detail_number}</td>
        <td style="text-align: center;">Penjualan Emas Digital</td>
        <td style="text-align: right;">{gold.weight}</td>
        <td style="text-align: center;">gram</td>
        <td style="text-align: right;">{gold.price:,.2f}</td>
        <td style="text-align: right;">{gold.total_price:,.2f}</td>
        </tr>"""

    print(table_product_data, "table_product_data")
    # email_body = email_body.replace(f"{{table_product}}", table_product_data)
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/sale.html",
            {
                "NAMA_USER": user.name,
                "TANGGAL_WAKTU": gold.transaction_date.strftime("%d/%m/%Y"),
                "ID_PELANGGAN": user.member_number,
                "NO_TRANSAKSI": gold.gold_sell_number,
                "GrandTotal": f"{gold.total_price:,.2f}",
                "table_product": table_product_data,
                **mail_props,
            },
        )
        # print(email_html, "email_html")
        sendGridEmail = settings.SENDGRID_EMAIL
        # print(sendGridEmail, "email setting")

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject="Penjualan Emas Digital",
            # subject=f"Penjualan Emas Digital {gold.gold_sell_number}",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
