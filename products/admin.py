from django.utils.html import format_html
from django.contrib import admin
from .models import Wine, Region, Category, GrapeVariety
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Wine)
class WineAdmin(SummernoteModelAdmin):
    # Fields to display in list view
    list_display = ('name',
                    'winemaker',
                    'region',
                    'rating',
                    'price',
                    'image_preview')
    # Enable search on these fields
    search_fields = ('name', 'winemaker', 'region__name', 'category__name')
    # Filters in the sidebar
    list_filter = ('region',
                   'category',
                   'rating',
                   'grape_varieties',
                   'price')
    # Auto-populate slug field from name
    prepopulated_fields = {'slug': ('name',)}
    # Horizontal filter for the ManyToManyField 'category'
    filter_horizontal = ('category',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url) # noqa
        return "No Image"


# Register your models here.
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(GrapeVariety)
