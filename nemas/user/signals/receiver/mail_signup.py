from django.core.mail import send_mail
from django.dispatch import receiver

# from user.signals import user_signup


def send_welcome_email(sender, **kwargs):
    user = kwargs["user"]
    send_mail(
        "Welcome to Our Service",
        "Thank you for signing up!",
        "from@example.com",
        [user.email],
        fail_silently=False,
    )
