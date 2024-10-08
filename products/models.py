from django.db import models
from django.utils.text import slugify


# Create your models here.
class Wine(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True)
    winemaker = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    category = models.ManyToManyField()
    region = models.ForeignKey()
    rating = models.DecimalField(max_digits=6, blank=True)
    image = models.ImageField(blank=True)

    """
    Automatically generate a slug from the title.
    Use of slugify adapted from code posted by Ikechukwu Henry Odoh
    In this Stack Overflow thread:
    https://stackoverflow.com/questions/50436658/how-to-auto-generate-slug-from-my-album-model-in-django-2-0-4
    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Wine, self).save(*args, **kwargs)
