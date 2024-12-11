from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Faq


@receiver(post_save, sender=Faq)
def send_notification_on_publish(sender, instance, created, **kwargs):
    """
    Send email to user when their FAQ is answered and published

    Adapted from code posted in this
    (https://dnmtechs.com/django-post_save-signal-implementation-in-python-3-programming/)
    blog post by Del Margaret on 5th December 2024
    """
    if not created and instance.status == 1 and instance.user and instance.user.email: # noqa
        subject = f"Your Question '{instance.question}' has been Answered and Published" # noqa
        message = f'''Hello {instance.user.username},\n\n
        Your question "{instance.question}" has been answered
        and marked as published on our FAQ page.\n
        You can view it now at https://pp5ecommerce-a72d5065ca06.herokuapp.com/faq.''' # noqa
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email]
        )
