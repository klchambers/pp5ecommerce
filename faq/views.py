from django.shortcuts import render, redirect
from .models import Faq
from .forms import FaqForm


def faq_list(request):
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

            # redirect back to the FAQ page
            return redirect('faq')

    template = 'faq/faq.html'
    context = {
        'published_faqs': published_faqs,
        'form': form
    }

    return render(request, template, context)
