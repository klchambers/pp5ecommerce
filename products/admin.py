from django.contrib import admin
from .models import Wine, Region, Category
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Wine)
class WineAdmin(SummernoteModelAdmin):
    # Fields to display in list view
    list_display = ('name', 'winemaker', 'region', 'rating')
    # Enable search on these fields
    search_fields = ('name', 'winemaker', 'region__name', 'category__name')
    # Filters in the sidebar
    list_filter = ('region', 'category', 'rating')
    # Auto-populate slug field from name
    prepopulated_fields = {'slug': ('name',)}
    # Horizontal filter for the ManyToManyField 'category'
    filter_horizontal = ('category',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Region)
