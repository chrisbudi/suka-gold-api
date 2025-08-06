from venv import create
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from gold_transaction.models import gold_saving_buy
from gold_transaction.models.gold_stock import gold_history
from shared.utils.notification import create_user_notification
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from user.models import user_props
from django.db import transaction

from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string

from user.models.users import user as User

from shared.services.email_service import EmailService
from wallet.models.wallet import wallet_history


@receiver(post_save, sender=gold_saving_buy)
def handle_purchase(
    sender: type[gold_saving_buy], instance: gold_saving_buy, created, **kwargs
):
    print(created, "created", "gold saving buy")
    if created:
        with transaction.atomic():
            # update user props
            user_props_instance: user_props = user_props.objects.get(user=instance.user)
            user_props_instance.gold_wgt += instance.weight
            user_props_instance.wallet_amt -= instance.price
            user_props_instance.save()

            price = gold_price().get_active_price()
            if price is None:
                raise ValueError("Active gold price not found")

            gold_history.objects.create(
                user=instance.user,
                date=datetime.now(),
                weight=instance.weight,
                price_base=price.gold_price_base,
                buy=price.gold_price_buy,
                sell=price.gold_price_sell,
                type="D",
                amount=0,
                note="sale-" + str(instance.gold_transaction_id),
            )

            wallet_history.objects.create(
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
                print("Instance user is None. Email generation skipped.")
            if mail:
                mailService.sendMail(mail)
                create_user_notification(
                    instance.user,
                    "Pembelian Emas Digital",
                    f"Anda telah melakukan pembelian emas digital dengan nomor transaksi {instance.gold_buy_number}.",
                    NotificationIconType.INFO,
                    NotificationTransactionType.GOLD_BUY,
                )


def generate_email(gold: gold_saving_buy, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = f"""
        <tr>
        <td style="text-align: center;">{detail_number}</td>
        <td style="text-align: center;">Pembelian Emas Digital</td>
        <td style="text-align: right;">{gold.weight}</td>
        <td style="text-align: center;">gram</td>
        <td style="text-align: right;">{gold.price:,.2f}</td>
        <td style="text-align: right;">{gold.total_price:,.2f}</td>
        </tr>"""
    detail_number += 1
    print(table_product_data, "table_product_data")
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/purchase.html",
            {
                "NAMA_USER": user.name,
                "TANGGAL_WAKTU": gold.transaction_date.strftime("%d/%m/%Y"),
                "ID_PELANGGAN": user.member_number,
                "NO_TRANSAKSI": gold.gold_buy_number,
                "SubTotal": f"{gold.total_price:,.2f}",
                "table_product": table_product_data,
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject="Pembelian Emas Digital",
            # subject=f"Pembelian Emas Digital {gold.gold_buy_number}",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
