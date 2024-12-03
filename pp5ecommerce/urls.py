"""
URL configuration for pp5ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    # Serve robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    # Serve sitemap.xml
    path('sitemap.xml', TemplateView.as_view(
        template_name="sitemap.xml", content_type='application/xml')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Set custom 404 handler to the project-level views
handler404 = 'pp5ecommerce.views.custom_404'
handler500 = 'pp5ecommerce.views.custom_500'
