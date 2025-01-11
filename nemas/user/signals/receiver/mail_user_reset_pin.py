from django.core.mail import send_mail
from django.dispatch import receiver

# from user.signals import email_user_reset_pin, email_user_reset_pin_done

# @receiver(email_user_reset_pin)
# def send_welcome_email(sender, **kwargs):
#     user = kwargs["user"]
#     send_mail(
#         "Welcome to Our Service",
#         "Thank you for signing up!",
#         "from@example.com",
#         [user.email],
#         fail_silently=False,
#     )
