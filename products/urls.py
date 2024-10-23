from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_info, name='product_info'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product,
         name='delete_product'),
    path('add/', views.add_product, name='add_product'),
    # Serve robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    # Serve sitemap.xml
    path('sitemap.xml', TemplateView.as_view(
        template_name="sitemap.xml", content_type='application/xml')),
]
