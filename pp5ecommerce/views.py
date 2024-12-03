from django.shortcuts import render


def custom_404(request, exception):
    """
    Error handler that renders a friendly 404 page.
    """
    return render(request, 'errors/404.html', status=404)


def custom_500(request, exception):
    """
    Error handler that renders a friendly 404 page.
    """
    return render(request, 'errors/500.html', status=500)
