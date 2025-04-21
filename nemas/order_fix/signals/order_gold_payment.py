from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from order.models import order_gold, order_gold_detail
from order.models import order_payment
from sendgrid import SendGridAPIClient
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
    mailService = EmailService()
    mail = generate_email(order_gold_model, instance, user)
    if mail:
        mailService.sendMail(mail)
    else:
        print("Failed to generate email. Mail object is None.")


#     else:
# send email send grid service
# pass


def generate_email(order: order_gold, order_payment: order_payment, user: User):

    print("start generate email")
    # with open(template_path, "r") as template_file:
    #     email_body = template_file.read()

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
        <td>{detail.qty}</td>
        <td>gr</td>
        <td>{detail.order_price}</td>
        <td>{detail.order_detail_total_price_round}</td>
        </tr>"""
        detail_number += 1

    # email_body = email_body.replace(f"{{table_product}}", table_product_data)

    print(table_product_data, "product data")
    print("successfully render to html")

    # print(email_html, "email_html")
    try:
        print("try to send email")
        email_html = render_to_string(
            "email/transaction/invoice.html",
            {
                "transaction_date": order.order_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "transaction_number": order.order_number,
                "transaction_account": order.user.id,
                "first_name": order.user.name,
                "table_product": table_product_data,
                "SubTotal": order.order_total_price,
                "Pph22": order.order_pph22,
                "GrandTotal": order.order_grand_total_price,
                "Pembayaran": order_payment.order_payment_method_name,
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

        print(user.email, sendGridEmail["DEFAULT_FROM_EMAIL"], "message")

        sg = SendGridAPIClient(sendGridEmail["API_KEY"])
        response = sg.send(message)

        if response.status_code == 202:
            print("Email sent successfully")
        else:
            print("Failed to send email")
    except Exception as e:
        print("Failed to render email template:", e)
    return message
