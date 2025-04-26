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


# @receiver(post_save, sender=disburst_transaction)
# def handle_disburst(
#     sender: type[disburst_transaction],
#     instance: disburst_transaction,
#     created,
#     **kwargs,
# ):
#     if created:
#         with transaction.atomic():
#             # update user props
#             user_props_instance: user_props = user_props.objects.get(user=instance.user)
#             user_props_instance.wallet_amt -= instance.disburst_total_amount
#             user_props_instance.save()

#             user_wallet_history.objects.create(
#                 user=instance.user,
#                 wallet_history_date=datetime.now(),
#                 wallet_history_amount=instance.disburst_total_amount,
#                 wallet_history_type="D",
#                 wallet_history_notes="disb-" + str(instance.disburst_transaction_id),
#             )
#         # send email
#         mailService = EmailService()
#         mail = generate_email(instance, instance.user)
#         if mail:
#             mailService.sendMail(mail)
#         else:
#             print("Failed to generate email. Mail object is None.")


# def generate_email(disburst: disburst_transaction, user: User):
#     # Format the email body with the reset key
#     detail_number = 1
#     table_product_data = ""
#     # for detail in disburst:
#     table_product_data += f"""
#     <tr>
#     <td>{detail_number}</td>
#     <td>Penarikan Uang</td>
#     <td>{disburst.disburst_amount}</td>
#     </tr>"""
#     detail_number += 1

#     # email_body = email_body.replace(f"{{table_product}}", table_product_data)
#     mail_props = EmailService().get_email_props()
#     try:
#         email_html = render_to_string(
#             "email/transaction/withdraw.html",
#             {
#                 "TANGGAL_WAKTU": disburst.disburst_timestamp.strftime(
#                     "%Y-%m-%d %H:%M:%S"
#                 ),
#                 "NAMA_USER": user.name,
#                 "NO_TRANSAKSI": disburst.disburst_payment_ref,
#                 "JUMLAH_SALDO": disburst.disburst_amount,
#                 "ADMIN": disburst.disburst_admin,
#                 "TOTAL_AMOUNT": disburst.disburst_total_amount,
#                 "table_product": table_product_data,
#                 **mail_props,
#             },
#         )
#         print(email_html, "email_html")
#         sendGridEmail = settings.SENDGRID_EMAIL
#         print(sendGridEmail, "email setting")

#         message = Mail(
#             from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
#             to_emails=[user.email],
#             subject="Nemas Disburst Transaction",
#             html_content=email_html,
#         )
#         return message
#     except FileNotFoundError as e:
#         print("Template file not found:", e)
#     except Exception as e:
#         print("Failed to render email template:", e)
