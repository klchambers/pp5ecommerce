from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """
    Category model designed to hold the style of wine
    e.g. white, red, & sparkling.
    """
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100)

    # Corrects automatic pluralisation of 'categorys'
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.friendly_name if self.friendly_name else self.name

    def get_friendly_name(self):
        return self.friendly_name


class Region(models.Model):
    # name = region, e.g., "Beaujolais"
    name = models.CharField(max_length=254)
    # Corresponding country in which the region is located
    country = models.CharField(max_length=254)

    class Meta:
        # preventing creation of duplicate regions
        # allows same region in different countries
        # e.g. Basque Country, Spain & Basque Country, France
        unique_together = ('name', 'country')
        # Order by country first, then by region
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.name}, {self.country}"


class GrapeVariety(models.Model):
    name = models.CharField(max_length=100, unique=True,)

    class Meta:
        verbose_name_plural = "grape varieties"

    def __str__(self):
        return self.name


class Wine(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True)
    winemaker = models.CharField(max_length=254)
    price = models.DecimalField(
                                max_digits=10,
                                decimal_places=2,
                                null=True,
                                blank=True)
    description = models.TextField(blank=True)
    # ManyToMany relationship with category model as one
    # wine can have multiple styles and one style links to many wines
    category = models.ManyToManyField(Category, related_name='wines')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=6,
                                 null=True,
                                 blank=True,
                                 decimal_places=0)
    image = CloudinaryField('image', blank=True)
    grape_varieties = models.ManyToManyField(
        GrapeVariety, related_name='wines', blank=True)

    """
    Automatically generate a slug from the title.
    Use of slugify adapted from code posted by Ikechukwu Henry Odoh
    In this Stack Overflow thread:
    https://stackoverflow.com/questions/50436658/how-to-auto-generate-slug-from-my-album-model-in-django-2-0-4
    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Wine, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, by {self.winemaker}"
