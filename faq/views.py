from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Faq
from .forms import FaqForm
import logging


def faq_list(request):
    """
    A view to return a list of published FAQs
    and handle user-submitted questions
    """
    # List published answers
    published_faqs = Faq.objects.filter(status=1)

    # Initialise form for authenticated users
    form = FaqForm(request.POST or None) if request.user.is_authenticated else None # noqa

    # Handle form submission
    if request.method == "POST" and form is not None:
        if form.is_valid():
            new_faq = form.save(commit=False)
            new_faq.user = request.user
            # status set to draft
            new_faq.status = 0
            new_faq.save()

            # assigning queryset of staff admin email addresses to a variable
            admin_emails = list(User.objects.filter(is_staff=True).values_list(
                'email', flat=True))
            subject = '''GlouGlou Admin | A new question has been submitted and is awaiting answer in FAQs''' # noqa
            message = (
                f'{new_faq.user.username} submitted the following question:\n'
                f'\n"{new_faq.question}".'
                f'\n\nPlease answer and publish in the admin panel. Alternatively, answer the user directly at {new_faq.user.email}' # noqa
            )
            # Sends notification email to admins that there is a
            # new question to answer and publish
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails,
                )
            except Exception as e:
                logging.error(f"Error sending confirmation email: {e}")
                raise

            # redirect back to the FAQ page
            messages.success(
                request,
                "Thank you for submitting your question!")
            return redirect(request.path)

        else:
            messages.error(
                request,
                "Error, please double check your question form and try again")

    template = 'faq/faq.html'
    context = {
        'published_faqs': published_faqs,
        'form': form
    }

    return render(request, template, context)
