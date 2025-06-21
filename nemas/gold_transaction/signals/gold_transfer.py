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

from shared.services.email_service import EmailService
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
                    gold_weight=instance.transfer_member_transfered_weight,
                    gold_history_price_base=price.gold_price_base,
                    gold_history_price_buy=price.gold_price_buy,
                    gold_history_price_sell=price.gold_price_sell,
                    gold_history_type="D",
                    gold_history_amount=0,
                    gold_history_note="transfer-" + instance.transfer_ref_number,
                ),
            ]
            # return admin to main account
        )

        UserFrom = instance.user_from
        UserTo = instance.user_to
        mailFrom = generate_email_receive(instance, UserFrom, UserTo)
        mailTo = generate_email_sender(instance, UserTo, UserFrom)
        mailService = EmailService()
        if mailService:
            for mail, role in [(mailFrom, "sender"), (mailTo, "receiver")]:
                if mail:
                    mailService.sendMail(mail)
                else:
                    print(f"Failed to generate email for {role}. Mail object is None.")
        else:
            print("Failed to create EmailService instance. Mail object is None.")


def generate_email_sender(transfer: gold_transfer, userTo: User, userFrom: User):
    # Format the email body with the reset key

    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/transfer_sender.html",
            {
                "NAMA_USER": userFrom.name,
                "NAMA_PENERIMA": userTo.name,
                "AMOUNT_WEIGHT_SEND": f"{transfer.transfer_member_gold_weight:,.4f}",
                "AMOUNT_VALUE": f"{transfer.transfer_member_amount_received:,.2f}",
                "AMOUNT_VALUE_RECEIVE": f"{transfer.transfer_member_amount_received:,.2f}",
                "AMOUNT_WEIGHT_RECEIVE": f"{transfer.transfer_member_transfered_weight:,.4f}",
                "NILAI_POTONGAN_GRAM": f"{transfer.transfer_member_admin_weight:,.4f}",
                "NILAI_POTONGAN_PERSEN": f"{transfer.transfer_member_admin_percentage:,.2f}",
                "PESAN": transfer.transfer_member_notes,
                "TUJUAN": transfer.transfer_member_service_option or " ",
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[userFrom.email],
            subject="Kirim Emas Ke Member",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)


def generate_email_receive(transfer: gold_transfer, userFrom: User, userTo: User):
    # Format the email body with the reset key

    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/transaction/transfer_receive.html",
            {
                "NAMA_USER": userTo.name,
                "NAMA_PENGIRIM": userFrom.name,
                "AMOUNT_WEIGHT_SEND": f"{transfer.transfer_member_gold_weight:,.4f}",
                "AMOUNT_VALUE": f"{transfer.transfer_member_amount_received:,.2f}",
                "AMOUNT_WEIGHT_RECEIVE": f"{transfer.transfer_member_transfered_weight:,.4f}",
                "NILAI_POTONGAN_GRAM": f"{transfer.transfer_member_admin_weight:,.4f}",
                "NILAI_POTONGAN_PERSEN": f"{transfer.transfer_member_admin_percentage:,.2f}",
                "PESAN": transfer.transfer_member_notes,
                "TUJUAN": transfer.transfer_member_service_option or " ",
                **mail_props,
            },
        )
        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[userTo.email],
            subject="Terima Emas Dari Member",
            # subject="Transfer Emas Receive",
            html_content=email_html,
        )
        return message
    except FileNotFoundError as e:
        print("Template file not found:", e)
    except Exception as e:
        print("Failed to render email template:", e)
