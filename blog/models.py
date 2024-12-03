from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=254, unique=True)
    slug = models.CharField(max_length=254, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    featured_image = CloudinaryField('image', default='placeholder')
    post = models.TextField()
    posted_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    """
    Automatically generate a slug from the title.
    Use of slugify adapted from code posted by Ikechukwu Henry Odoh
    In this Stack Overflow thread:
    https://stackoverflow.com/questions/50436658/how-to-auto-generate-slug-from-my-album-model-in-django-2-0-4
    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
