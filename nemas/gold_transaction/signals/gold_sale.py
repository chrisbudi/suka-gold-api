from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from core.domain import gold_price
from django.contrib.auth import get_user_model

from gold_transaction.models import gold_saving_sell
from user.models import user_gold_history, user_wallet_history, user_props
from django.db import transaction

from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string

from user.models.users import user as User

from shared_kernel.services.email_service import EmailService


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

            user_gold_history.objects.create(
                user=instance.user,
                gold_purchase_date=datetime.now(),
                gold_weight=instance.weight,
                gold_history_price_base=price.gold_price_base,
                gold_history_price_buy=price.gold_price_buy,
                gold_history_price_sell=price.gold_price_sell,
                gold_history_type="C",
                gold_history_amount=0,
                gold_history_note="sale-" + str(instance.gold_transaction_id),
            )

            user_wallet_history.objects.create(
                user=instance.user,
                wallet_history_date=datetime.now(),
                wallet_history_amount=instance.price,
                wallet_history_type="D",
                wallet_history_notes="sale-" + str(instance.gold_transaction_id),
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
            else:
                print("Failed to generate email. Mail object is None.")


def generate_email(gold: gold_saving_sell, user: User):
    # Format the email body with the reset key
    detail_number = 1
    table_product_data = f"""
        <tr>
        <td>{detail_number}</td>
        <td>Penjualan Emas Digital</td>
        <td>{gold.weight}</td>
        <td>gram</td>
        <td>{gold.price:,.2f}</td>
        <td>{gold.total_price:,.2f}</td>
        </tr>"""

    print(table_product_data, "table_product_data")
    # email_body = email_body.replace(f"{{table_product}}", table_product_data)
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/sale.html",
            {
                "NAMA_USER": user.name,
                "TANGGAL_WAKTU": gold.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
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
